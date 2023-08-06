"""Application essential services and loaders."""

import abc
import asyncio
import errno
import logging
import os
import pathlib
import uuid
from ast import literal_eval
from argparse import ArgumentParser
from enum import Enum
from functools import partial
from time import time
from typing import (
    Union,
    List,
    Type,
    TypeVar,
    Optional,
    Iterable,
    cast,
    TypedDict,
    Awaitable,
    Callable,
    Collection,
    NewType,
    Tuple,
)
from contextvars import ContextVar  # noqa: pycharm
from weakref import proxy
from warnings import warn

import yaml
from aiohttp.web import Application, run_app, AppRunner

import kaiju_tools.jsonschema as js
from kaiju_tools.interfaces import App, ServiceManagerInterface, PublicInterface
from kaiju_tools.registry import ClassRegistry
from kaiju_tools.encoding import load
from kaiju_tools.functions import retry, timeout
from kaiju_tools.logging import HANDLERS, Logger
from kaiju_tools.mapping import recursive_update
from kaiju_tools.templates import Template
from kaiju_tools.types import Namespace, SortedStack, RequestContext
from kaiju_tools.context_vars import *

__all__ = [
    'Service',
    'ContextableService',
    'ServiceClassRegistry',
    'SERVICE_CLASS_REGISTRY',
    'ServiceConfigurationError',
    'ServiceNotAvailableError',
    'ServiceContextManager',
    'RequestContext',
    'run_command',
    'Commands',
    'COMMANDS',
    'BaseCommand',
    'LoggingService',
    'Scheduler',
    'ExecPolicy',
    'RequestContext',
    'ServiceConfig',
    'REQUEST_SESSION',
    'REQUEST_CONTEXT',
    'HandlerSettings',
    'LoggerSettings',
    'ConfigLoader',
    'get_cli_parser',
    'ConfigurationError',
    'Settings',
    'AppSettings',
    'RunSettings',
    'ProjectSettings',
    'MainSettings',
    'ServiceSettings',
    'init_app',
    'run_server',
]


class ServiceConfig(TypedDict, total=False):
    """Service configuration parameters."""

    cls: str  #: service class name as in :py:class:`~kaiju_tools.services.service_class_registry`
    name: str  #: unique service name, each service should have a default value for this
    enabled: bool  #: disable service
    required: bool  #: skip a service and proceed on initialization error
    override: bool  #: replace an existing service with the same name
    settings: dict  #: custom settings, unpacked to a service's __init__


class ConfigurationError(KeyError):
    """Configuration key not found."""


class Settings(dict):
    """Settings object."""

    validator: js.Object = None

    def __init__(self, seq):
        """Initialize."""
        if self.validator:
            seq = js.compile_schema(self.validator)(seq)
        super().__init__(seq)

    def __getattr__(self, item):
        """Get a parameter from settings dict."""
        try:
            return self[item]
        except KeyError:
            raise ConfigurationError(f'No such config value: {item}')


class AppSettings(Settings):
    """Web application init settings."""

    validator = js.Object(
        {'debug': js.Boolean(default=False), 'client_max_size': js.Integer(minimum=1024, default=1024**2)},
        additionalProperties=False,
        required=[],
    )


class RunSettings(Settings):
    """Server run settings."""

    validator = js.Object(
        {
            'host': js.Nullable(js.String(minLength=1, default=None)),
            'port': js.Nullable(js.Integer(minimum=1, maximum=65535, default=None)),
            'path': js.Nullable(js.String(minLength=1, default=None)),
            'shutdown_timeout': js.Integer(minimum=0, default=30),
            'keepalive_timeout': js.Integer(minimum=0, default=60),
        },
        additionalProperties=False,
        required=[],
    )


