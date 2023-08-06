"""Basic types and constants."""

import uuid
from bisect import bisect
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import (
    Optional,
    Mapping,
    Iterator,
    Sized,
    Iterable,
    Dict,
    cast,
    NewType,
    MutableMapping,
    Tuple,
    Hashable,
    Any,
    FrozenSet,
    TypedDict,
)

from kaiju_tools.encoding import Serializable
from kaiju_tools.functions import not_implemented

__all__ = [
    'SortedStack',
    'RestrictedDict',
    'TTLDict',
    'NSKey',
    'Namespace',
    'Session',
    'Scope',
    'SCOPES',
    'SCOPE_MAP',
    'RequestContext',
]


class SortedStack(Sized, Iterable):
    """A sorted collection (stack) of items.

    >>> stack = SortedStack({'dogs': 12, 'sobaki': 5})
    >>> stack = SortedStack(stack)
    >>> stack.extend(SortedStack({'cats': 5}))

    Selection:

    >>> stack.select(8)
    ['sobaki', 'cats']

    >>> stack.rselect(8)
    ['dogs']

    Insertion and removal:

    >>> stack.insert(1, 'koty')
    >>> stack.pop_many(3)
    ['koty']

    >>> stack.pop()
    'sobaki'

    >>> len(stack)
    2

    >>> stack.clear()
    >>> bool(stack)
    False

    """

    __slots__ = ('_scores', '_values')

    def __init__(self, __items: Iterable = None):
        self._scores = []
        self._values = []
        if __items:
            self.extend(__items)

    def __iter__(self):
        return iter(zip(self._values, self._scores))

    def __len__(self):
        return len(self._values)

    def __delitem__(self, __item):
        del self._scores[__item]
        del self._values[__item]

    @property
    def lowest_score(self):
        """Get the lowest score in the stack."""
        return next(iter(self._scores), None)

    def extend(self, items: Iterable, /):
        """Extend the stack by adding more than one element."""
        if isinstance(items, dict):
            items = items.items()
        for item, score in items:
            self.insert(score, item)

    def insert(self, score, item, /):
        """Insert a single element into the stack."""
        idx = bisect(self._scores, score)
        self._scores.insert(idx, score)
        self._values.insert(idx, item)

    def select(self, score_threshold, /) -> list:
        """Select and return items without removing them from the lowest score to `score_threshold`.

        The values are guaranteed to be in order.
        """
        return self._select(score_threshold, reverse=False)

    def rselect(self, score_threshold, /) -> list:
        """Select and return items without removing them from the highest score to `score_threshold`.

        The values are guaranteed to be in order.
        """
        return self._select(score_threshold, reverse=True)

    def pop(self):
        """Pop a single element which has the lowest score.

        :raises StopIteration: if there are no values to return.
        """
        return self._pop(reverse=False)

    def rpop(self):
        """Pop a single element which has the highest score.

        :raises StopIteration: if there are no values to return.
        """
        return self._pop(reverse=True)

    def pop_many(self, score_threshold, /) -> list:
        """Pop and return values with scores less than `score_threshold`.

        The returned values are guaranteed to be in order.
        Returns an empty list if no values.
        """
        return self._pop_many(score_threshold, reverse=False)

    def rpop_many(self, score_threshold, /) -> list:
        """Pop and return values with scores greater than `score_threshold`.

        Returned values are guaranteed to be in order.
        """
        return self._pop_many(score_threshold, reverse=True)

    def clear(self):
        """Clear all values."""
        self._scores.clear()
        self._values.clear()

    def _pop_many(self, score_threshold, reverse=False) -> list:
        """Pop values with scores less than `score`.

        The returned values are guaranteed to be in order.
        Returns an empty list if no values.
        """
        idx = bisect(self._scores, score_threshold)
        if reverse:
            self._scores = self._scores[:idx]
            values, self._values = self._values[idx:], self._values[:idx]
        else:
            self._scores = self._scores[idx:]
            values, self._values = self._values[:idx], self._values[idx:]
        return values

    def _pop(self, reverse=False):
        if not self._values:
            raise StopIteration('Empty stack.')
        if reverse:
            del self._scores[-1]
            return self._values.pop(-1)
        else:
            del self._scores[0]
            return self._values.pop(0)

    def _select(self, score_threshold, reverse=False) -> list:
        """Select and return items without removing them from the stack.

        The values are guaranteed to be in order.
        """
        idx = bisect(self._scores, score_threshold)
        if reverse:
            values = self._values[idx:]
            values.reverse()
            return values
        else:
            return self._values[:idx]


class RestrictedDict(dict):
    """Same as a normal mapping but forbids key updates.

    >>> m = RestrictedDict(a=1, b=2)
    >>> m['c'] = 3
    >>> 'c' in m
    True

    Resetting a key raises a ValueError:

    >>> m['c'] = 5  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError:

    >>> m.update({'c': 5})   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    NotImplementedError:

    So as trying to remove it:

    >>> m.pop('c')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    NotImplementedError:

    """

    __msg = 'Restricted mapping does not allow key deletion.'

    @not_implemented(__msg)
    def popitem(self):
        ...

    @not_implemented(__msg)
    def pop(self, __key):
        ...

    @not_implemented(__msg)
    def update(self, __m, **kwargs):
        ...

    def __setitem__(self, __k, __v) -> None:
        if self.__contains__(__k):
            raise ValueError('Item is already present.')
        super().__setitem__(__k, __v)


NSKey = NewType('NSKey', str)  # namespace key


