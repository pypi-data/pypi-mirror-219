"""Mapping related functions and classes."""

from itertools import zip_longest
from typing import Any, TypeVar, Tuple, List, Union, Iterable, Collection

__all__ = ['get_field', 'set_field', 'recursive_update', 'strip_fields', 'filter_fields', 'flatten', 'unflatten']

_DictLike = TypeVar('_DictLike', Tuple[dict], List[dict], dict)


def strip_fields(__obj: _DictLike, *, prefix: str = '_') -> _DictLike:
    """Strip unwanted fields from a dictionary by prefix.

    It also accepts an iterable of dictionaries.

    >>> strip_fields({'_meta': 123, 'name': 'bob'}, prefix='_')
    {'name': 'bob'}

    >>> strip_fields([{'a': 1, '.b': 2}, {'c': [{'.d': 4, 'e': 5}], '.b': 4}], prefix='.')
    [{'a': 1}, {'c': [{'e': 5}]}]

    """
    if isinstance(__obj, dict):
        new = {}
        for key, value in __obj.items():
            if not key.startswith(prefix):
                new[key] = strip_fields(value, prefix=prefix)
        return new
    elif isinstance(__obj, (list, tuple)):
        return type(__obj)(strip_fields(sub, prefix=prefix) for sub in __obj)
    else:
        return __obj


def flatten(__obj: _DictLike, *, delimiter: str = '.') -> _DictLike:
    """Flatten dictionary keys using a specified delimiter.

    It also accepts an iterable of dictionaries.

    >>> flatten({'a': {'b': {'c': 1, 'd': 2}}})
    {'a.b.c': 1, 'a.b.d': 2}

    >>> flatten([{'a': {'b': 1}}, {'a': {'b': [{'c': {'d': 1}}], 'e': 2}}])
    [{'a.b': 1}, {'a.b': [{'c.d': 1}], 'a.e': 2}]

    """
    if isinstance(__obj, dict):
        _data = {}
        for key, value in __obj.items():
            prefix = f'{key}{delimiter}'
            if isinstance(value, dict):
                value = flatten(value, delimiter=delimiter)
                for k, v in value.items():
                    k = f'{prefix}{k}'
                    _data[k] = v
            elif isinstance(value, Collection) and not isinstance(value, str):
                _data[key] = [flatten(sub, delimiter=delimiter) for sub in value]
            else:
                _data[key] = value
        return _data
    elif isinstance(__obj, (list, tuple)):
        return type(__obj)(flatten(sub, delimiter=delimiter) for sub in __obj)
    else:
        return __obj


def unflatten(__obj: _DictLike, *, delimiter: str = '.') -> _DictLike:
    """Unpack a flattened dict into a nested dict using a specified delimiter.

    It also accepts an iterable of dictionaries. You shouldn't pass nested dictionaries as
    arguments in this function.

    >>> unflatten({'a.b.c': True, 'a.c.d': False, 'e': True})
    {'a': {'b': {'c': True}, 'c': {'d': False}}, 'e': True}

    >>> unflatten([{'a.b.c': 1}, {'a.b.d': 2}])
    [{'a': {'b': {'c': 1}}}, {'a': {'b': {'d': 2}}}]

    """
    if isinstance(__obj, dict):
        _data: dict = {}
        for key, value in __obj.items():
            key = key.split(delimiter)
            _d = _data
            for k in key[:-1]:
                if k in _d:
                    _d = _d[k]
                else:
                    _new_d: dict = {}
                    _d[k] = _new_d
                    _d = _new_d
            _d[key[-1]] = value
        return _data
    elif isinstance(__obj, (list, tuple)):
        return type(__obj)(unflatten(sub, delimiter=delimiter) for sub in __obj)
    else:
        return __obj


