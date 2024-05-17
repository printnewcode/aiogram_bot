from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name=__name__)


@router.message(CommandStart)
async def start(message: Message, db) -> None:
    """ Отправляет приветственное сообщение, записывает пользователя в database. """
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(text="Привет! Отправь мне файл с расширением .docx или .pdf и я достану из него текст.")
    await db.create_tables()
    await db.adding_user(username, user_id)
