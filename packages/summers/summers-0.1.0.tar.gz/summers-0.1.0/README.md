# Summers

Summers 是一款 python 语言的依赖注入框架, 主要参考了 java spring 框架进行设计和实现. 它很好地解决了 python 语言面向接口/抽象编程, 便捷地实现解耦.

框架的主要组成:

- Summers: 依赖注入, 主要技术有: 反射, 装饰器, 单例, 动态导入等
- Parser: 扫描解析器, 主要技术有: 正则表达式
- CleanArch: 整洁架构校验器

## 1.快速入门

### 1.1 配置注解/装饰器

注解是基于整洁架构分层风格来命名的, 主要包括:

- 资源类型:
  - Business: 业务组件(domain: 领域对象, 值对象, 聚合根)
  - Service: 资源库接口(domain: repository 接口)
  - Repository: 资源库实现类(infra: repository 实现类)
  - Application: 应用服务(app: 应用层服务)
  - Controller: 控制器(view)
- 对象类型:
  - singleton: 声明为单例
- 依赖声明:
  - injection: 执行注入

注意: 目前应用对多的依赖关系为聚合关系, 因此该框架目前只支持对类进行注解, 不支持对函数进行注解.

1.接口定义

```python
class RepoRepository(ABC):
    @abstractmethod
    def get(self):
        pass


class BookRepository(ABC):
    @abstractmethod
    def get(self):
        pass
```

2.基础资源定义

引用注解/装饰器, 只需通过 `@DI.xxxx` 即可, 为了被其它类能够快捷注入, 声明资源类型须应定义别名 name, 即这个类的简称.

```python
@DI.Repository(name='gitlabRepoImpl')
class GitlabRepoImpl(RepoRepository):
    """
    gitlab 仓库实现类
    """
    def get(self):
        print('Gitlab Repo', self.__class__)


@DI.Repository(name='mavenRepoImpl')
class MavenRepoImpl(Repo):
    """
    maven 仓库实现类
    """
    def get(self):
        print('Maven Repo', self.__class__)
```

3.依赖关系定义

```python
# BookRepositoryImpl 依赖于别名为 [mavenRepoImpl, gitlabRepoImpl] 的实现类, 且建议通过接口来接收这个实现类实例
@DI.Repository(name='bookRepositoryImpl')
@DI.inject(mvn_repo="mavenRepoImpl", git_repo="gitlabRepoImpl")
class BookRepositoryImpl(BookRepository):
    mvn_repo: Repo = None
    git_repo: Repo = None

    def get(self):
        self.mvn_repo.get()
        self.git_repo.get()

        objs = Book.objects.all()
        jsons = BookSerializer(objs, many=True)

        return jsons
```

### 1.2 配置及启动主程序

#### 1.2.1 普通应用程序

可以直接 new 具体的实现类获取该实例, 框架也会自动注入依赖的对象, 但不建议这么用, 这违反了解耦的初衷.

```python
# 依赖注入
from summers.di import DI
from book.infra.repository.repository0 import GitlabRepoImpl

DI.scan('./book')

# 通过手工 new 方式
repo_svc = GitlabRepoImpl()
repo_svc.get()
```

#### 1.2.2 django 框架

在主程序启动前, 加入 Summers 扫描解析器. 以下为 django3.x 实例, 配置 manage.py

```python
if __name__ == '__main__':
  # 依赖注入 --> 改为 django 自定义插件/中间件
  from summers.di import DI

  DI.scan('./book', exclude=__file__, reload=False)

  main()
```

随后正常启动应用程序即可, Summers 会主动扫描工程, 解析所有匹配的注解, 根据类的别名进行对象实例化和注入.

## 2.框架扩展

### 2.1 资源类型

框架默认的资源类型遵循整洁架构标准, 可自行修改 Summers 中的装饰器接口定义及实现类.

### 2.2 扫描解析器

框架提供两种扫描解析器, 分别为文本扫解析器(默认), 包导入解析器, 可自行扩展 Parser 实现类.

### 2.3 整洁架构

框架默认支持整洁架构框架校验, 基于其分层命名及依赖关系, 判断其是否符合整洁架构要求, 可自行扩展 CleanArch 实现类.
