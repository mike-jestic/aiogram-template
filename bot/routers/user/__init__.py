from ...utils.router import Router
from .. import root_handlers_router


router = Router()

root_handlers_router.include_router(router)
