from abc import ABC, abstractmethod
from typing import List

from .command import Command


class CommandCoachPlugin(ABC):
    @abstractmethod
    async def before_handle(self, command: Command):
        pass

    @abstractmethod
    async def handle_failed(self):
        pass

    @abstractmethod
    async def after_handle(self, command: Command):
        pass


class Plugins:
    def __init__(self, found: List[CommandCoachPlugin]):
        self.found = found

    async def before(self, command: Command):
        for m in self.found:
            await m.before_handle(command)

    async def failure(self):
        for m in self.found:
            await m.handle_failed()

    async def after(self, command: Command):
        reversed_found = list(reversed(self.found))
        for m in reversed_found:
            await m.after_handle(command)
