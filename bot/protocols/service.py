from typing import Protocol


class Service(Protocol):
    async def setup(self) -> None:
        ...

    async def dispose(self) -> None:
        ...
