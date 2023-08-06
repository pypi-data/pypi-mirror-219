from urllib.parse import quote

import pytz

from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.models import Variable


def assemble_logfile_url(context):
    base_url = f"https://{Variable.get('global_LOGFILE_SERVER_FQDN')}"
    return f"{base_url}" \
           f"/dag_id={context.get('task_instance').dag_id}" \
           f"/run_id={quote(context['dag_run'].run_id)}" \
           f"/task_id={context.get('task_instance').task_id}" \
           f"/attempt={context.get('task_instance').prev_attempted_tries}.log" \
           f"?token=t06nd1wtqv"


def assemble_logzio_query(context):
    if context["dag_run"].run_id is None:
        return None

    base_url = "https://app-eu.logz.io/#/dashboard/osd/discover/?"
    dag_id = context.get("task_instance").dag_id
    # following the real examples by placing the query at the logz.io Kibana and copy the URL, it seems like
    # we do not need to escape the lucene query value for URL or for Lucene special characters
    # https://lucene.apache.org/core/9_6_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html
    # #Escaping_Special_Characters
    # It is sufficient if we replace "+" with "%2B" in the dag_run_id.
    dag_run_id = context["dag_run"].run_id.replace("+", "%2B")
    return f"{base_url}" \
           f"_a=(" \
           f"  columns:!(level,message,task_id,type)," \
           f"  filters:!(" \
           f"    (" \
           f"      '$state':(store:appState)," \
           f"      meta:(" \
           f"        alias:!n," \
           f"        disabled:!f," \
           f"        index:'logzioCustomerIndex*'," \
           f"        key:dag_run_id," \
           f"        negate:!f," \
           f"        params:(query:'{dag_run_id}')," \
           f"        type:phrase" \
           f"      )," \
           f"      query:(" \
           f"        match_phrase:(dag_run_id:'{dag_run_id}')" \
           f"      )" \
           f"    ),(" \
           f"      '$state':(store:appState)," \
           f"      meta:(" \
           f"        alias:!n," \
           f"        disabled:!f," \
           f"        index:'logzioCustomerIndex*'," \
           f"        key:dag_id," \
           f"        negate:!f," \
           f"        params:(query:'{dag_id}')," \
           f"        type:phrase" \
           f"      )," \
           f"      query:(" \
           f"        match_phrase:(dag_id:{dag_id})" \
           f"      )" \
           f"    )" \
           f"  )," \
           f"  index:'logzioCustomerIndex*'," \
           f"  interval:auto," \
           f"  query:(language:lucene,query:'')," \
           f"  sort:!(!('@timestamp',asc))" \
           f")&" \
           f"_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-3d,to:now))&" \
           f"accountIds=519784&" \
           f"switchToAccountId=519784".replace(" ", "")


def send_slack_message(context, slack_msg_subject, status_icon_url, slack_task_id):
    """Send a Slack notification with some context and links with customizable variants."""
    base_url = f"https://{Variable.get('global_WEBSERVER_FQDN')}"
    airflow_url = f"{base_url}/dags/{context.get('task_instance').dag_id}/grid?" \
                  f"dag_run_id={quote(context['dag_run'].run_id)}&" \
                  f"task_id={context.get('task_instance').task_id}&" \
                  f"tab=logs"

    # because we use Slack Block Kit, this message is the fallback text to render the notification,
    # not the body content itself
    notification_msg = f"{slack_msg_subject} " \
                       f"(dag={context.get('task_instance').dag_id}," \
                       f" task={context.get('task_instance').task_id}," \
                       f" try={context.get('task_instance').try_number - 1})"

    start_time = context.get("data_interval_start") \
        .astimezone(pytz.timezone("UTC")).strftime("%Y-%m-%d %H:%M:%S (%Z)")
    env = Variable.get("global_ENV")
    project_id = Variable.get("global_PROJECT_ID")
    slack_blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": slack_msg_subject}
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": status_icon_url,
                    "alt_text": "status icon"
                },
                {"type": "plain_text", "text": f"Account: {project_id}-{env}", "emoji": True},
                {"type": "plain_text", "text": f"TS: {start_time}", "emoji": True}
            ]
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*DAG*:\n{context.get('task_instance').dag_id}"},
                {"type": "mrkdwn", "text": f"*Run type*:\n{context['dag_run'].run_type}"},
                {"type": "mrkdwn", "text": f"*Task*:\n{context.get('task_instance').task_id}"},
                # NOTE-zw: we render the Slack message including the current (i.e. the one just failed) attempt #.
                # This is the on-failure callback, therefore when the code flow reaches this function, the task
                # instance must not be in the state of RUNNING. According to the Airflow source code,
                # https://github.com/CloverHealth/airflow/blob/ab412c578ed8e41014c34d4d22faa3f1a51af5f6/airflow
                # /models.py#L931-L942
                # here the ti.try_number has plus one offset. We take it back to point it to the actual failed attempt.
                {"type": "mrkdwn", "text": f"*Try#*:\n{context.get('task_instance').try_number - 1}"}
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Airflow GUI", "emoji": False},
                    "value": "Airflow",
                    "url": airflow_url
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "logz.io", "emoji": False},
                    "value": "logz.io",
                    "url": assemble_logzio_query(context)
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "raw log", "emoji": False},
                    "value": "raw log",
                    "url": assemble_logfile_url(context)
                }
            ]
        }
    ]

    slack_alert = SlackWebhookOperator(
        task_id=slack_task_id,
        message=notification_msg,
        blocks=slack_blocks,
        slack_webhook_conn_id="slack"
    )

    return slack_alert.execute(context=context)


def slack_alert_on_failure(context):
    """Send a Slack notification with some context and links when a task eventually failed."""

    send_slack_message(
        context,
        "Airflow task eventually failed",
        "https://s3.amazonaws.com/logzio-static-content-cdn/slack/high.png",
        "slack_alert_on_failure")


def slack_alert_on_retry(context):
    """Send a Slack notification with some context and links when a task failed but up for retry."""

    send_slack_message(
        context,
        "Airflow task failed but up for retry",
        "https://s3.amazonaws.com/logzio-static-content-cdn/slack/medium.png",
        "slack_alert_on_retry")
