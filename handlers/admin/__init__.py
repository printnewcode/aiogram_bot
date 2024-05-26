from aiogram import Router
from filters.admin_filter import AdminFilter


def get_admin_handlers_router() -> Router:
    from handlers.admin import stats

    admin_router = Router()
    
    admin_router.message.filter(AdminFilter)
    admin_router.callback_query.filter(AdminFilter)
    
    admin_router.include_router(stats.router)

    return admin_router
