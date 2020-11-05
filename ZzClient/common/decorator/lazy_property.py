from functools import total_ordering, wraps

class Promise:
    """
    应答类
    在lazy函数的闭包中创建的代理类的基类。
    它用于识别代码中的应答。
    """

    def __cast(self):
        pass

# noinspection PyArgumentList,PyCallingNonCallable
def _lazy_proxy_unpickle(func, args, kwargs, *result_classes):
    return Lazy(func, *result_classes)(*args, **kwargs)


def lazy(func, *result_classes):
    """
    将任何可调用项转换为延迟加载的可调用项。结果类或类型
    是必需的——至少需要一个，以便自动强制
    延迟计算代码被触发。如果结果不存在则初始化
    """

    @total_ordering
    class Proxy(Promise):
        """
        封装函数调用并充当方法的代理
        调用该函数的结果。函数没有求值
        直到结果上的一个方法被调用。
        """
        __prepared = False

        def __init__(self, args, kw):
            self.__args = args
            self.__kw = kw
            if not self.__prepared:
                self.__prepare_class__()
            self.__prepared = True

        def __reduce__(self):
            return (
                _lazy_proxy_unpickle,
                (func, self.__args, self.__kw) + result_classes
            )

        def __repr__(self):
            return repr(self.__cast())

        @classmethod
        def __prepare_class__(cls):
            for resultclass in result_classes:
                for type_ in resultclass.mro():
                    for method_name in type_.__dict__:
                        # 所有 __promise__ 返回相同的包装器方法
                        if hasattr(cls, method_name):
                            continue
                        math = cls.__promise__(method_name)
                        setattr(cls, method_name, math)
            cls._delegate_bytes = bytes in result_classes
            cls._delegate_text = str in result_classes
            if not (cls._delegate_bytes and cls._delegate_text):
                raise TypeError("不能同时使用字节和文本返回类型调用lazy()")
            if cls._delegate_text:
                cls.__str__ = cls.__text_cast
            elif cls._delegate_bytes:
                cls.__bytes__ = cls.__bytes_cast

        @classmethod
        def __promise__(cls, method_name):
            def __wrapper(self, *args, **kw):
                res = func(*self.__args, **self.__kw)
                return getattr(res, method_name)(*args, **kw)

            return __wrapper

        def __text_cast(self):
            return func(*self.__args, **self.__kw)

        def __bytes_cast(self):
            return bytes(func(*self.__args, **self.__kw))

        def __bytes_cast_encoded(self):
            return func(*self.__args, **self.__kw).encode()

        def __cast(self):
            if self._delegate_bytes:
                return self.__bytes_cast()
            elif self._delegate_text:
                return self.__text_cast()
            else:
                return func(*self.__args, **self.__kw)

        def __str__(self):
            return str(self.__cast())

        def __eq__(self, other: Promise):
            if isinstance(other, Promise):
                # noinspection PyUnresolvedReferences
                other = other.__cast()
            return self.__cast() == other

        def __lt__(self, other: Promise):
            if isinstance(other, Promise):
                # noinspection PyUnresolvedReferences
                other = other.__cast()
            return self.__cast() < other

        def __hash__(self):
            return hash(self.__cast())

        def __mod__(self, rhs):
            if self._delegate_text:
                return str(self) % rhs
            return self.__cast() % rhs

        def __deepcopy__(self, memo):
            # 该类的实例实际上是不可变的。它只是一个函数集合。
            memo[id(self)] = self
            return self

    @wraps(func)
    def __wrapper__(*args, **kw):
        # 创建代理对象
        return Proxy(args, kw)

    return __wrapper__


class Lazy:
    """
    lazy 加载装饰器
    此方法不允许被嵌套使用:
    @Lazy
    def test_function():
        do something
    """
    def __init__(self, fun):
        self.fun = fun

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.fun(instance)
        setattr(instance, self.fun.__name__, value)
        return value
