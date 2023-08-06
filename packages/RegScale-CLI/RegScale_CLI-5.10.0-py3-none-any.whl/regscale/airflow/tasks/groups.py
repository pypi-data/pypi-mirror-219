"""Define pre-made TaskGroups for usage across DAGs."""
from uuid import uuid4

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from regscale.airflow.tasks.init import get_shared_keys, set_shared_config_values
from regscale.airflow.tasks.click import execute_click_command
from regscale.airflow.hierarchy import AIRFLOW_CLICK_OPERATORS as OPERATORS


def setup_task_group(
    dag: DAG,
):
    """Create a TaskGroup for setting up the init.yaml and initialization of the DAG
    :param DAG dag: an Airflow DAG
    """
    setup_tag = str(uuid4()[:8])
    with TaskGroup("setup", dag=dag) as setup:
        init_yaml = PythonOperator(
            task_id=f"initialize_init_yaml-{setup_tag}",
            task_group=setup,
            python_callable=execute_click_command,
            op_kwargs={"command": OPERATORS["init"]["command"], "skip_prompts": True},
            provide_context=True,
            dag=dag,
        )
        shared_keys_task = PythonOperator(
            task_id=f"get_shared_keys-{setup_tag}",
            task_group=setup,
            python_callable=get_shared_keys,
            provide_context=True,
            dag=dag,
        )
        config_task = PythonOperator(
            task_id=f"set_config-{setup_tag}",
            task_group=setup,
            python_callable=set_shared_config_values,
            provide_context=True,
            dag=dag,
        )

        init_yaml >> shared_keys_task >> config_task

    return setup
