from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)


@router.message(Command("start"))
async def start(message: Message, db) -> None:
    """ Отправляет приветственное сообщение, записывает пользователя в database. """
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(text="Привет! Отправь мне файл с расширением .docx или .pdf и я достану из него текст.")
    await db.adding_user(username, user_id)
