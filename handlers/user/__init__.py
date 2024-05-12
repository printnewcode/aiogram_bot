from aiogram import Router


def get_user_handlers_router() -> Router:
    from handlers.user import get_text_from_pdf, get_text_from_docx, document_handling, start

    user_router = Router()

    user_router.include_routers(
        get_text_from_pdf.router,
        get_text_from_docx.router,
        document_handling.router,
        start.router
    )

    return user_router
