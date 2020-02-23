import sys
import os
from py_sqoop.base import CommandParser, handle_default_options
import pkgutil
from importlib import import_module


def find_commands(core_dir):
    commands_dir = os.path.join(core_dir, "commands")
    return [name for _, name, is_pkg in pkgutil.iter_modules([commands_dir])
            if not is_pkg and not name.startswith('_')]


def get_commands():
    commands = {name: 'py_sqoop' for name in find_commands(os.path.dirname(__file__))}
    return commands


def load_command_class(app_name, name):
    module = import_module("%s.commands.%s" % (app_name, name))
    return module.Command()


class ManagementUtility:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__":
            self.prog = "python sqoop"

    def fetch_command(self, subcommand):
        commands = get_commands()
        print(commands)
        app_name = commands[subcommand]
        klass = load_command_class(app_name, subcommand)
        return klass

    def execute(self):
        try:
            sub_command = self.argv[1]
        except IndexError:
            print("to add the information of the index error")
            return
        parser = CommandParser()
        parser.add_argument("--pythonpath")
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except Exception:
            pass
        self.fetch_command(sub_command).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    utility = ManagementUtility(argv)
    utility.execute()