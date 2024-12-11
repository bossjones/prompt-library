"""
This type stub file was generated by pyright.
"""

import abc
from typing import Awaitable, Callable, Optional, Protocol, TYPE_CHECKING, Union
from starlette.types import ASGIApp, Receive, Scope, Send

if TYPE_CHECKING:
    ...
LOGGER = ...
class MiddlewareFactory(Protocol):
    def __call__(self, app: ASGIApp) -> ASGIApp:
        ...



class ASGIAppBuilder(abc.ABC):
    """
    Class for building ASGI applications.

    Methods:
        with_app(
            path: str,
            root: str,
            middleware: Optional[list[MiddlewareFactory]] = None,
        ) -> ASGIAppBuilder:
            Adds a static application to the ASGI app at the specified path.

            Args:
                path (str): The URL path where the application will be mounted.
                root (str): The root directory of the application.
                middleware (Optional[list[MiddlewareFactory]]): Middleware to apply to the application.

        with_dynamic_directory(
            path: str,
            directory: str,
            validate_callback: Optional[ValidateCallback] = None,
            middleware: Optional[list[MiddlewareFactory]] = None,
        ) -> ASGIAppBuilder:
            Adds a dynamic directory to the ASGI app, allowing for dynamic loading of applications from the specified directory.

            Args:
                path (str): The URL path where the dynamic directory will be mounted.
                directory (str): The directory containing the applications.
                validate_callback (Optional[ValidateCallback]): A callback function to validate the application path.
                    This is useful to plug in authentication or authorization checks.
                    The validate_callback receives the application path and the scope,
                    and returns a boolean indicating whether the application is valid.
                    You may also raise an exception for a custom error message.
                middleware (Optional[list[MiddlewareFactory]]): Middleware to apply to sub app.

        build() -> ASGIApp:
            Builds and returns the final ASGI application.
    """
    @abc.abstractmethod
    def with_app(self, *, path: str, root: str, middleware: Optional[list[MiddlewareFactory]] = ...) -> ASGIAppBuilder:
        """
        Adds a static application to the ASGI app at the specified path.

        Args:
            path (str): The URL path where the application will be mounted.
            root (str): The root directory of the application.
            middleware (Optional[list[MiddlewareFactory]]): Middleware to apply to the application.

        Returns:
            ASGIAppBuilder: The builder instance for chaining.
        """
        ...

    @abc.abstractmethod
    def with_dynamic_directory(self, *, path: str, directory: str, validate_callback: Optional[ValidateCallback] = ..., middleware: Optional[list[MiddlewareFactory]] = ...) -> ASGIAppBuilder:
        """
        Adds a dynamic directory to the ASGI app, allowing for dynamic loading of applications from the specified directory.

        Args:
            path (str): The URL path where the dynamic directory will be mounted.
            directory (str): The directory containing the applications.
            validate_callback (Optional[ValidateCallback]): A callback function to validate the application path.
                This is useful to plug in authentication or authorization checks.
                The validate_callback receives the application path and the scope,
                and returns a boolean indicating whether the application is valid.
                You may also raise an exception for a custom error message.
            middleware (Optional[list[MiddlewareFactory]]): Middleware to apply to sub app. `marimo_app_file`
            is added to the scope of the request, so middleware can access it.

        Returns:
            ASGIAppBuilder: The builder instance for chaining.
        """
        ...

    @abc.abstractmethod
    def build(self) -> ASGIApp:
        """
        Builds and returns the final ASGI application.

        Returns:
            ASGIApp: The built ASGI application.
        """
        ...



ValidateCallback: TypeAlias = Callable[[str, "Scope"], Union[Awaitable[bool], bool]]
class DynamicDirectoryMiddleware:
    def __init__(self, app: ASGIApp, base_path: str, directory: str, app_builder: Callable[[str, str], ASGIApp], validate_callback: Optional[ValidateCallback] = ...) -> None:
        ...

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...



def create_asgi_app(*, quiet: bool = ..., include_code: bool = ..., token: Optional[str] = ...) -> ASGIAppBuilder:
    """
    Public API to create an ASGI app that can serve multiple notebooks.
    This only works for application that are in Run mode.

    **Examples.**

    You can create an ASGI app, and serve the application with a
    server like `uvicorn`:

    ```python
    import uvicorn

    builder = (
        create_asgi_app()
        .with_app(path="/app", root="app.py")
        .with_app(path="/app2", root="app2.py")
        .with_app(path="/", root="home.py")
    )
    app = builder.build()

    if __name__ == "__main__":
        uvicorn.run(app, port=8000)
    ```

    Or you can further integrate it with a FastAPI app:

    ```python
    import uvicorn
    from fastapi import FastAPI
    import my_middlewares
    import my_routes

    app = FastAPI()

    builder = (
        create_asgi_app()
        .with_app(path="/app", root="app.py")
        .with_app(path="/app2", root="app2.py")
    )

    # Add middlewares
    app.add_middleware(my_middlewares.auth_middleware)


    # Add routes
    @app.get("/login")
    async def root():
        pass


    # Add the marimo app
    app.mount("/", builder.build())

    if __name__ == "__main__":
        uvicorn.run(app, port=8000)
    ```

    You may also want to dynamically load notebooks from a directory. To do
    this, use the `with_dynamic_directory` method. This is useful if the
    contents of the directory change often without requiring a server restart.

    ```python
    import uvicorn

    builder = create_asgi_app().with_dynamic_directory(
        path="/notebooks", directory="./notebooks"
    )
    app = builder.build()

    if __name__ == "__main__":
        uvicorn.run(app, port=8000)
    ```

    **Args.**

    - quiet (bool, optional): Suppress standard out
    - include_code (bool, optional): Include notebook code in the app
    - token (str, optional): Auth token to use for the app.
        If not provided, an empty token is used.

    **Returns.**

    - ASGIAppBuilder: A builder object to create multiple ASGI apps
    """
    class Builder(ASGIAppBuilder):
        ...
