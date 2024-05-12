from aiogram import Router
from aiogram.types import Message

from filters.admin_filter import AdminFilter
from services.settings import ADMIN_LIST

router = Router(name=__name__)


@router.message(AdminFilter(is_admin=True))
async def stats(message: Message, db) -> None:
    """ Отвечает на команду /stats. Отправляет количество пользователей. """
    user_id = message.from_user.id
    if user_id in ADMIN_LIST:
        answer = await db.counting()
        await message.answer(f"Количество пользователей в боте: {str(answer)}")
    else:
        await message.answer("Отказано в доступе")
