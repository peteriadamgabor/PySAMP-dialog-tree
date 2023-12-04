import inspect
from dataclasses import dataclass

import pysamp.commands


@dataclass
class FayCommand(pysamp.commands.Command):
    arg_names: list[str] | None = None
    custom_usage_message: str | None = None

    def __post_init__(self):
        super().__post_init__()
        parameters = list(inspect.signature(self.handler).parameters.values())

        self._usage_message.color = 0xFFFFFFAA

        if self.custom_usage_message is not None:
            self._usage_message.text = self.custom_usage_message
        else:
            self._usage_message.text = ("((" + f'Használat: {list(self.triggers)[0]} ' + ' '.join(
                        (
                            f'[{self.arg_names[index]}]'
                            if self.arg_names is not None and len(self.arg_names) == len(parameters[1:])
                            else f'[{parameter.name}]'
                        )
                        if parameter.default is inspect._empty and parameter.kind != inspect.Parameter.VAR_POSITIONAL
                        else f'<{parameter.name}>'
                        for index, parameter in enumerate(parameters[1:])
                    ) + "))")


_original_cmd = pysamp.commands.cmd


def cmd(*args, arg_names=None, custom_usage_message=None, **kwargs):
    ret = _original_cmd(*args, **kwargs)
    command = pysamp.commands.dispatcher._commands[-1]
    command.arg_names = arg_names
    command.custom_usage_message = custom_usage_message
    return ret


pysamp.commands.Command = FayCommand
pysamp.commands.cmd = cmd
