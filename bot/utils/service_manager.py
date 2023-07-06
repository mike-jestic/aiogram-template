import asyncio
import re
from typing import Dict

from ..protocols.service import Service


def snake_case(s: str):
    return "_".join(
        re.sub(
            "([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


class ServiceManager:
    
    def __init__(self):
        self._services: Dict[str, Service] = {}

    def register(self, service: Service):
        service_class_snake_name = snake_case(service.__class__.__name__)
        self._services[service_class_snake_name] = service
        return service

    def unregister(self, service: Service):
        service_class_snake_name = snake_case(service.__class__.__name__)
        del self._services[service_class_snake_name]

    async def setup_all(self):
        if not self._services:
            return

        service_setup_coros = (service.setup() for service in self._services.values())
        await asyncio.gather(*(service_setup_coros))

    async def dispose_all(self):
        if not self._services:
            return

        service_dispose_coros = (
            service.dispose() for service in self._services.values()
        )

        await asyncio.gather(*service_dispose_coros)


    def __getattr__(self, service):
        return self._services[service]
