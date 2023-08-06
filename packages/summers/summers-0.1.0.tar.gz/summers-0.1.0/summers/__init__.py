"""
框架整体定义(接口), 主要组成:
- Summers: 依赖注入
- Parser: 扫描解析器
- CleanArch: 整洁架构校验器

# 遵循整洁架构风格的依赖注入框架核心
1.面向接口/抽象编程
  - 定义接口及实现类[y]
  - 通过接口接收实现类实例[y]
2.Ioc 容器: 负责创建和管理所有的对象
  - 单例[y] // TODO 默认为单例
  - 资源唯一性校验 // TODO
3.对象类型定义:
  - Business: 业务组件(domain: 领域对象, 值对象, 聚合根)
  - Service: 资源库接口(domain: repository 接口)
  - Repository: 资源库实现类(infra: repository 实现类)
  - Application: 应用服务(app: 应用层服务)
  - Controller: 控制器(view)
3.依赖注入:
  - 注入方式:
    - 类加载注入[y]
    - 注解隐式装配[y]
    - 构造器注入[x]
    - 属性注入[x]
    - setter 注入[x]
  - 依赖解析: 解析类定义中的依赖关系
    - 解析方式
      - 文本解析[y]
      - 模块导入解析[y]
    - 配置方式
      - 注解方式[y]
      - 配置文件[y]
4.生命周期管理:
  - 创建[y]
  - 初始化[y]
  - 销毁[x] // TODO
5.框架检验:
  - 整洁架构依赖关系校验[x] // TODO
  - 整洁架构可视化[x] // TODO
"""
from abc import ABC, abstractmethod


class Summers(ABC):
    """
    依赖注入
    """

    @abstractmethod
    def Business(*args, **kwargs):
        """
        业务组件(domain: 领域对象, 值对象, 聚合根)
        """
        pass

    @abstractmethod
    def Service(*args, **kwargs):
        """
        资源库接口(domain: repository 接口)
        """
        pass

    @abstractmethod
    def Repository(*args, **kwargs):
        """
        资源库(infra: repository 实现类)
        """
        pass

    @abstractmethod
    def Application(*args, **kwargs):
        """
        应用服务(app: 应用层服务)
        """
        pass

    @abstractmethod
    def Controller(cls):
        """
        控制器(view)
        """
        pass

    @abstractmethod
    def singleton(cls):
        """
        单例
        """
        pass

    @abstractmethod
    def scan(path: str, **kwargs):
        """
        注解扫描
        """
        pass

    @abstractmethod
    def instantiate(class_name: str, *args, **kwargs):
        """
        获取实例
        """
        pass

    @abstractmethod
    def inject(*args, **kwargs):
        """
        对象注入
        """
        pass

    @abstractmethod
    def destroy(*args, **kwargs):
        """
        销毁资源
        """
        pass


class Parser(ABC):
    """
    解析器, 主要分为两种:
    - 文本解析器(通用, 默认方式)
    - 模块导入解析器(对启动器有依赖, 部分场景不适用, 如: django3.x 及以上版本)
    """

    @abstractmethod
    def get_annotation(dir_path, **kwargs):
        pass


class CleanArch(ABC):
    """
    整洁架构
    """

    @abstractmethod
    def dependencies(*args, **kwargs):
        """
        获取依赖关系信息, JSON 格式
        """
        pass

    @abstractmethod
    def validate(*args, **kwargs):
        """
        整洁架构框风格依赖关系校验
        """
        pass