@dataclass
class Namespace(Mapping):
    """Namespace can be used for shared key and name management.

    Create namespaces.

    >>> ns = Namespace(env='dev', name='app')
    >>> sub_ns = ns / 'sub'  # eq to .create_namespace('sub')
    >>> str(sub_ns)
    'dev.app.sub'

    Get keys.

    >>> sub_ns.get_key('key')
    'dev.app.sub.key'

    """

    delimiter = '.'  # it is supported both by kafka topics and redis keys

    env: str
    name: str
    namespaces: Dict[str, 'Namespace'] = field(init=False, default_factory=dict)

    def get_key(self, __key: str) -> NSKey:
        """Get a shared key."""
        if self.delimiter in __key:
            raise ValueError(f'"{self.delimiter}" symbol is not allowed in namespace names.')
        return cast(NSKey, self.delimiter.join((self.env, self.name, __key)))

    def create_namespace(self, __ns: str) -> 'Namespace':
        """Create a new sub-namespace."""
        if self.delimiter in __ns:
            raise ValueError(f'"{self.delimiter}" symbol is not allowed in namespace names.')
        if __ns in self.namespaces:
            return self.namespaces[__ns]
        else:
            ns = Namespace(env=self.env, name=self.delimiter.join((self.name, __ns)))
            self.namespaces[__ns] = ns
            return ns

    @classmethod
    def join(cls, *args):
        """Join arguments in a namespace key.

        You should use `NSKey.get_key` instead of this when possible.
        """
        return NSKey(cls.delimiter.join(args))

    def __getitem__(self, __item: str) -> 'Namespace':
        return self.namespaces[__item]

    def __len__(self):
        return len(self.namespaces)

    def __iter__(self) -> Iterator[str]:
        return iter(self.namespaces)

    def __truediv__(self, __other: str) -> 'Namespace':
        return self.create_namespace(__other)

    def __str__(self):
        return self.delimiter.join((self.env, self.name))


class TTLDict(MutableMapping):
    """A simple TTL dict mostly compatible with a normal one.

    Similar to a normal dict, but with ttl in seconds:

    >>> d = TTLDict()
    >>> d.set('key', 'value', ttl=1)
    >>> d.get('key')
    'value'

    With no ttl (infinite):

    >>> d['key'] = 'value'

    """

    __slots__ = ('_dict',)

    def __init__(self, *args, **kws):
        self._dict: Dict[Hashable, Tuple[Any, float]] = dict()  # (value, exp)
        for key, value in dict(*args, **kws).items():
            self[key] = value

    def __getitem__(self, key: Hashable) -> Any:
        value, t = self._dict[key]
        if not t or t > time():
            return value
        else:
            del self[key]
            raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.set(key, value, 0)

    def __delitem__(self, key: Hashable) -> None:
        del self._dict[key]

    def __len__(self) -> int:
        return len(self._dict)

    def __bool__(self) -> bool:
        return bool(len(self))

    def __eq__(self, other: 'TTLDict') -> bool:
        return other._dict == self._dict  # noqa

    def __iter__(self):
        return iter(self.keys())

    def get(self, item: Hashable, default: Any = None):
        try:
            return self[item]
        except KeyError:
            return default

    def get_exp(self, key: Hashable) -> float:
        """Get exp time of a key."""
        value, t = self._dict[key]
        if not t or t > time():
            return t
        else:
            del self[key]
            raise KeyError(key)

    def set(self, key: Hashable, value: Any, ttl: float) -> None:
        """Set a key."""
        self._dict[key] = (value, time() + ttl)


class Scope(Enum):
    """Session permission scopes for RPC methods."""

    SYSTEM = 0
    ADMIN = 10
    USER = 100
    GUEST = 1000


SCOPES = {s.name: s for s in Scope}
SCOPE_MAP = {Scope.SYSTEM: 'system', Scope.ADMIN: 'admin', Scope.USER: 'user'}  # used by permission servicesR


class RequestContext(TypedDict):
    """Request context for an RPC request."""

    correlation_id: str
    session_id: Optional[str]
    request_deadline: Optional[int]


class Session(Serializable):
    """User session data."""

    __slots__ = ('id', 'h_agent', 'user_id', 'expires', 'permissions', 'data', 'created', '_stored', '_changed')

    def __init__(
        self,
        *,
        id: str,  # noqa
        h_agent: Optional[bytes],
        user_id: Optional[uuid.UUID],
        expires: int,
        permissions: FrozenSet[str],
        data: dict,
        created: datetime,
        _stored: bool,
        _changed: bool,
        _loaded: bool,
    ):
        """Initialize.

        :param id:
        :param h_agent:
        :param user_id:
        :param expires:
        :param permissions:
        :param data:
        :param created:
        :param _stored:
        :param _changed:
        :param _loaded:
        """
        self.id = id
        self.h_agent = h_agent
        self.user_id = user_id
        self.expires = expires
        self.permissions = frozenset(permissions)
        self.data = data
        self.created = created
        self._stored = _stored
        self._changed = _changed
        self._loaded = _loaded

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, key, value):
        self.update({key: value})

    @property
    def scope(self) -> Scope:
        """Base user scope."""
        if SCOPE_MAP[Scope.SYSTEM] in self.permissions:
            return Scope.SYSTEM
        elif SCOPE_MAP[Scope.USER] in self.permissions:
            return Scope.USER
        else:
            return Scope.GUEST

    @property
    def stored(self) -> bool:
        """Session should be stored."""
        return self._stored

    @property
    def changed(self) -> bool:
        """Session has changed."""
        return self._changed

    @property
    def loaded(self) -> bool:
        """Session has been loaded from db."""
        return self._loaded

    def update(self, data: dict):
        """Update session data."""
        self.data.update(data)
        self._changed = True

    def clear(self):
        """Clear all session data."""
        self.data.clear()
        self._changed = True

    def repr(self) -> dict:
        """Get object representation."""
        return {slot: getattr(self, slot) for slot in self.__slots__ if not slot.startswith('_')}
