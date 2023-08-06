from kaiju_tools.app import *  # noqa: legacy
from kaiju_tools.rpc import JSONRPCServer, AbstractRPCCompatible  # noqa: legacy
from kaiju_tools.http import RPCClientService, HTTPService
from kaiju_tools.sessions import SessionService, LoginService, AuthenticationService

SERVICE_CLASS_REGISTRY.register(LoggingService)
SERVICE_CLASS_REGISTRY.register(Scheduler)
SERVICE_CLASS_REGISTRY.register(SessionService)
SERVICE_CLASS_REGISTRY.register(LoginService)
SERVICE_CLASS_REGISTRY.register(AuthenticationService)
SERVICE_CLASS_REGISTRY.register(JSONRPCServer)
SERVICE_CLASS_REGISTRY.register(HTTPService)
SERVICE_CLASS_REGISTRY.register(RPCClientService)
