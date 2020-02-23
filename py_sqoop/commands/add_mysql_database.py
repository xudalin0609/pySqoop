from py_sqoop import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        pass

    def run_from_argv(self, argv):
        print("run_from_argv")