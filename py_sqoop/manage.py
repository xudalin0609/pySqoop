import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

if __name__ == "__main__":
   sys.path.append(rootPath)
   # from py_sqoop.generate_sh_file import main
   from py_sqoop.core import execute_from_command_line
   execute_from_command_line()
