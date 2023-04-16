from __future__ import annotations

from typing import Iterable

from fastapi import FastAPI
from starlette.routing import Mount
from app.main import app


def gen_routes(app: FastAPI | Mount) -> Iterable[tuple[str, str]]:
    for route in app.routes:
        if isinstance(route, Mount):
            yield from (
                (f"{route.path}{path}", name) for path, name in gen_routes(route)
            )
        else:
            yield (
                route.path,
                "{}.{}".format(route.endpoint.__module__, route.endpoint.__qualname__),
            )


def list_routes(app: FastAPI) -> None:
    import tabulate

    routes = sorted(set(gen_routes(app)))  # also readable enough
    print(tabulate.tabulate(routes, headers=["path", "full name"]))


if __name__ == "__main__":
    list_routes(app)
