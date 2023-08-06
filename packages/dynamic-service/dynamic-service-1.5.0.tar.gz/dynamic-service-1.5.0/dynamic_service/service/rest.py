# rest.py

import os
import logging
import warnings
from functools import partial
import threading
import datetime as dt
import copy
import types
import functools
from typing import (
    Any, Union, Iterable, Optional, Dict, Callable, TypeVar
)

from represent import Modifiers

from sockets_communication.service import ServiceInterface

from uvicorn import Server, Config as ServiceConfig
from fastapi import FastAPI, APIRouter
import fastapi

from dynamic_service.base import icons
from dynamic_service.endpoints import (
    EndpointFileResponse, BaseEndpoint,
    GET, EndpointRedirectResponse,
    DocsEndpoint, FAVICON, DOCS, valid_endpoints
)

__all__ = [
    "RESTService"
]

Port = Union[str, int]
Host = str

Number = Union[int, float]

Endpoints = Dict[str, BaseEndpoint]
EndpointsContainer = Union[Iterable[BaseEndpoint], Endpoints]

_ReturnType = TypeVar("_ReturnType")

def override_signature(
        command: Union[Callable, types.FunctionType], /, *,
        new: Union[Callable[..., _ReturnType], types.FunctionType],
        name: Optional[str] = None
) -> Union[Callable[..., _ReturnType], types.FunctionType]:
    """
    Overrides the signature of a function.

    :param command: The function to override.
    :param new: The function wit the new signature.
    :param name: The new name for the function.

    :return: The old function with the new signature.
    """

    attributes = (
        '__module__', '__name__', '__qualname__',
        '__doc__', '__annotations__'
    )

    for attr in attributes:
        setattr(command, attr, getattr(new, attr))
    # end for

    command.__annotations__['return'] = (
        Dict[str, Union[int, new.__annotations__['return']]]
    )

    command = functools.update_wrapper(command, new, assigned=attributes)

    command.__kwdefaults__ = copy.copy(new.__kwdefaults__)

    if isinstance(name, str):
        command.__name__ = name
    # end if

    return command
# end override_signature

class Endpoint(partial):
    """A class to wrap around an endpoint object."""

    __slots__ = ()
# end Endpoint

