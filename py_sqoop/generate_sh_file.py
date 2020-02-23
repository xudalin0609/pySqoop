from py_sqoop.manage import rootPath
import argparse
from py_sqoop.models import BaseModel
import os


class GenerateShFile:
    def __init__(self):
        self.header = "sqoop"

    def add_parser(self):
        # TODO
        # 参数选项优化,添加文件参数，可选参数等
        parser = argparse.ArgumentParser()
        parser.add_argument("import_export", choices=["import", "export"], help="import to hive")
        parser.add_argument("--connect", help="mysql URI what you want to connect", required=True)
        parser.add_argument("--username", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--table", required=True)
        parser.add_argument("--fields-terminated-by", default=",")
        parser.add_argument("--update-key", required=True)
        parser.add_argument("--export-dir", required=True)
        parser.add_argument("--update-mode", default="allowinsert")
        return parser

    def generate_sh_file(self):
        args = self.add_parser().parse_args()
        args = BaseModel(args).command_line
        with open(os.path.join(os.path.dirname(os.getcwd()), "sh", "{}_{}.sh".format(args['import_export'], args["--table"])), "w+") as f:
            s = ""
            s += args.pop("sqoop") + " "
            s += args.pop("import_export") + " "
            for k, v in args.items():
                s += "{} {} ".format(k, v)
            f.write(s)

    def run(self):
        self.generate_sh_file()


def main():
    GenerateShFile().run()
