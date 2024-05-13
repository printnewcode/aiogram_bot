from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin_filter import AdminFilter

router = Router(name=__name__)


@router.message(Command("stats"))
@router.message(~AdminFilter(is_admin=True))
async def stats(message: Message, db) -> None:

    """ Отвечает на команду /stats. Отправляет количество пользователей. """
    answer = await db.counting()
    await message.answer(f"Количество пользователей в боте: {str(answer)}")
