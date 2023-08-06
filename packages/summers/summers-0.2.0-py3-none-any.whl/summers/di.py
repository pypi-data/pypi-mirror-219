"""
依赖注入框架 Summers 具体实现
"""
import importlib

from summers import Summers
from summers.sc_txt import AnnoParser


class DI(Summers):
    """
    依赖注入框架实现类

    # 基本用法
    - 资源类型:
      - @DI.Business(name="类别名")
      - @DI.Service(name="类别名")
      - @DI.Repository(name="类别名")
      - @DI.Application(name="类别名")
      - @DI.Controller(name="类别名")
    - 对象类型:
      - @DI.singleton
    - 依@DI.赖声明:
      - @DI.injection(成员1="类别名a", 成员2="类别名b" ...)
    """
    cls_factory = {}  # 资源工厂
    obj_factory = {}  # 对象工厂
    is_singleton = True  # TODO 默认为单例模式

    @staticmethod
    def Business(*args, **kwargs):

        def wrapper(cls):

            for key in kwargs:
                obj_name = kwargs['name']
                full_name = str(cls)
                class_name = full_name[8: len(full_name) - 2]
                if obj_name not in DI.cls_factory:
                    DI.cls_factory[obj_name] = class_name

            return cls

        return wrapper

    @staticmethod
    def Service(*args, **kwargs):
        return DI.Business(*args, **kwargs)

    @staticmethod
    def Repository(*args, **kwargs):
        return DI.Business(*args, **kwargs)

    @staticmethod
    def Application(*args, **kwargs):
        return DI.Business(*args, **kwargs)

    @staticmethod
    def Controller(cls):
        return cls

    @staticmethod
    def singleton(cls):
        """
        单例
        """
        instances = DI.obj_factory

        def wrapper(*args, **kwwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwwargs)

            return instances[cls]

        return wrapper

    @staticmethod
    def instantiate(class_name: str, *args, **kwargs):
        """
        获取实例
        """
        idx = class_name.rfind('.')
        m_name = class_name[0: idx]
        c_name = class_name[idx + 1:]
        obj = None
        try:
            # module_meta = __import__(m_name, globals(), locals(), [c_name])
            module_meta = importlib.import_module(m_name)
            class_meta = getattr(module_meta, c_name)
            obj = class_meta(*args, **kwargs)
            DI.obj_factory[class_name] = obj
        except Exception as err:
            print("实例化_ERR", err)

        return obj

    @staticmethod
    def inject(*args, **kwargs):
        """
        对象注入
        """

        def wrapper(cls):
            print("对象注入", cls)
            for key in kwargs:
                obj_name = kwargs[key]
                try:
                    # class_name = DI.cls_factory[obj_name]
                    class_name = DI.di_conf[obj_name]['class']
                    setattr(cls, key, DI.instantiate(class_name))
                except Exception as err:
                    print("注入_ERR", err, cls)
                    pass

            return cls

        return wrapper

    @staticmethod
    def scan(path: str, **kwargs):
        """
        注解扫描
        """
        # LoadParser.get_conf(path, **kwargs)
        # 读取工程配置
        DI.di_conf = AnnoParser.get_annotation(path)

    @staticmethod
    def destroy(*args, **kwargs):
        """
        销毁资源 TODO
        """
        pass
