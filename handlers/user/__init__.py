from aiogram import Router


def get_user_handlers_router() -> Router:
    from handlers.user import document_handling, start

    user_router = Router()

    user_router.include_routers(
        document_handling.router,
        start.router
    )

    return user_router
