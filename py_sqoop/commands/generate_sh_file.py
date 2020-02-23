from py_sqoop import BaseCommand


class Command(BaseCommand):

    def run_from_argv(self, argv):
        print(argv)
        print("generate_sh_file")