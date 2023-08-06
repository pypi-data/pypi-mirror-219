from unittest import TestCase

from wizlib.command_handler import CommandHandler
from .data_command import Command


class TestCommandSync(TestCase):

    def test_from_handler(self):
        r, s = CommandHandler(Command).handle(['play'])
        self.assertEqual(r, 'Play!')

    def test_default(self):
        r, s = CommandHandler(Command).handle()
        self.assertEqual(r, 'Play!')
