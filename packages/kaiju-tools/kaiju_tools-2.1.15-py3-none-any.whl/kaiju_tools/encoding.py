"""Object serialization interfaces and classes."""

import abc
import calendar
import datetime
import uuid
from decimal import Decimal
from enum import Enum
from typing import cast, Mapping, Tuple, Type
from types import SimpleNamespace

import msgpack
import orjson as rj

# import rapidjson as rj  # type: ignore

from kaiju_tools.registry import ClassRegistry

__all__ = [
    'SerializerInterface',
    'Serializable',
    'SerializedClass',
    'SerializedClasses',
    'MimeTypes',
    'dumps',
    'loads',
    'load',
    'JSONSerializer',
    'MsgpackSerializer',
    'JSONEncoder',
    'MsgpackType',
    'ReservedClassIDs',
    'Types',
    'MSGPACK_TYPES',
    'msgpack_dumps',
    'msgpack_loads',
    'SERIALIZERS',
    'ENCODERS',
    'BINARY_TYPES',
]


class Serializable:
    """Class which supports serialization of its attributes."""

    serializable_attrs = None  #: Should be a frozenset or None. If None, then all will be used for serialization.
    include_null_values = True  #: include null values in a representation

    def repr(self) -> dict:
        """Must return a representation of object __init__ arguments."""
        _repr = {}
        if self.serializable_attrs is None:
            if self.__slots__:
                for slot in self.__slots__:
                    if not slot.startswith('_') and hasattr(self, slot):
                        v = getattr(self, slot)
                        if not self.include_null_values and v is None:
                            continue
                        if isinstance(v, Serializable):
                            _repr[slot] = v.repr()
                        else:
                            _repr[slot] = v
            else:
                for k, v in self.__dict__.items():
                    if not self.include_null_values and v is None:
                        continue
                    if not k.startswith('_'):
                        if isinstance(v, Serializable):
                            _repr[k] = v.repr()
                        else:
                            _repr[k] = v
        else:
            if self.__slots__:  # type: ignore
                for slot in self.__slots__:
                    if slot in self.serializable_attrs and hasattr(self, slot):
                        v = getattr(self, slot)
                        if not self.include_null_values and v is None:
                            continue
                        if isinstance(v, Serializable):
                            _repr[slot] = v.repr()
                        else:
                            _repr[slot] = v
            else:
                for k, v in self.__dict__.items():
                    if not self.include_null_values and v is None:
                        continue
                    if k in self.serializable_attrs:
                        if isinstance(v, Serializable):
                            _repr[k] = v.repr()
                        else:
                            _repr[k] = v

        return _repr

    def __repr__(self):
        return f'{self.__class__.__name__}(**{self.repr()})'


class SerializedClass(Serializable):
    """Serialized class."""

    def repr(self) -> dict:
        return {'__cls': self.__class__.__name__, '__attrs': super().repr()}

    @classmethod
    def from_repr(cls, attrs: dict):
        return cls(**attrs)  # noqa


class MimeTypes:
    """Standard message type headers."""

    json = 'application/json'
    msgpack = 'application/msgpack'


class SerializedClasses(ClassRegistry[str, Type[SerializedClass]]):
    """Serialized class."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (SerializedClass,)


class SerializerInterface(abc.ABC):
    """Abstract serializer interface that should be used by clients/servers to process raw messages."""

    mime_type = None  # you should define an appropriate mime type here

    def __init__(self, types: SerializedClasses = None):
        self.types = types if types else SerializedClasses()

    @classmethod
    @abc.abstractmethod
    def loads(cls, data):
        pass

    @classmethod
    @abc.abstractmethod
    def dumps(cls, data) -> bytes:
        pass


class JSONSerializer(SerializerInterface):
    """Base serializer class."""

    mime_type = MimeTypes.json

    @classmethod
    def _dumps_defaults(cls, value):
        if isinstance(value, Serializable):
            v = value.repr()
            return v
        elif isinstance(value, (set, frozenset, tuple)):
            return list(value)
        elif type(value) is bytes:
            return '[BYTES]'
        else:
            return str(value)  # TODO: need to think about that (asyncpg.pgproto.pgproto.UUID)

    def dumps(self, value):
        return rj.dumps(value, default=self._dumps_defaults, option=rj.OPT_NON_STR_KEYS)

    def loads(self, value):
        return rj.loads(value)


JSONEncoder = JSONSerializer
_encoder = JSONSerializer()
dumps = _encoder.dumps
loads = _encoder.loads


def load(f):
    return loads(f.read())


class MsgpackType(abc.ABC):
    """Serializable binary object."""

    ext_class_id: int  # must be set

    def repr(self) -> dict:
        raise NotImplementedError(
            'You either need to inherit from `kaiju_tools.serialization.Serializable`'
            ' or to set up your own `repr()` method or to set up you own'
            ' `pack_b` and `unpack_b` methods.'
        )

    def to_bytes(self) -> bytes:
        """Pack object to bytes (you can use a struct here to optimize size)."""
        return msgpack_dumps(self.repr())  # noqa

    @classmethod
    def from_bytes(cls, data: bytes) -> 'MsgpackType':
        """Unpack bytes into object."""
        return cls(**msgpack_loads(data))  # noqa


class ReservedClassIDs:
    """Msgpack ids reserved by the library."""

    # reserved from 0 to 16 (incl.)

    uuid = 1
    datetime = 3
    decimal = 4
    date = 5

    serialized_class = 19
    jsonrpc_request = 20
    jsonrpc_response = 21
    jsonrpc_error = 22


class Types(ClassRegistry[int, Type[MsgpackType]]):
    """Msgpack types registry."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (MsgpackType,)

    @classmethod
    def get_key(cls, obj: Type[MsgpackType]) -> int:
        """Determine a name by which a registered class will be referenced in the class mapping."""
        return obj.ext_class_id

    def _validate_object(self, obj) -> int:
        super()._validate_object(obj)
        key = self.get_key(obj)
        if not 16 < key < 128:
            raise ValueError('Msgpack ext type id allowed to be in range from 17 to 127 but got "%s".', key)
        return key


