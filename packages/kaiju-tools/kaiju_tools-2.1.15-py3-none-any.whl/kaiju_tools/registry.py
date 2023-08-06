"""Class and object registries."""

import abc
import inspect
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import (
    Any,
    Type,
    TypeVar,
    Generic,
    ClassVar,
    Callable,
    Collection,
    Generator,
    Iterable,
    Hashable,
    Union,
    Optional,
    Tuple,
    FrozenSet,
)

__all__ = ['RegistryError', 'RegistrationFailed', 'Registry', 'ClassRegistry', 'ObjectRegistry', 'FunctionRegistry']

_Key = TypeVar('_Key', bound=Hashable)
_Obj = TypeVar('_Obj')
_Default = TypeVar('_Default')


class RegistryError(Exception):
    """A base class for all registry errors."""


class RegistrationFailed(ValueError, RegistryError):
    """Object cannot be registered in this registry."""


@dataclass
class Registry(Mapping, Generic[_Key, _Obj], abc.ABC):
    """A base registry class.

    You may use it to store some arbitrary data.
    It's recommended to use any of its derived classes if possible:
    `ObjectRegistry`, `FunctionRegistry` or `ClassRegistry`.
    """

    objects: dict = field(default_factory=dict)
    raise_if_exists: bool = False

    def can_register(self, obj) -> bool:
        """Check if an object can be registered."""
        try:
            self._validate_object(obj)
        except RegistrationFailed:
            return False
        else:
            return True

    def register(self, obj: _Obj, name: _Key = None) -> _Key:
        """Register an object in the registry and return a key under which it has been registered.

        :param obj: object to register
        :param name: provide a custom name (not recommended)
        :raises RegistrationFailed: if an object can't be registered
        :returns: object key in the registry
        """
        key = self._validate_object(obj)
        if name:
            key = name
        self.objects[key] = obj
        return key

    def register_many(self, obj: Collection[_Obj]) -> Tuple[_Key, ...]:
        """Register multiple objects at once.

        :param obj: objects
        :raises RegistrationFailed: if any of the objects can't be registered
        :returns: a tuple of object keys
        """
        return tuple(self.register(item) for item in obj)

    def get_key(self, obj: _Obj) -> _Key:
        """Get a key by which an object will be referenced in the registry."""
        raise NotImplementedError()

    def register_from_namespace(self, namespace: Mapping, *, ignore_key_names: bool = True) -> FrozenSet[_Key]:
        """Register all supported objects from an arbitrary mapping.

        Incompatible objects will be ignored. Returns a set of registered keys.

        :param namespace: any mapping
        :param ignore_key_names: set it to True to ignore namespace keys when settings object names
        :returns: a set of registered keys
        """
        keys = set()
        for key, obj in namespace.items():
            if ignore_key_names:
                key = None
            try:
                key = self.register(obj, name=key)
            except RegistrationFailed:
                pass
            else:
                keys.add(key)
        return frozenset(keys)

    def register_from_module(self, module: object, *, ignore_key_names: bool = True) -> FrozenSet[_Key]:
        """Register classes from current object.

        :param module: any object with `__dict__`
        :param ignore_key_names: set it to True to ignore namespace keys when settings object names
        :returns: a set of registered keys
        """
        return self.register_from_namespace(module.__dict__, ignore_key_names=ignore_key_names)

    def find_all(self, condition: Callable[[Any], bool]) -> Generator[_Obj, None, None]:
        """Find all objects matching a condition."""
        for value in self.objects.values():
            if condition(value):
                yield value

    def find(self, condition: Callable[[Any], bool]) -> _Obj:
        """Find an object matching a condition."""
        return next(self.find_all(condition), None)

    def clear(self) -> None:
        """Unlink all registered objects. Use it with caution."""
        self.objects.clear()

    def __enter__(self):
        """Enter the context."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clear all registered objects on exit."""
        self.clear()

    def __contains__(self, item: _Key) -> bool:
        return item in self.objects

    def __getitem__(self, item: _Key) -> _Obj:
        return self.objects[item]

    def __delitem__(self, item: _Key) -> None:
        del self.objects[item]

    def __iter__(self) -> Iterable[_Key]:
        return iter(self.objects.keys())

    def __len__(self) -> int:
        return len(self.objects)

    def get(self, key: _Key, default: _Default = None) -> Union[_Obj, _Default]:
        try:
            return self[key]
        except KeyError:
            return default

    def _validate_object(self, obj) -> _Key:
        """Validate object before registration."""
        key = self.get_key(obj)
        if key in self.objects and self.raise_if_exists:
            raise RegistrationFailed(f'Object with the same name already present: {key}')
        return key


