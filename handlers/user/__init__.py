from aiogram import Router


def get_user_handlers_router() -> Router:
    from handlers.user import parser, start

    user_router = Router()

    user_router.include_routers(
        parser.router,
        start.router
    )

    return user_router
