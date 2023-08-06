"""Provide mixins for click models."""
import logging
from uuid import uuid4
from airflow.operators.python import PythonOperator

from regscale.models.click_models import ClickGroup, ClickCommand
from regscale.airflow.tasks.click import execute_click_command


class AirflowOperatorMixin:
    """Mixin to the ClickGroup to flatten for an Airflow Operator"""

    def flatten_operator(self):
        """Flatten the group to a dictionary of PythonOperator objects"""
        operators_ = {}

        def _flatten_operator(group_, prefix=""):
            for name, cmd in group_.commands.items():
                if isinstance(cmd, ClickCommand):
                    cmd_name = cmd.name if prefix == "" else f"{prefix}__{cmd.name}"
                    logging.info(f"{cmd_name=}")

                    def _make_operator_wrapper(
                        cmd_name, cmd: ClickCommand, **kwargs
                    ) -> PythonOperator:
                        """Create a wrapper to make a python operator."""
                        op_kwargs = None
                        logging.info(f"{cmd_name=}")
                        if "op_kwargs" in kwargs:
                            op_kwargs = kwargs.pop("op_kwargs")
                        inputs = dict(
                            task_id=f"{cmd_name}_{str(uuid4())}",
                            python_callable=execute_click_command,
                            provide_context=True,
                        )
                        if kwargs:
                            inputs |= kwargs
                        if op_kwargs:
                            inputs |= {"op_kwargs": {"command": cmd, **op_kwargs}}
                        else:
                            inputs |= {"op_kwargs": {"command": cmd}}
                        return PythonOperator(**inputs)

                    def _lambda_wrapper(**kwargs):
                        return _make_operator_wrapper(
                            cmd_name=cmd_name, cmd=cmd, **kwargs
                        )

                    operators_[cmd_name] = {
                        "operator": PythonOperator(
                            task_id=cmd_name,
                            python_callable=execute_click_command,
                            provide_context=True,
                            op_kwargs={"command": cmd},
                        ),
                        "lambda": lambda **kwargs: _lambda_wrapper(**kwargs),
                        "command": cmd,
                    }
                elif isinstance(cmd, ClickGroup):
                    new_prefix = (
                        f"{prefix}__{cmd.group_name}" if prefix else cmd.group_name
                    )
                    _flatten_operator(cmd, new_prefix)

        _flatten_operator(self)
        return operators_


class AirflowClickGroup(AirflowOperatorMixin, ClickGroup):
    """Initialize the AirflowClickGroup object."""


if __name__ == "__main__":
    from regscale.regscale import cli

    group = AirflowClickGroup.from_group(cli, prefix="regscale")
    operators = group.flatten_operator()
    print(operators)
