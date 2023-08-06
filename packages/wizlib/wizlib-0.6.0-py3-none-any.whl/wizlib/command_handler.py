from argparse import ArgumentParser
import sys
from dataclasses import dataclass

from wizlib.class_family import ClassFamily
from wizlib.super_wrapper import SuperWrapper


class CommandHandler:
    """Handle commands from a ClassFamily"""

    def __init__(self, atriarch):
        """Pass in the command base class, the atriarch of a
        classfamily that meeting the CommandHandler spec"""
        self.parser = ArgumentParser(prog=atriarch.app_name)
        subparsers = self.parser.add_subparsers(dest='command')
        for command in atriarch.family_members('name'):
            key = command.get_member_attr('key')
            aliases = [key] if key else []
            subparser = subparsers.add_parser(command.name, aliases=aliases)
            command.add_arg_spec(subparser)
        self.atriarch = atriarch

    def handle(self, args=None):
        args = args if args else [self.atriarch.default]
        values = vars(self.parser.parse_args(args))
        command = values.pop('command')
        command_class = self.atriarch.family_member('name', command)
        if not command_class:
            raise Exception(f"Unknown command {command}")
        command = command_class(**values)
        result = command.execute()
        return result, command.status

    @classmethod
    def shell(cls, atriarch):
        """Call this from a shell/main entrypoint"""
        result, status = cls(atriarch).handle(sys.argv[1:])
        if result:
            print(result)
        if status:
            print(status)


@dataclass
class Atriarch(ClassFamily, SuperWrapper):

    status = ''

    @classmethod
    def add_arg_spec(self, parser):
        """Add arguments to the command's parser - override this.
        Add global arguments in the base class."""
        pass

    def handle_args(self):
        """Clean up args, calculate any, ask through UI, etc. - override
        this"""
        pass

    def execute(self, method, *args, **kwargs):
        """Actually perform the command - override and wrap this via
        SuperWrapper"""
        self.handle_args()
        result = method(self, *args, **kwargs)
        return result
