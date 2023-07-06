from typing import Any, Optional

from aiogram import Dispatcher as AiogramDispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.strategy import FSMStrategy

from .service_manager import ServiceManager


class Dispatcher(AiogramDispatcher):
    def __init__(
        self,
        *,
        storage: Optional[BaseStorage] = None,
        fsm_strategy: FSMStrategy = FSMStrategy.USER_IN_CHAT,
        events_isolation: Optional[BaseEventIsolation] = None,
        disable_fsm: bool = False,
        name: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            storage=storage,
            fsm_strategy=fsm_strategy,
            events_isolation=events_isolation,
            disable_fsm=disable_fsm,
            name=name,
            **kwargs
        )

        self.services = ServiceManager()