class MainSettings(Settings):
    """Main project settings."""

    validator = js.Object(
        {
            'name': js.String(minLength=1),
            'version': js.String(minLength=1),
            'env': js.String(minLength=1),
            'loglevel': js.Enumerated(enum=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO'),
        },
        additionalProperties=False,
        required=['name', 'version', 'env'],
    )


class ServiceSettings(Settings):
    """Service configuration."""

    validator = js.Object(
        {
            'cls': js.String(minLength=1),
            'name': js.String(minLength=1),
            'enabled': js.Boolean(default=True),
            'required': js.Boolean(default=True),
            'override': js.Boolean(default=False),
            'loglevel': js.JSONSchemaObject(enum=['DEBUG', 'INFO', 'WARNING', 'ERROR', None], default=None),
            'settings': js.Object(),
        },
        additionalProperties=False,
        required=['cls'],
    )

    def __init__(self, seq):
        if type(seq) is str:
            seq = {'cls': seq}
        super().__init__(seq)


class ProjectSettings(Settings):
    """Validation schema for project settings."""

    def __init__(self, app: dict, run: dict, main: dict, etc: dict, services: list):
        """Initialize."""
        super().__init__(
            dict(
                app=AppSettings(app),
                run=RunSettings(run),
                main=MainSettings(main),
                etc=Settings(etc),
                services=tuple(ServiceSettings(srv) for srv in services),
            )
        )


def get_cli_parser() -> ArgumentParser:
    """Parse application CLI args."""
    _parser = ArgumentParser(prog='aiohttp web application', description='web application run settings')
    _parser.add_argument('--host', dest='host', default=None, help='web app host (default - from settings)')
    _parser.add_argument('--port', dest='port', type=int, default=None, help='web app port (default - from settings)')
    _parser.add_argument(
        '--path', dest='path', default=None, metavar='FILE', help='socket path (default - from settings)'
    )
    _parser.add_argument(
        '--debug', dest='debug', action='store_true', default=None, help='run in debug mode (default - from settings)'
    )
    _parser.add_argument(
        '-c',
        '--config',
        dest='cfg',
        default=[],
        metavar='FILE',
        action='append',
        help='yaml config paths, use multiple times to merge multiple configs (default - settings/config.yml)',
    )
    _parser.add_argument(
        '-l',
        '--log',
        dest='loglevel',
        default=None,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='log level',
    )
    _parser.add_argument(
        '-f',
        '--env-file',
        dest='env_file',
        default=[],
        metavar='FILE',
        action='append',
        help='env file paths (default to ./settings/env.json + ./settings/env.local.json)',
    )
    _parser.add_argument(
        '-e',
        '--env',
        dest='env',
        default=[],
        metavar='KEY=VALUE',
        action='append',
        help='overrides env variable (may be used multiple times)',
    )
    _parser.add_argument(
        '--no-os-env', dest='no_os_env', action='store_true', default=False, help='do not use OS environment variables'
    )
    _parser.add_argument(
        'cmd', metavar='COMMAND', default=None, nargs='?', help='optional management command to execute'
    )
    return _parser


class ConfigLoader:
    """Config loader class. It is intended to be used before the app start."""

    CmdName = NewType('CmdName', str)
    config_class = ProjectSettings
    _file_loaders = {
        '.json': load,
        '.yml': partial(yaml.load, Loader=yaml.SafeLoader),
        '.yaml': partial(yaml.load, Loader=yaml.SafeLoader),
    }

    def __init__(
        self,
        base_config_paths: Iterable[str] = tuple(),
        base_env_paths: Iterable[str] = tuple(),
        default_env_paths: Iterable[str] = tuple(),
    ):
        """Initialize.

        :param base_config_paths: list of base paths to .yml config files in sequential order
        :param base_env_paths: list of base paths to .env files in sequential order
        :param default_env_paths: list of paths to .env files which may be overriden by the `--env-file` flag
        """
        self.base_config_paths = base_config_paths
        self.base_env_paths = base_env_paths
        self.default_env_paths = default_env_paths
        self.logger = logging.getLogger('loader')

    def configure(self) -> (Optional[CmdName], ProjectSettings):
        """Load project config and command.

        Loading order:

        - ./settings/config.yml
        - .yml files, first to last
        - ./settings/env.json
        - .env files, first to last
        - os env vars (unless --no-os-env specified)
        - CLI env vars

        """
        parser = get_cli_parser()
        args = parser.parse_known_args()[0].__dict__
        config_paths = [*self.base_config_paths, *args.get('cfg', [])]
        _paths = args.get('env_file', [])
        if not _paths:
            _paths = self.default_env_paths
        env_paths = [*self.base_env_paths, *_paths]
        config, env = {}, {}
        for cfg_path in config_paths:
            _data = self._from_file(cfg_path)
            _services = _data.pop('services', [])
            config = recursive_update(config, _data)
            if 'services' in config:
                config['services'].extend(_services)
            else:
                config['services'] = _services
        for env_path in env_paths:
            env.update(self._from_file(env_path))
        if not args['no_os_env']:
            self._update_env_from_os(env)
        self._update_env_from_cli(env, args)
        config = self._from_dict(config, env)
        if not args['no_os_env']:
            self._update_config_from_os(config)
        self._update_config_from_cli(config, args)
        command = args.get('cmd')
        config = ProjectSettings(**config)
        return command, config

    def _from_file(self, path) -> dict:
        """Load data from a config file."""
        self.logger.info('Loading %s', path)
        path = pathlib.Path(path)
        if path.suffix not in self._file_loaders:
            raise ConfigurationError(f'Unknown config file format: {path}')
        loader = self._file_loaders[path.suffix]
        if not path.exists() or path.is_dir():
            warn('Config path does not exist or it\'s a directory.' ' "%s" - not found!' % path)
            return {}
        with open(path) as f:
            data = loader(f)
        return data

    def _from_dict(self, data: dict, env: dict) -> ProjectSettings:
        """Create config from a template and env map."""
        data = Template(data).fill(env)
        config = self.config_class(**data)
        return config

    def _update_env_from_os(self, env: dict) -> None:
        """Get env arguments from OS env."""
        self.logger.debug('Loading OS')
        for key in list(env.keys()):
            value = os.getenv(key)
            if value:
                self.logger.info('From OS: %s', key)
                env[key] = self._init_env_value(value)

    def _update_env_from_cli(self, env: dict, args: dict) -> None:
        """Update env map from CLI arguments."""
        self.logger.debug('Loading CLI')
        for record in args.get('env', []):
            k, v = record.split('=')
            if v:
                self.logger.info('From CLI: %s', k)
                env[k] = self._init_env_value(v)

    def _update_config_from_os(self, config: ProjectSettings):
        """Set OS args."""

    @staticmethod
    def _update_config_from_cli(config: ProjectSettings, args: dict):
        """Set CLI arguments."""
        for key in ('host', 'port', 'path'):
            value = args.get(key)
            if value is not None:
                config.run[key] = value
        debug = args.get('debug')
        if debug is not None:
            config.app['debug'] = debug
        log = args.get('loglevel')
        if log is not None:
            config.main['loglevel'] = log

    @staticmethod
    def _init_env_value(value: str):
        """Parse env arg from --env or unix environment."""
        if value is None:
            return None
        value = value.strip()
        if not value:
            return None
        _value = value.lower()
        if _value == 'true':
            value = True
        elif _value == 'false':
            value = False
        elif _value == 'none':
            value = None
        else:
            try:
                value = literal_eval(value)
            except Exception:  # noqa: reasonable
                pass
        return value


class Service(abc.ABC):
    """Base service class."""

    service_name = None  #: you may define a custom service name here

    def __init__(self, app: App = None, logger=None):
        """Initialize.

        :param app: aiohttp web application
        :param logger: a logger instance (None for default)
        """
        self.app = app
        if logger is None:
            logger = logging.getLogger(self.app.name)
        self.logger: Logger = logger

    def discover_service(
        self,
        name: Union[str, object, None],
        cls: Union[Union[str, Type], Iterable[Union[str, Type]]] = None,
        required=True,
    ):
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
            False means that nothing will be returned, i.e. service will be disabled
        :param cls: specify service class. If name wasn't specified, then the first
            service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if name is False and not required:
            return
        elif isinstance(name, Service):
            return name
        else:
            return self.app.services.discover_service(name=name, cls=cls, required=required)


class ContextableService(Service):
    """A service which must be asynchronously initialized after it was created."""

    async def init(self):
        """Define your asynchronous initialization here."""

    async def close(self):
        """Define your asynchronous de-initialization here."""

    @property
    def closed(self) -> bool:
        """Must return True if `close()` procedure has been successfully executed."""
        return False

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


Contextable = ContextableService


class ServiceConfigurationError(RuntimeError):
    """An error during services configuration or initialization."""


class ServiceNotAvailableError(ValueError):
    """Service with such name doesn't exist."""


class ServiceClassRegistry(ClassRegistry[str, Type[Service]]):
    """Class registry for service classes."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (Service,)


SERVICE_CLASS_REGISTRY = ServiceClassRegistry(raise_if_exists=False)  #: default service class registry object

_Service = TypeVar('_Service', bound=Service)


class ServiceContextManager(ContextableService, ServiceManagerInterface):
    """Services manager."""

    service_name = 'srv'

    def __init__(
        self,
        app: App,
        settings: List[Union[ServiceConfig, str]],
        class_registry: ServiceClassRegistry = SERVICE_CLASS_REGISTRY,
        logger=None,
    ):
        """Initialize."""
        super().__init__(app=app, logger=logger)
        self._settings = settings
        self._registry = class_registry
        self._required = set()
        self._running_services = []
        self._services = {}

    async def init(self):
        self._create_services()
        for name, service in self._services.items():
            try:
                await self.start_service(name)
            except Exception as exc:
                if name in self._required:
                    await self.close()
                    raise
                else:
                    self.logger.error('Service failed', service=name, exc_info=exc)

    async def close(self):
        for name in self._running_services[::-1]:
            await self.terminate_service(name)
        self._running_services.clear()

    def add_service(self, service: Service, required: bool = True, name: str = None) -> None:
        """Add a service directly to the service map.

        This method is supposed to be used in testing / debugging, not intended for production use.
        """
        name = self._get_service_name(type(service), name)
        service.service_name = name
        self._services[name] = service
        service.logger = self.app.logger.getChild(name)
        if required:
            self._required.add(service.service_name)

    async def start_service(self, name: str) -> None:
        """Start an idle service."""
        service = self._services[name]
        if name in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.debug('Starting service', service=service.service_name)
            await service.init()
            self._running_services.append(name)

    async def terminate_service(self, name: str) -> None:
        """Terminate a running service."""
        service = self._services[name]
        if name not in self._running_services:
            return
        if isinstance(service, ContextableService):
            self.logger.debug('Closing service', service=service.service_name)
            try:
                await service.close()
            except Exception as exc:
                self.logger.error('Service failed to close', service=name, exc_info=exc)
        self._running_services.remove(name)

    async def cleanup_context(self, _):
        """Get aiohttp cleanup context."""
        await self.init()
        yield
        await self.close()

    def __getattr__(self, item):
        return self._services[item]

    def __getitem__(self, item):
        return self._services[item]

    def __contains__(self, item):
        return item in self._services

    def items(self):
        return self._services.items()

    def discover_service(
        self,
        name: Union[str, _Service, False] = None,
        cls: Type[_Service] = None,
        required: bool = True,
    ) -> Optional[_Service]:
        """Discover a service using specified name and/or service class.

        :param name: specify a service name or service instance (in latter case
            it will be returned as is)
        :param cls: specify service class or a list of classes. If name wasn't specified,
            then the first service matching given class will be returned. If name and class
            both were specified, then the type check will be performed on a newly
            discovered service. If multiple classes are provided they will be checked in
            priority order one by one.
        :param required: means that an exception will rise if service doesn't exist
            otherwise in this case None will be returned
        """
        if isinstance(name, Service):
            return name

        if name:
            if name not in self._services:
                raise ServiceNotAvailableError(f'Service not found: "{name}".')
            service = self._services[name]
            if not isinstance(service, cls):
                raise ServiceNotAvailableError(f'Service class mismatch: {cls} vs {type(service)}.')
            return service

        service = next((service for service in self._services.values() if isinstance(service, cls)), None)
        if service:
            return service
        elif required:
            raise ServiceNotAvailableError(f'Service not found: {name}/{cls}.')

    @staticmethod
    def _get_service_name(service_cls: Type, name: Optional[str]) -> str:
        if not name:
            name = getattr(service_cls, 'service_name', None)
        if name is None:
            name = service_cls.__name__
        return name

    def _create_services(self) -> None:
        for settings in self._settings:
            if type(settings) is str:
                settings = ServiceConfig(cls=settings)
            if not settings.get('enabled', True):
                continue
            cls = self._registry[settings['cls']]
            name = self._get_service_name(cls, settings.get('name'))
            if name in self._services and not settings.get('override'):
                raise ServiceConfigurationError('Service with name "%s" already registered.' % name)
            _name = cls.service_name
            cls.service_name = name  # TODO: fix it
            service = cls(app=self.app, **settings.get('settings', {}), logger=self.app.logger.getChild(name))  # noqa
            cls.service_name = _name
            service.service_name = name
            self._services[name] = service
            if settings.get('required', True):
                self._required.add(name)
            loglevel = settings.get('loglevel')
            if loglevel:
                service.logger.setLevel(loglevel)


_Callable = Callable[..., Awaitable]


class ExecPolicy(Enum):
    """Task policy for a scheduled task."""

    WAIT = 'WAIT'  #: wait until the current task iteration is executed
    CANCEL = 'CANCEL'  #: cancel the current iteration immediately and restart the task


class _ScheduledTask:
    """Scheduled task information."""

    __slots__ = (
        '_scheduler',
        'name',
        'method',
        'params',
        'interval',
        'policy',
        'called_at',
        '_enabled',
        'executed',
        'retries',
        '__weakref__',
    )

    def __init__(
        self,
        scheduler: 'Scheduler',
        name: str,
        method: Callable,
        params: Union[dict, None],
        interval: float,
        policy: ExecPolicy,
        retries: int,
    ):
        """Initialize."""
        self._scheduler = proxy(scheduler)
        self.name = name
        self.method = method
        self.params = params
        self.interval = interval
        self.policy = policy
        self.called_at = 0
        self.retries = retries
        self._enabled = True
        self.executed: Union[asyncio.Task, None] = None

    @property
    def enabled(self) -> bool:
        """Task is enabled for execution."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable task."""
        self._enabled = value
        if value is True:
            t_ex = self.called_at + self.interval
            self._scheduler._stack.insert(t_ex, self)  # noqa

    @property
    def max_timeout(self) -> float:
        if self.policy is ExecPolicy.CANCEL:
            return max(0.0, self.interval)
        else:
            return max(0.0, self.interval * 4.0)


class Scheduler(ContextableService, PublicInterface):
    """Scheduler for periodic tasks execution."""

    ExecPolicy = ExecPolicy

    def __init__(self, *args, refresh_rate: float = 1.0, **kws):
        """Initialize.

        :param refresh_rate: base refresh rate
        """
        super().__init__(*args, **kws)
        self.refresh_rate = refresh_rate
        self._stack = SortedStack()
        self._tasks: List[_ScheduledTask] = []
        self._scheduler_task: Union[asyncio.Task, None] = None

    async def init(self):
        """Initialize."""
        self._scheduler_task = asyncio.create_task(self._iter())

    async def close(self):
        """Close."""
        self._scheduler_task.cancel()
        self._scheduler_task = None
        self._stack.clear()
        await asyncio.gather(
            *(
                task.executed
                for task in self._tasks
                if task.executed and not (task.executed.done() or task.executed.cancelled())
            ),
            return_exceptions=True,
        )

    @property
    def routes(self):
        return {'tasks': self.list_tasks}

    async def list_tasks(self):
        """List registered tasks."""
        return [
            {
                'name': task.name,
                'enabled': task.enabled,
                'interval': task.interval,
                'policy': task.policy.value,
                'retires': task.retries,
                'executed': task.executed is not None,
                'called_at': task.called_at,
            }
            for task in self._tasks
        ]

    @property
    def tasks(self):
        """Get a list of registered tasks."""
        return self._tasks

    def schedule_task(
        self,
        method: _Callable,
        interval: float,
        params: Union[dict, None] = None,
        *,
        policy: ExecPolicy = ExecPolicy.CANCEL,
        retries: int = 0,
        name: str = None,
    ) -> _ScheduledTask:
        """Schedule a periodic task.

        :param method: RPC server method name
        :param params: method input arguments
        :param interval: exec interval in seconds
        :param policy: exec policy
        :param retries: number of retries if any
        :param name: optional custom task name (for tracing)
        :returns: an instance of scheduled task
            you can temporarily suspend this task from execution by settings `task.enabled = False`
            it will not be picked up by the scheduler until you set it back to `True`
        """
        if name is None:
            name = f'scheduled:{method.__name__}'
        if params is None:
            params = {}
        self.logger.debug('schedule', task_name=name, interval=interval, policy=policy.value)
        task = _ScheduledTask(self, name, method, params, interval, policy, retries)
        self._tasks.append(task)
        self.refresh_rate = min(self.refresh_rate, interval, 0.1)
        t_ex = time() + interval
        self._stack.insert(t_ex, task)
        return task

    async def _iter(self) -> None:
        """Iterate over the tasks ready to run."""
        while 1:
            to_execute = self._stack.pop_many(time())
            for scheduled in to_execute:
                scheduled = cast(_ScheduledTask, scheduled)
                if not scheduled.enabled:
                    continue
                if scheduled.executed and not (scheduled.executed.done() or scheduled.executed.cancelled()):
                    if scheduled.policy is ExecPolicy.CANCEL:
                        scheduled.executed.cancel(msg='Cancelled by the scheduler')
                    elif scheduled.policy is ExecPolicy.WAIT:
                        continue
                    else:
                        raise RuntimeError(f'Unsupported exec policy: {scheduled.policy}')

                scheduled.executed = task = asyncio.create_task(self._run_task(scheduled))
                scheduled.called_at = time()
                task._scheduled = scheduled
                task.add_done_callback(self._task_callback)
                task.set_name(scheduled.name)

            await asyncio.sleep(self._get_sleep_interval())

    async def _run_task(self, task: _ScheduledTask) -> None:
        """Run task in a wrapper."""
        try:
            async with timeout(task.max_timeout):
                if task.retries:
                    await retry(task.method, kws=task.params, retries=task.retries)
                else:
                    await task.method(**task.params)
        except Exception as exc:
            self.logger.error('task error', task_name=task.name, exc_info=exc)

    def _get_sleep_interval(self) -> float:
        """Get real sleep interval for the scheduler loop."""
        lowest_score = self._stack.lowest_score
        if lowest_score is None:
            lowest_score = 0
        t0 = time()
        interval = min(max(lowest_score - t0, t0), self.refresh_rate)
        return interval

    def _task_callback(self, task: asyncio.Task) -> None:
        """Capture a task result."""
        result = task.result()
        if isinstance(result, Exception):
            self.logger.error(str(result), exc_info=result)
        scheduled = task._scheduled  # noqa
        self._stack.insert(scheduled.called_at + scheduled.interval, scheduled)
        scheduled.executed = None
        task._scheduled = None


class HandlerSettings(TypedDict, total=False):
    """Log handler settings in a config file."""

    cls: str
    name: str
    enabled: bool
    settings: dict
    loglevel: str


class LoggerSettings(TypedDict, total=False):
    """Logger settings in a config file."""

    name: str
    enabled: bool
    handlers: Union[List[str], bool]
    loglevel: str


class LoggingService(ContextableService):
    """Log handler and formatter configuration for application loggers."""

    def __init__(
        self,
        *args,
        loggers: Collection[LoggerSettings] = None,
        handlers: Collection[HandlerSettings] = None,
        loglevel: str = None,
        handler_classes=HANDLERS,
        **kws,
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self.handler_classes = handler_classes
        self.logger_settings: Collection[LoggerSettings] = loggers
        self.handler_settings: Collection[HandlerSettings] = handlers
        self.loglevel = loglevel if loglevel else getattr(self.app, 'loglevel', 'INFO')
        self.clear_root_logger()
        self.handlers = self.init_handlers()
        self.loggers = self.init_loggers()

    @staticmethod
    def clear_root_logger() -> None:
        """Remove all existing handlers from the root logger."""
        logger = logging.getLogger()
        logger.handlers.clear()
        logger.setLevel(logging.FATAL)

    def init_handlers(self) -> dict:
        """Initialize handler classes."""
        handlers = {}
        for settings in self.handler_settings:
            if not settings.get('enabled', True):
                continue
            cls = self.handler_classes[settings['cls']]
            handler = cls(app=self.app, **settings.get('settings', {}))
            loglevel = settings.get('loglevel', self.loglevel)
            handler.setLevel(loglevel)
            handlers[settings['name']] = handler
        return handlers

    def init_loggers(self) -> dict:
        """Initialize logger classes."""
        loggers = {}
        for settings in self.logger_settings:
            if not settings.get('enabled', True):
                continue
            logger = logging.getLogger(settings['name'])
            if settings['handlers'] is True:
                logger_handlers = self.handlers.keys()
            else:
                logger_handlers = settings['handlers']
            for handler in logger_handlers:
                logger.addHandler(self.handlers[handler])
            loglevel = settings.get('loglevel', self.loglevel)
            logger.setLevel(loglevel)
            loggers[settings['name']] = logger
        return loggers


class BaseCommand(ContextableService, abc.ABC):
    """Base application command, recognized by CLI."""

    service_name = None  #: command name after `python -m my_app [...]`
    run_app = True

    def __init__(self, app: App, logger=None):
        """Initialize."""
        super().__init__(app=app, logger=logger)
        self._runner = AppRunner(app)
        self._closed = True

    @classmethod
    def get_parser(cls) -> ArgumentParser:
        """Get an argument parser for CLI command arguments.

        You can provide additional CLI args for this particular command here.
        """
        return ArgumentParser()

    @abc.abstractmethod
    async def command(self, **kws):
        """Run a specific command."""

    async def init(self):
        """Initialize."""

    async def close(self):
        """Close command context."""

    @property
    def closed(self) -> bool:
        return self._closed

    def run(self):
        result = 1
        loop = asyncio.get_event_loop()
        try:
            self.logger.info('Setting up a webapp runner.')
            if self.run_app:
                loop.run_until_complete(self._runner.setup())
            self.logger.info('Initialization.')
            loop.run_until_complete(self.init())
            self._closed = False
            params, _ = self.get_parser().parse_known_args()
            self.logger.info('Executing command "%s" with params: "%s"', self.service_name, params)
            result = loop.run_until_complete(self.command(**params.__dict__))
        except Exception as err:
            self.logger.error('Command failed.', exc_info=err)
        finally:
            self.logger.info('Closing.')
            loop.run_until_complete(self.close())
            if self.run_app:
                loop.run_until_complete(self._runner.cleanup())
            loop.close()
            self._closed = True
            return result


class Commands(ClassRegistry):
    """Map of all available commands."""

    @classmethod
    def get_base_classes(cls) -> Tuple[Type, ...]:
        return (BaseCommand,)


COMMANDS = Commands()  # : default commands registry


def run_command(app: App, command: ConfigLoader.CmdName, commands_registry: Commands = COMMANDS) -> int:
    """Run an app with a CLI command.

    :param app: application object
    :param command: command name after python -m app ...
    :param commands_registry: provide an instance of command class registry
    :returns: unix exit code
    """
    if command in commands_registry:
        cmd = commands_registry[command]
        cmd = cmd(app=app, logger=app.logger.getChild('CLI'))
        result = cmd.run()
    else:
        app.logger.error('Unknown command "%s".', command)
        result = errno.ENOENT
    return result


def init_app(
    settings: ProjectSettings,
    attrs: dict = None,
    middlewares: Collection = None,
    class_registry: ServiceClassRegistry = SERVICE_CLASS_REGISTRY,
) -> App:
    """Create a web application object.

    :param settings: project settings, usually provided by the configuration service.
    :param attrs: additional application attributes
    :param middlewares: list of additional aiohttp middlewares
    :param class_registry: registry of service classes
    """
    from kaiju_tools.http import error_middleware, session_middleware

    if middlewares is None:
        middlewares = []

    middlewares = [error_middleware, session_middleware, *middlewares]
    app = Application(middlewares=middlewares, logger=logging.getLogger(settings.main.name), **settings.app)
    app.request_context = REQUEST_CONTEXT
    app.request_session = REQUEST_SESSION
    app.id = uuid.uuid4()
    for key, value in settings.main.items():
        app[key] = value
        setattr(app, key, value)
    if attrs:
        for key, value in attrs.items():
            app[key] = value
            setattr(app, key, value)
    app.settings = settings
    app = cast(App, app)
    app.cookie_key = f'{app.env}-{app.name}-sid'
    app.namespace = Namespace(env=app.env, name=app.name)
    app.namespace_shared = Namespace(env=app.env, name='_shared')
    app.services = services = ServiceContextManager(
        app=app, settings=settings.services, class_registry=class_registry, logger=app.logger
    )
    app.cleanup_ctx.append(services.cleanup_context)
    return app


def run_server(
    init_app_func=init_app,
    base_config_paths: Collection[str] = None,
    base_env_paths: Collection[str] = None,
    default_env_paths: Collection[str] = None,
) -> None:
    """Run aiohttp server or command.

    You should use this in the `__main__` section of the project to start the app.

    :param init_app_func: app initialization function
    :param base_config_paths: list of base paths to .yml config files in sequential order
    :param base_env_paths: list of base paths to .env files in sequential order
    :param default_env_paths: list of paths to .env files which may be overriden by the `--env-file` flag
    """
    logging.basicConfig(level='INFO')  # to be able to log config loader
    config_loader = ConfigLoader(
        base_config_paths=base_config_paths, base_env_paths=base_env_paths, default_env_paths=default_env_paths
    )
    command, config = config_loader.configure()
    logging.root.handlers = []
    app: App = init_app_func(config)
    if config.app.debug:
        warn('Running in debug mode')
    if command:
        run_command(app, command)
    else:
        run_app(app, access_log=None, **config.run)
