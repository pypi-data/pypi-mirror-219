from airflow.models.dag import DAG

from rcplus_alloy_common.version import head_ref
from rcplus_alloy_common.airflow.utils import AlloyProject


class AlloyDag(DAG):
    """Alloy DAG class which enforces tags and dag_id naming convention."""

    def __init__(self, dag_id, *args, tags=None, **kwargs):
        project = AlloyProject(3)  # __init__, _load_project_config, __init__, dag_fun
        dag_id_prefix = f"{project['project_id']}-{project['software_component']}"
        if not dag_id.startswith(dag_id_prefix):
            dag_id = f"{dag_id_prefix}-{dag_id}"

        if tags is None:
            tags = []
        if project["git_repo_name"] not in tags:
            tags.append(project["git_repo_name"])
        if project["project_version"] not in tags:
            tags.append(project["project_version"])

        super().__init__(dag_id, *args, tags=tags, **kwargs)

    def run(self, *args, **kwargs):
        # NOTE-zw: This log message went nowhere even when we change the level to ERROR, further investigation required.
        self.log.info(f"Running dag `{self.dag_id}` with version `rcplus_alloy_common@{head_ref}`")
        super().run(*args, **kwargs)
