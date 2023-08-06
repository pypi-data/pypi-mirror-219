import sys
from os import walk, path
from importlib import import_module, reload

from summers.sc_txt import Parser


class LoadParser(Parser):
    """
    注解解析器 (模块导入方式, 不适用于 django3.x 及以上版本)
    """

    @staticmethod
    def get_annotation(dir_path, **kwargs):
        """
        扫描工程/模块, 动态载入并获取注解信息
        TODO 扫描范围
        """
        for root, dirs, files in walk(dir_path):
            if '.vscode' not in root and '__' not in root and 'migrations' not in root:
                for file in files:
                    if '.py' in file and 'manage.py' not in file:
                        file_path = path.join(root, file)
                        file_name = file_path[2: len(file_path)-3].replace('/', '.')

                        # 动态载入模块获取注解信息
                        if file_name + '.py': # not in kwargs['exclude']:
                            print("文件1", file_name)
                            try:
                                # m = import_module(file_name)
                                # print("模块2", m)
                                # print("导入3", sys.modules[file_name])
                                # del sys.modules[file_name]
                                if kwargs['reload']:
                                    m = import_module(file_name)
                                    # print("模块2", m)
                                    # print("导入3", sys.modules[file_name])
                                else:
                                    m = import_module(file_name)
                                    # print("模块2", m)
                                    # print("导入3", sys.modules[file_name])
                                    del sys.modules[file_name]
                            except Exception as err:
                                print("载入_ERR", err)
                                reload(file_name)
