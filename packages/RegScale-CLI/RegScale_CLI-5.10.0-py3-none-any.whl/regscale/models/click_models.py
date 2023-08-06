#!/usr/bin/env python3

"""Click BaseModels."""

from typing import Any, List, Optional, Union, Callable, Tuple, Dict
from pydantic import BaseModel, validator
import inspect
import click.core
import click
import contextlib
from regscale.models.inspect_models import SignatureModel


class ClickOption(BaseModel):
    """A BaseModel based on a click object
    This is the simplest unit in the click hierarchy, representing an option that can be passed to a command.
    """

    name: str
    value: Any = None
    default: Any = None
    option: Optional[Union[click.core.Option, dict]] = None
    type: Optional[str] = None
    help: Optional[str] = None
    prompt: Optional[str] = None
    confirmation_prompt: Optional[bool] = None
    is_flag: Optional[bool] = None
    is_bool_flag: Optional[bool] = None
    count: Optional[int] = None
    allow_from_autoenv: Optional[bool] = None
    expose_value: Optional[bool] = None
    is_eager: Optional[bool] = None
    callback: Optional[Union[str, Any]] = None
    callback_signature: Optional[Any] = None

    class Config:
        extra = "ignore"  # ignore extra fields
        arbitrary_types_allowed = True

    @validator("option")
    def _check_option(cls, var):
        """Check if option is a click.Option or dict"""
        if not isinstance(var, (dict, click.core.Option)):
            raise TypeError("option must be a click.Option or dict")
        return var

    @classmethod
    def from_option(
        cls,
        option: click.core.Option,
        include_callback: bool = True,
        include_option: bool = False,
    ):
        """Build the BaseModel from a click.Option"""
        print(option)
        data = {
            "option": option if include_option else option.__dict__,
            "help": option.help,
            "name": option.name,
            "default": option.default,
            "type": str(option.type),
            "prompt": option.prompt,
            "confirmation_prompt": option.confirmation_prompt,
            "is_flag": option.is_flag,
            "is_bool_flag": option.is_bool_flag,
            "count": option.count,
            "allow_from_autoenv": option.allow_from_autoenv,
            "expose_value": option.expose_value,
            "is_eager": option.is_eager,
            "callback": option.callback
            if include_callback
            else option.callback.__qualname__,
        }
        # get the signature of the callback,
        if option.callback is not None:
            sig = inspect.signature(option.callback)
            data["callback_signature"] = {
                "parameters": [
                    {
                        "name": name,
                        "default": param.default
                        if param.default is not inspect.Parameter.empty
                        else None,
                        "kind": param.kind,
                        "annotation": param.annotation
                        if param.annotation is not inspect.Parameter.empty
                        else None,
                    }
                    for name, param in sig.parameters.items()
                ],
                "return_annotation": sig.return_annotation
                if sig.return_annotation is not inspect.Signature.empty
                else None,
            }
        return cls(**data)

    @property
    def required(self):
        """Make sure it is a required parameter."""
        return self.prompt is False and self.default is None


