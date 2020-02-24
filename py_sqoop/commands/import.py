from py_sqoop import TransCommand


class Command(TransCommand):

    def run_from_argv(self, argv):
        self.create_parser()
        super().handle(argv)