class RESTService(ServiceInterface):
    """
    A class to represent a service object.

    The BaseService is the parent class of service class.
    The service class creates a service object to deploy
    functionality of endpoint objects as a REST API.

    data attributes:

    - name:
        The name of the service.

    - endpoints:
        A set of endpoint objects to serve with the api.

    - root:
        A common root path to add to all endpoints.

    - icon:
        A path to an icon file to display in a web interface (*.ico).

    - home:
        The path to the home page of the web interface.

    - debug:
        The value to set the home page as the test page.

    >>> from dynamic_service.endpoints import BaseEndpoint, GET
    >>> from dynamic_service.service.rest import RESTService
    >>>
    >>> class MyEndpoint(BaseEndpoint):
    >>>     ...
    >>>
    >>>     def endpoint(self, *args: Any, **kwargs: Any) -> Any:
    >>>         ...
    >>>
    >>> endpoint = MyEndpoint(path="/my_endpoint", methods=[GET])
    >>>
    >>> service = RESTService(
    >>>     name="service", path="<PATH TO THE SERVICE>",
    >>>     endpoints=[endpoint]
    >>> )
    >>>
    >>> service.run()
    """

    SILENT = False

    ICON = icons() + "\\icon.ico"
    VERSION = "0.0.0"
    DESCRIPTION = ""
    NAME = "Dynamic-Service"

    __modifiers__ = Modifiers(excluded=["app", "server"])

    __slots__ = (
        "name", "version", "endpoints", "description", "icon",
        "home", "debug", "app", "service", "_root", "server",
        "_serving_process", "_running_parameters", "_serving"
    )

    def __init__(
            self,
            name: Optional[str] = None,
            version: Optional[str] = None,
            endpoints: Optional[EndpointsContainer] = None,
            root: Optional[str] = None,
            description: Optional[str] = None,
            icon: Optional[str] = None,
            home: Optional[Union[str, bool]] = None,
            debug: Optional[bool] = None
    ) -> None:
        """
        Defines the class attributes.

        :param name: The name of the service.
        :param version: The version of the service.
        :param endpoints: The service endpoints.
        :param description: The description of the object.
        :param icon: The icon path.
        :param root: The root to the path.
        :param home: The home endpoint.
        :param debug: The value to create the docs' endpoint for the home endpoint.
        """

        super().__init__()

        self._root: Optional[str] = None

        _Base = type(self)

        self.endpoints: Dict[str, BaseEndpoint[_Base]] = {}

        if (home is True) or (debug and (home is None)):
            home = True
        # end if

        self.app: Optional[FastAPI] = None
        self.server: Optional[Server] = None

        self._serving_process: Optional[threading.Thread] = None

        self._running_parameters: Optional[Dict[str, Any]] = None

        self._serving = False

        self.description = description or self.DESCRIPTION
        self.root = root or ""
        self.icon = icon or self.ICON
        self.home = home
        self.name = name or self.NAME
        self.version = version or self.VERSION

        self.endpoints.update(self.valid_endpoints(endpoints))

        for endpoint in self.endpoints.values():
            endpoint.service = self
        # end for
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Gets the state of the object.

        :return: The state of the object.
        """

        data = super().__getstate__()

        data["app"] = None
        data["server"] = None
        data["_serving_process"] = None

        return data
    # end __getstate__

    @staticmethod
    def valid_endpoints(endpoints: Optional[Any] = None) -> Endpoints:
        """
        Process the endpoints' commands to validate and modify it.

        :param endpoints: The endpoints object to check.

        :return: The valid endpoints object.
        """

        return valid_endpoints(endpoints=endpoints)
    # end valid_endpoints

    @property
    def root(self) -> str:
        """
        Gets the root path of the service.

        :returns: The root path.
        """

        return self._root
    # end get_root

    @root.setter
    def root(self, value: str) -> None:
        """
        Sets the root path of the endpoints and the service.

        :param value: The root path.
        """

        if value == self._root:
            return
        # end if

        if not hasattr(self, "endpoints"):
            raise AttributeError(
                f"{self} must container 'endpoints' "
                f"attribute before attempting to set 'root'"
            )
        # end if

        self._root = value

        for endpoint in self.endpoints.copy().values():
            endpoint.root = self.root

            if endpoint.root:
                self.endpoints.pop(endpoint.path)

                self.endpoints[
                    "/" + endpoint.root + endpoint.path
                ] = endpoint
            # end if
        # end for

        if self.built:
            self.build()
        # end if
    # end set_root

    @property
    def serving(self) -> bool:
        """
        Checks if the service is currently serving.

        :return: The boolean value.
        """

        return self._serving
    # end serving

    @property
    def built(self) -> bool:
        """
        Checks if the service was built.

        :return: The value for the service being built.
        """

        return isinstance(self.app, FastAPI)
    # end built

    @property
    def created(self) -> bool:
        """
        Checks if the service was created.

        :return: The value for the service being created.
        """

        return isinstance(self._serving_process, threading.Thread)
    # end created

    def add_endpoint(self, endpoint: BaseEndpoint, path: Optional[str] = None) -> None:
        """
        Adds the endpoint to the service.

        :param path: The path for the endpoint.
        :param endpoint: The command to run.
        """

        self.endpoints[path or endpoint.path] = endpoint
    # end add_endpoint

    def add_endpoints(self, endpoints: EndpointsContainer) -> None:
        """
        Adds the endpoint to the service.

        :param endpoints: The commands to run.
        """

        self.endpoints.update(self.valid_endpoints(endpoints))
    # end add_endpoints

    def set_endpoint(
            self, endpoint: BaseEndpoint, path: Optional[str] = None
    ) -> None:
        """
        Adds the endpoint to the service.

        :param path: The path for the endpoint.
        :param endpoint: The command to run.
        """

        path = path or endpoint.path

        if path not in self.endpoints:
            raise ValueError(
                f"The path was not initialized for a different "
                f"endpoint beforehand. Consider using "
                f"'{self.add_endpoint.__name__}' method instead, "
                f"to add endpoints with new path. Given path: {path}. "
                f"Valid paths: {', '.join(self.endpoints.keys())}"
            )
        # end if

        self.endpoints[path] = endpoint
    # end set_endpoint

    def remove_endpoint(
            self, *,
            path: Optional[str] = None,
            endpoint: Optional[BaseEndpoint] = None
    ) -> None:
        """
        Removes the endpoint from the service.

        :param path: The index for the endpoint.
        :param endpoint: The command to run.
        """

        if path is not None:
            try:
                self.endpoints.pop(path)

            except KeyError:
                raise ValueError(
                    f"The path was not initialized for a different "
                    f"endpoint beforehand, therefore an endpoint "
                    f"labeled with that path couldn't be removed. Given path: {path}. "
                    f"Valid paths: {', '.join(self.endpoints.keys())}"
                )
            # end try

        elif endpoint is not None:
            for key, value in self.endpoints.items():
                if (value is endpoint) or (value == endpoint):
                    self.endpoints.pop(key)
                # end if

            else:
                raise ValueError(
                    f"Endpoint object '{repr(endpoint)}' doesn't "
                    f"exist in the endpoints of service object {repr(self)}, "
                    f"therefore could not be removed. Given path: {path}. "
                    f"Valid paths: {', '.join(self.endpoints.keys())}"
                )
            # end for
        # end if
    # end remove_endpoint

    def remove_endpoints(
            self, *,
            paths: Optional[Iterable[str]] = None,
            endpoints: Optional[EndpointsContainer] = None
    ) -> None:
        """
        Removes the endpoint from the service.

        :param paths: The paths for the endpoint.
        :param endpoints: The commands to run.
        """

        if paths is not None:
            for path in paths:
                self.remove_endpoint(path=path)
            # end if

        else:
            for endpoint in endpoints:
                self.remove_endpoint(endpoint=endpoint)
            # end for
        # end if
    # end remove_endpoint

    def remove_all_endpoints(self) -> None:
        """Removes all the endpoints from the service."""

        self.endpoints.clear()
    # end remove_all_endpoints

    def update_endpoints(self, endpoints: EndpointsContainer) -> None:
        """
        Adds the endpoint to the service.

        :param endpoints: The commands to run.
        """

        self.endpoints.update(self.valid_endpoints(endpoints))
    # end update_endpoints

    def build(self) -> None:
        """
        Builds the service endpoints.

        :returns: The app object.
        """

        self.app = FastAPI(
            title=self.name,
            description=self.description,
            version=self.version,
            docs_url=None
        )

        router = APIRouter()

        for endpoint in self.endpoints.values():
            endpoint.root = self.root

            path = ("/" + endpoint.root if endpoint.root else '') + endpoint.path

            command = override_signature(
                Endpoint(endpoint.__call__, endpoint),
                new=endpoint.endpoint, name=type(endpoint).__name__
            )

            try:
                router.add_api_route(
                    path, command,
                    methods=endpoint.methods, description=endpoint.description,
                    **endpoint.options
                )

            except fastapi.exceptions.FastAPIError:
                endpoint.options.setdefault('response_model', None)

                router.add_api_route(
                    path, command,
                    methods=endpoint.methods, description=endpoint.description,
                    **endpoint.options
                )
            # end try
        # end for

        root = "/" + self.root if self.root else ''

        if (self.icon is not None) and os.path.exists(self.icon):
            router.add_api_route(
                root + FAVICON, lambda: EndpointFileResponse(self.icon),
                methods=[GET], include_in_schema=False
            )
        # end if

        if isinstance(self.home, bool) and self.home:
            router.add_api_route(
                root + '/', lambda: EndpointRedirectResponse(DOCS),
                methods=[GET], include_in_schema=False
            )
        # end if

        if DOCS not in self.endpoints:
            router.add_api_route(
                root + DOCS, DocsEndpoint(
                    icon=root + FAVICON,
                    methods=[GET], title=self.name
                ).endpoint, methods=[GET], include_in_schema=False
            )
        # end if

        self.app.include_router(router)
    # end build

    def create(
            self,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True
    ) -> None:
        """
        Creates the process to run the api service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        """

        if silent is None:
            silent = self.SILENT
        # end if

        if not self.built:
            self.build()
        # end if

        self.server = Server(
            config=ServiceConfig(
                app=self.app, host=host, port=port
            )
        )

        self._serving_process = threading.Thread(
            target=lambda: (
                (
                    logging.disable(logging.INFO) if silent else ()
                ), self.server.run()
            ), daemon=daemon
        )
    # end create

    def start_serving(
            self,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True
    ) -> None:
        """
        Starts serving the service.

        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        """

        if self.serving:
            warnings.warn(f"Serving process of {self} is already running.")

            return
        # end if

        if not self.created:
            self.create(
                host=host, port=port, silent=silent,
                daemon=daemon
            )
        # end if

        self._serving = True

        self._serving_process.start()
    # end start_serving

    def run(
            self,
            serve: Optional[bool] = True,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            refresh: Optional[Union[Number, dt.timedelta]] = True,
            wait: Union[Number, dt.timedelta, dt.datetime] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the api service.

        :param serve: The value to start serving.
        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the system.
        :param update: The value to update the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        self._running_parameters = dict(
            host=host, port=port, serve=serve,
            silent=silent, daemon=daemon, wait=wait,
            update=update, refresh=refresh,
            timeout=timeout, block=block
        )

        if serve:
            self.start_serving(
                host=host, port=port,
                silent=silent, daemon=daemon
            )
        # end if

        super().run(
            update=update, refresh=refresh,
            block=block, wait=wait, timeout=timeout
        )
    # end run

    def rerun(
            self,
            serve: Optional[bool] = True,
            host: Optional[Host] = None,
            port: Optional[Port] = None,
            silent: Optional[bool] = None,
            daemon: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            refresh: Optional[Union[Number, dt.timedelta]] = True,
            wait: Union[Number, dt.timedelta, dt.datetime] = None,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the api service.

        :param serve: The value to start serving.
        :param host: The host of the server.
        :param port: The port of the server.
        :param silent: The value to silent the output.
        :param daemon: The value to set the process as daemon.
        :param block: The value to block the execution and wain for the service.
        :param refresh: The value to refresh the system.
        :param update: The value to update the service.
        :param wait: The waiting time.
        :param timeout: The start_timeout for the process.
        """

        self.terminate()

        parameters = dict(
            host=host, port=port, serve=serve,
            silent=silent, daemon=daemon, wait=wait,
            update=update, refresh=refresh,
            timeout=timeout, block=block
        )

        parameters = {
            key: value for key, value in parameters.items()
            if value is not None
        }

        self._running_parameters.update(parameters)

        self.run(**self._running_parameters)
    # end rerun

    def stop_serving(self) -> None:
        """Stops the service process."""

        if self.serving:
            self._serving = False
        # end if

        if self.created and self._serving_process.is_alive():
            self._serving_process = None
        # end if
    # end stop_serving

    def terminate(self) -> None:
        """Pauses the process of service."""

        super().terminate()

        self.stop_serving()
    # end terminate
# end BaseService