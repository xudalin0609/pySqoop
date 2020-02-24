import argparse
import os, sys
import json
from py_sqoop.function_tools import dict_merge


class BaseCommand:

    def create_parser(self):
        self.parser = argparse.ArgumentParser()


class TransCommand(BaseCommand):

    def add_parser(self):
        # TODO
        # 参数选项优化,添加文件参数，可选参数等,将sqoop参数变为不定参数

        self.create_parser()
        self.parser.add_argument("action", choices=["import", "export"], help="import to hive")
        self.parser.add_argument("--db-name", help="database you want to connect", required=True)
        self.parser.add_argument("--table", required=True)
        self.parser.add_argument("--fields-terminated-by", default=",")
        self.parser.add_argument("--update-key", required=True)
        self.parser.add_argument("--export-dir")
        self.parser.add_argument("--target-dir")
        self.parser.add_argument("--update-mode", default="allowinsert")

    def generate_sh_file(self, argv):
        args = self.parser.parse_args(argv[1:])
        args = BaseModel(args).command_line
        with open(os.path.join(os.path.dirname(os.getcwd()), "sh", "{}_{}.sh".format(args['action'], args["--table"])),
                  "w+") as f:
            s = ""
            s += args.pop("sqoop") + " "
            s += args.pop("action") + " "
            for k, v in args.items():
                s += "{} {} ".format(k, v)
            f.write(s)
            print("generate sh file success")

    def handle(self, argv):
        self.add_parser()
        self.generate_sh_file(argv)


# TODO
# BaseModel will be deleted,merge to TransCommand class
class BaseModel:

    def __init__(self, paras):
        self.command_line = dict()
        self.command_line['sqoop'] = "sqoop"
        self.analyse_para(paras)

    def analyse_para(self, paras):
        self.import_module(paras)

    def __add_line(self, para):
        return "--" + para

    def import_module(self, paras):
        paras = vars(paras)
        self.command_line['action'] = paras.pop('action')
        db_name = paras.pop('db_name')
        with open(os.path.join(os.path.dirname(os.getcwd()), "databases", "%s.json" % (db_name)), 'r') as f:
            t = json.load(f)

        paras = dict_merge(paras, t)

        for k, i in paras.items():
            if k == "fields_terminated_by":
                i = '"%s"' % i
            self.command_line[self.__add_line(k)] = i

    @property
    def command(self):
        return self.command_line


class DataBaseCommand(BaseCommand):

    def add_parser(self):
        self.parser.add_argument("--db-name", required=True)
        self.parser.add_argument("--db-url", required=True)
        self.parser.add_argument("--password", required=True)

    def save(self, argv):
        args, option = self.parser.parse_known_args(argv[1:])
        tmp_dic = {}
        for k, v in vars(args).items():
            tmp_dic[k] = v
        save_path = os.path.join(os.path.dirname(os.getcwd()), "databases", "%s.json" % (tmp_dic['db_name']))
        with open(save_path, 'w') as f:
            json.dump(tmp_dic, f)

    def handle(self, argv):
        self.add_parser()
        self.save(argv)
