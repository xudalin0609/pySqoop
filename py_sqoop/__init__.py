import argparse
import os,sys


class BaseCommand:

    def to_add(self):
        pass

    def handle(self):
        pass


class TransCommand(BaseCommand):

    def run_from_argv(self, argv):
        pass

    def add_parser(self):
        # TODO
        # 参数选项优化,添加文件参数，可选参数等
        parser = argparse.ArgumentParser()
        parser.add_argument("action", choices=["import", "export"], help="import to hive")
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
        with open(os.path.join(os.path.dirname(os.getcwd()), "sh", "{}_{}.sh".format(args['action'], args["--table"])), "w+") as f:
            s = ""
            s += args.pop("sqoop") + " "
            s += args.pop("action") + " "
            for k, v in args.items():
                s += "{} {} ".format(k, v)
            f.write(s)

    def run(self):
        self.generate_sh_file()

    def handle(self):
        self.run()


class BaseModel:

    def __init__(self, paras):
        self.command_line = dict()
        self.command_line['sqoop'] = "sqoop"
        self.analyse_para(paras)

    def analyse_para(self, paras):
        self.import_module(paras)

    def __add_line(self, para):
        return "--"+para

    def import_module(self, paras):
        paras = vars(paras)
        self.command_line['action'] = paras.pop('action')
        for k, i in paras.items():
            self.command_line[self.__add_line(k)] = i

    @property
    def command(self):
        return self.command_line