@dataclass
class ClassRegistry(Registry, Generic[_Key, _Obj], abc.ABC):
    """A default registry for classes.

    It can be used to register a set of classes for example for dynamic object initialization
    based on class names.

    Register a class:

    >>> class NotBase:
    ...     ...
    >>> class Base:
    ...     ...
    >>> class C(Base):
    ...     x = 1
    ...     def __init__(self, y):
    ...         self.y = y
    >>> class Reg(ClassRegistry):
    ...     @classmethod
    ...     def get_base_classes(cls):
    ...         return Base,
    >>> reg = Reg()
    >>> reg.register(C)
    'C'

    >>> reg.register(42)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    registry.RegistrationFailed:

    >>> reg.register(NotBase) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    registry.RegistrationFailed:

    Register from another class or module:

    >>> class D(Base):
    ...     x = 2
    >>> class Module:
    ...     D = D
    >>> reg.register_from_module(Module)
    frozenset({'D'})

    Mapping features:

    >>> 'D' in reg
    True
    >>> reg['C'].x
    1
    >>> dict(reg)['C'].__name__
    'C'

    Conditional get:

    >>> reg.find(condition=lambda x: x.__name__ == 'C').__name__
    'C'

    Special method — finding a subclass:

    >>> reg.find_subclass(Base).__name__
    'C'
    >>> len(list(reg.find_subclasses(Base)))
    2

    Example - dynamic object construction from a data dict.

    >>> o = {'cls': 'C', 'data': {'y': 10}}
    >>> o = reg[o['cls']](**o['data'])
    >>> o.x + o.y
    11

    """

    allow_abstract: ClassVar[bool] = False

    @classmethod
    @abc.abstractmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        ...

    def find_subclasses(self, bases: Union[Collection[_Obj], _Obj]) -> Generator[_Obj, None, None]:
        """Find all subclasses matching bases. A shortcut to `find_all` method."""
        return self.find_all(condition=lambda x: issubclass(x, bases))

    def find_subclass(self, bases: Union[Collection[_Obj], _Obj]) -> _Obj:
        """Find a first subclass matching bases. A shortcut to `find` method."""
        return next(self.find_subclasses(bases), None)

    def get_key(self, obj: _Obj) -> _Key:
        """Get a class name."""
        return getattr(obj, '__name__', str(obj))

    def _validate_object(self, obj) -> _Key:
        if not inspect.isclass(obj):
            raise RegistrationFailed(f'Can\'t register object {obj} because it\'s not a class.')
        elif not self.allow_abstract and (inspect.isabstract(obj) or abc.ABC in obj.__bases__):
            raise RegistrationFailed(f'Can\'t register object {obj} because it\'s an abstract class.')
        elif not issubclass(obj, self.get_base_classes()):
            raise RegistrationFailed(
                f'Can\'t register object {obj} because it\'s not a subclass'
                f' of any of the base classes {self.get_base_classes()}'
            )
        key = Registry._validate_object(self, obj)
        return key


@dataclass
class ObjectRegistry(Registry, Generic[_Key, _Obj], abc.ABC):
    """A default registry for objects.

    It can be used to store specific objects in a single mapping (for example for storing
    application services in a single service registry).

    See `ClassRegistry` for more usage examples.

    >>> class Base:
    ...     ...
    >>> class C(Base):
    ...     x = 1
    ...     def __init__(self, y):
    ...         self.y = y
    >>> o = C(y='TEST')
    >>> class Reg(ObjectRegistry):
    ...     @classmethod
    ...     def get_base_classes(cls):
    ...         return Base,
    >>> reg = Reg()
    >>> reg.register(o)
    'C'

    >>> reg.register(42)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    registry.RegistrationFailed:

    Special method — finding an instance of a class:

    >>> reg.find_instance(Base).y  # noqa
    'TEST'

    """

    @classmethod
    @abc.abstractmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        ...

    def find_instances(self, bases: Union[Collection[Type[_Obj]], Type[_Obj]]) -> Generator[_Obj, None, None]:
        """Find all subclasses matching bases. A shortcut to `find_all` method."""
        return self.find_all(condition=lambda x: isinstance(x, bases))

    def find_instance(self, bases: Union[Collection[Type[_Obj]], Type[_Obj]]) -> Optional[_Obj]:
        """Find a first subclass matching bases. A shortcut to `find` method."""
        return next(self.find_instances(bases), None)

    def get_key(self, obj: _Obj) -> _Key:
        """Get a name by which a registered class will be referenced in the mapping."""
        return getattr(type(obj), '__name__', str(type(obj)))

    def _validate_object(self, obj) -> _Key:
        key = Registry._validate_object(self, obj)
        if not isinstance(obj, self.get_base_classes()):
            raise RegistrationFailed(
                f'Can\'t register object {obj} because it\'s not an instance'
                f' of any of the base classes {self.get_base_classes()}'
            )
        return key


@dataclass
class FunctionRegistry(Registry[str, Callable]):
    """A very simple function registry.

    >>> reg = FunctionRegistry()
    >>> def test():
    ...     return True
    >>> reg.register(test)
    'test'

    >>> reg['test']()
    True

    """

    def call(self, name: _Key, *args, **kws):
        """Call a stored function with arguments."""
        return self[name](*args, **kws)

    def get_key(self, obj: Callable) -> _Key:
        """Get a name by which a registered class will be referenced in the mapping."""
        return obj.__name__

    def _validate_object(self, obj) -> _Key:
        key = Registry._validate_object(self, obj)
        if not callable(obj):
            raise RegistrationFailed(f'Can\'t register object {obj} because it\'s not a function.')
        return key