MSGPACK_TYPES = Types(raise_if_exists=True)


class MsgpackSerializer(SerializerInterface):
    """Base serializer class."""

    mime_type = MimeTypes.msgpack

    @classmethod
    def _default_types(cls, obj):
        """Convert type."""
        if isinstance(obj, uuid.UUID):
            return msgpack.ExtType(ReservedClassIDs.uuid, obj.bytes)
        elif isinstance(obj, datetime.datetime):
            return msgpack.ExtType(ReservedClassIDs.datetime, msgpack.dumps(calendar.timegm(obj.utctimetuple())))
        elif isinstance(obj, datetime.date):
            return msgpack.ExtType(ReservedClassIDs.date, msgpack.dumps(calendar.timegm(obj.timetuple())))
        elif isinstance(obj, MsgpackType):
            return msgpack.ExtType(obj.ext_class_id, obj.to_bytes())
        elif isinstance(obj, SerializedClass):
            return msgpack.ExtType(ReservedClassIDs.serialized_class, msgpack.dumps(tuple(obj.repr().values())))
        elif isinstance(obj, Serializable):
            return {k: cls._default_types(v) for k, v in obj.repr().items()}
        elif isinstance(obj, (set, frozenset)):
            return list(obj)
        elif isinstance(obj, Mapping):
            return dict(obj)
        elif type(obj) == SimpleNamespace:
            return obj.__dict__
        elif isinstance(obj, Enum):
            return obj.value
        elif type(obj) == Decimal:
            return msgpack.ExtType(ReservedClassIDs.decimal, msgpack.dumps(str(obj)))
        else:
            return obj

    def _ext_hook(self, code, data):
        """Load type."""
        if code == ReservedClassIDs.uuid:
            return uuid.UUID(bytes=data)
        elif code == ReservedClassIDs.datetime:
            return datetime.datetime.utcfromtimestamp(msgpack.loads(data))
        elif code == ReservedClassIDs.date:
            return datetime.date.fromtimestamp(msgpack.loads(data))
        elif code == ReservedClassIDs.decimal:
            return Decimal(msgpack.loads(data))
        # elif code == ReservedClassIDs.serialized_class:
        #     data = msgpack.loads(data)
        #     return self._load_serialized_obj({'__cls': data[0], '__attrs': data[1]})
        elif code in MSGPACK_TYPES:
            cls = cast(MsgpackType, MSGPACK_TYPES[code])
            return cls.from_bytes(data)
        # elif type(data) is dict and '__cls' in data:
        #     return self._load_serialized_obj(data)
        else:
            raise ValueError(code)

    def loads(self, *args, **kws):
        return msgpack.loads(*args, ext_hook=self._ext_hook, **kws)

    def dumps(self, *args, **kws):
        return msgpack.dumps(*args, default=self._default_types, **kws)


_serializer = MsgpackSerializer()
msgpack_dumps = _serializer.dumps
msgpack_loads = _serializer.loads


class Serializers(ClassRegistry[str, Type[SerializerInterface]]):
    """Message serializer registry class."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (SerializerInterface,)

    @classmethod
    def get_key(cls, obj: Type[SerializerInterface]) -> str:
        return obj.mime_type


SERIALIZERS = Serializers(raise_if_exists=True)
SERIALIZERS.register(JSONSerializer)
SERIALIZERS.register(MsgpackSerializer)
ENCODERS = SERIALIZERS
BINARY_TYPES = MSGPACK_TYPES
