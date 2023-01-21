from importlib import import_module
from typing import List

from .command import Command, CommandHandler
from .error import CommandCoachError
from .plugin import Plugins, CommandCoachPlugin


def _instantiate_handler(command: Command):
    command_class_name = command.__class__.__name__
    module = import_module(command.__module__)

    handler_class = getattr(module, f'{command_class_name}Handler')
    if not issubclass(handler_class, CommandHandler):
        raise CommandCoachError('Command Handler must inherit directly from <CommandHandler>')

    return handler_class()


class CommandCoach:
    def __init__(self, plugins: List[CommandCoachPlugin]):
        self._plugins_collection = plugins

    async def handle(self, command: Command) -> None:
        plugins = Plugins(self._plugins_collection)

        if not isinstance(command, Command):
            raise CommandCoachError('Every command must be a child of <Command> class')

        handler = _instantiate_handler(command)

        await plugins.before(command)

        try:
            await handler.handle(command)
        except BaseException as e:
            await plugins.failure()
            raise e

        await plugins.after(command)


def command_bus_maker(plugins: List[CommandCoachPlugin]) -> CommandCoach:
    return CommandCoach(plugins)
