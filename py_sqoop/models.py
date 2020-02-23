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
        self.command_line['import_export'] = paras.pop('import_export')
        for k, i in paras.items():
            self.command_line[self.__add_line(k)] = i

    @property
    def command(self):
        return self.command_line