class ClickCommand(BaseModel):
    name: str
    command: Optional[click.core.Command] = None
    help: Optional[str] = None
    options_metavar: Optional[str] = None
    context_settings: Optional[Any] = None
    params: Dict[str, ClickOption]
    callback: Optional[Union[str, Any]] = None
    signatures: Optional[SignatureModel] = None

    class Config:
        extra = "ignore"  # ignore extra fields
        arbitrary_types_allowed = True

    @validator("command")
    def _check_command(cls, var):
        """Validate a click.Command"""
        if not isinstance(var, (click.Command, click.core.Command)):
            print(f"command must be a click.Command not {type(var)}")
        return var

    @classmethod
    def from_command(
        cls,
        command: click.core.Command,
        include_callback: bool = True,
        include_command: bool = False,
    ):
        """Generate the pydantic class from the click.Command"""
        data = {
            "command": command if include_command else None,
            "name": command.name,
            "help": command.help,
            "options_metavar": command.options_metavar,
            "context_settings": command.context_settings,
            "params": {
                param.name: ClickOption.from_option(param, include_callback)
                for param in command.params
                if isinstance(param, click.Option)
            },
            "signature": SignatureModel.from_callable(
                command=command.name, fn=command.callback
            ),
            "callback": command.callback
            if include_callback
            else command.callback.__qualname__,
        }
        return cls(**data)

    def _execute(self, *args, **kwargs) -> Optional[Any]:
        """Execute the command."""
        if not isinstance(self.callback, Callable):
            raise RuntimeWarning("Callable not configured as callback")
        with contextlib.suppress(SystemExit):
            return self.callback(*args, **kwargs)

    def _validate_params(self, *args, **kwargs) -> Tuple[list, dict]:
        """Validate the params and represent them as a dict of key value pairs"""
        # iterate and get the expected list of params, if they are not Optional
        param_values = []
        param_dict = {}
        for i, param in enumerate(self.params):
            if args and i < len(args):
                # process positional arguments first
                param_values.append(args[i])
            elif kwargs and param in kwargs:
                # process keyword arguments
                param_dict[param] = kwargs[param]
            elif self.params[param].default is not None:
                # use default for param if provided
                param_dict[param] = self.params[param].default
            else:
                raise ValueError(f"Missing required argument {param}")
        return param_values, param_dict

    def call(self, *args, **kwargs):
        """Call the callable for the command."""
        param_values, param_dict = self._validate_params(*args, **kwargs)
        return self._execute(*param_values, **param_dict)

    def return_cli_commands(self):
        """Return a list of all cli_commands independent of hierarchy"""
        cli_commands = []
        for param in self.params:
            if isinstance(param, ClickCommand):
                cli_commands.extend(param.return_cli_commands())
            else:
                cli_commands.append(param)
        return cli_commands

    @property
    def param_defaults(self) -> dict:
        """Return a dictionary with basic defaults for the parameters
        :returns: A dict in the following form:
        >>> {
            "has_default": bool,
            "default": option.default,
            "required": bool,
            "prompt": bool
        }

        for all options required by Click.
        """
        return {
            option.name: {
                "has_default": bool(option.default),
                "default": option.default,
                "required": option.required,
                "prompt": option.prompt,
            }
            for _, option in self.params.items()
        }

    def get_callback_args(self, putative_params: dict):
        """Get the callback arguments from the dag_run configuration.

        :param putative_params: The dag_run configuration and op_kwargs dictionary.
        :return: A dictionary where each key is a parameter name and each value is either the default
                 value of the parameter (if it has one and if the parameter is not present in dag_run_conf),
                 or the value from dag_run_conf.
        """
        callback_args = {}

        if self.callback is not None and self.signatures is not None:
            for _, param in self.signatures.parameters.items():
                param_name = param.name
                param_default = param.default
                if param_name in putative_params:
                    callback_args[param_name] = putative_params[param_name]
                elif param_default is not inspect.Parameter.empty:
                    callback_args[param_name] = param_default

        return callback_args

    @property
    def parameters(self) -> List[str]:
        """Return a list of parameters expected by this command"""
        signatures = self.signatures or []
        params = self.params or []
        return [
            param.name if hasattr(param, "name") else param for param in signatures
        ] + [param.name if hasattr(param, "name") else param for param in params]


class ClickGroup(BaseModel):
    """BaseModel representation of a click Group"""

    name: str
    group_name: str
    # This double-quoted ClickGroup is a forward reference to allow for nested groups
    commands: Dict[str, Union[ClickCommand, "ClickGroup"]]

    class Config:
        extra = "ignore"  # ignore extra fields
        arbitrary_types_allowed = True

    @classmethod
    def from_group(
        cls,
        group: click.Group,
        prefix: Optional[str] = None,
        include_callback: bool = True,
    ):
        """Define a BaseModel based on a click.Group group."""
        prefix = f"{prefix}__{group.name}" if prefix else f"{group.name}"
        data = {
            "name": prefix,
            "group_name": group.name,
            "commands": {},
        }
        for cmd_name, cmd in group.commands.items():
            if not cmd:
                continue
            if isinstance(cmd, click.core.Group):
                data["commands"][cmd.name] = cls.from_group(cmd, include_callback)
            elif isinstance(cmd, click.core.Command):
                data["commands"][cmd.name] = ClickCommand.from_command(
                    cmd, include_callback
                )
        return cls(**data)

    def flatten(self, prefix: str = "") -> dict:
        """Flatten the group to a dictionary of commands."""
        commands = {}

        def _flatten(group_: Union[ClickCommand, "ClickGroup"], prefix_: str = ""):
            for cmd in group_.commands:
                # flake8: noqa: F821
                if isinstance(cmd, ClickCommand):
                    cmd_name = f"{prefix_}__{cmd.name}" if prefix_ else cmd.name
                    commands[cmd_name] = cmd
                elif isinstance(cmd, ClickGroup):
                    new_prefix = (
                        f"{prefix_}__{cmd.group_name}" if prefix_ else cmd.group_name
                    )
                    _flatten(cmd, new_prefix)

        _flatten(self, prefix)
        return commands


if __name__ == "__main__":
    from regscale.regscale import cli

    group = ClickGroup.from_group(cli, prefix="regscale")
    from pprint import pprint

    pprint(group)
