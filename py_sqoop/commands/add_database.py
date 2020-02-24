from py_sqoop import DataBaseCommand


class Command(DataBaseCommand):

    def run_from_argv(self, argv):
        self.create_parser()
        super().handle(argv)