def get_field(__obj: _DictLike, __key: Union[str, List[str]], *, default: Any = KeyError, delimiter: str = '.') -> Any:
    """Extract field from a folded dictionary. You may specify a default value or default exception class.

    >>> get_field({'a': {'b': [1], 'c': 2}}, 'a.b')
    [1]

    >>> get_field({'a': [{'b': 1}, {'b': 2}, {}]}, 'a-b', default=None, delimiter='-')
    [1, 2, None]

    >>> get_field([{'b': {'c': [{'d': 1}, {'d': 2}, {}]}}, {'b': 3}], 'b.c.d', default=None)
    [[1, 2, None], None]

    """
    # if type(obj) is dict and key in obj:
    #     return obj[key]

    if isinstance(__key, str):
        __key = __key.split(delimiter)

    for n, _key in enumerate(__key):
        if _key:
            if isinstance(__obj, dict):
                if _key in __obj:
                    __obj = __obj[_key]
                else:
                    if type(default) is type:
                        if issubclass(default, Exception):
                            raise default(__key)
                    return default
            elif isinstance(__obj, (list, tuple)):
                __obj = type(__obj)(
                    get_field(sub_obj, __key[n:], default=default, delimiter=delimiter) for sub_obj in __obj
                )
                return __obj
            else:
                return default

    return __obj


def set_field(__obj: dict, __key: str, value, *, delimiter: str = '.') -> None:
    """Set a field in a nested dictionary by some delimited key.

    This method will modify an existing object. Nested fields will be created automatically if required.
    This method doesn't accept iterables due to their ambiguity.

    >>> o = {'data': {}}
    >>> set_field(o, 'data.shite.name', True)
    >>> o
    {'data': {'shite': {'name': True}}}

    """
    __key = __key.split(delimiter)
    for _key in __key[:-1]:
        if _key not in __obj:
            __obj[_key] = {}
        __obj = __obj[_key]
    __obj[__key[-1]] = value


def recursive_update(__obj1: _DictLike, __obj2: Union[tuple, list, dict]) -> _DictLike:
    """Recursively update dictionary from another dictionary.

    Returns the same updated object.

    It also accepts iterables of dictionaries and will try to update them in order,
    but such use of this method is discouraged.

    >>> recursive_update({'a': {'b': 1}}, {'a': {'c': 2}, 'd': 3})
    {'a': {'b': 1, 'c': 2}, 'd': 3}

    >>> recursive_update([{'a': {'b': 1}}, {'a': {'b': 1}}], [None, {'a': {'c': 2}, 'd': 3}])
    [{'a': {'b': 1}}, {'a': {'b': 1, 'c': 2}, 'd': 3}]

    """
    if isinstance(__obj1, dict):
        if isinstance(__obj2, dict):
            for key, value in __obj2.items():
                if key in __obj1:
                    __obj1[key] = recursive_update(__obj1[key], value)
                else:
                    __obj1[key] = value
        else:
            __obj1 = __obj2
    elif isinstance(__obj1, (list, tuple)):
        result = []
        if isinstance(__obj2, (list, tuple)):
            for o1, o2 in zip_longest(__obj1, __obj2):
                if o1 is not None:
                    if o2 is not None:
                        result.append(recursive_update(o1, o2))
                    else:
                        result.append(o1)
                else:
                    result.append(o2)
        __obj1 = type(__obj1)(result)
    else:
        __obj1 = __obj2
    return __obj1


def _filter_field(obj, keys, default):
    for n, key in enumerate(keys):
        if isinstance(obj, dict):
            return {key: _filter_field(obj.get(key, default), keys[n + 1 :], default)}  # noqa: linter?
        elif isinstance(obj, Collection) and not isinstance(obj, str):
            return [_filter_field(o, keys[n:], default) for o in obj]
    return obj


def filter_fields(__obj: dict, fields: Iterable[str], *, default=None, delimiter: str = '.') -> dict:
    """Filter dict keys from a specified set of fields.

    If a specified field doesn't exist in the mapping, it will be set to `default` value.
    It also accepts iterables of dictionaries.

    >>> filter_fields({'a': {'b': 1, 'c': 2}}, fields=['a.b', 'a.d'])
    {'a': {'b': 1, 'd': None}}

    >>> filter_fields({'a': [{'b': 1, 'c': 2}, {'b': 2, 'c': 3}]}, fields=['a.b', 'a.g'], default=False)
    {'a': [{'b': 1, 'g': False}, {'b': 2, 'g': False}]}

    """
    result = {}
    for field in fields:
        result = recursive_update(result, _filter_field(__obj, field.split(delimiter), default))
    return result
