import os

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
import asyncio
from docx import Document
from dotenv import load_dotenv
import logging
import PyPDF2
from sqlalchemy.ext.asyncio import create_async_engine

from base1 import RelationalDatabase as RelatDb
# from base1 import adding_data, counting
from settings import DEBUG, ADMIN_LIST

load_dotenv()

router = Router()

logging.basicConfig(level=logging.INFO)  # Включаем логирование


@router.message(Command("start"))
async def start(message: Message, engine) -> None:
    """ Отправляет приветственное сообщение, записывает пользователя в database. """
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(text="Привет! Отправь мне файл с расширением .docx или .pdf и я достану из него текст.")
    await RelatDb(engine).adding_data(username, user_id)


@router.message(Command("stats"))
async def stats(message: Message, engine) -> None:
    """ Отвечает на команду /stats. Отправляет количество пользователей. """
    user_id = message.from_user.id
    if user_id in ADMIN_LIST:
        answer = await RelatDb(engine).counting()
        await message.answer(f"Количество пользователей в боте: {str(answer)}")
    else:
        await message.answer("Отказано в доступе")


@router.message()
async def document_handling(message: Message, bot: Bot) -> None:
    """
    Достает из файла docx или pdf текст

    (при помощи функций extract_text_from_docx и extract_text_from_docx)

     и возврщает его пользователю
    """
    file_id = message.document.file_id  # Достаем file_id из отправленного документа
    file = await bot.get_file(file_id)
    file_path = file.file_path  # Получаем file_path с помощью getfile
    doc = await bot.download_file(file_path)  # Скачиваем документ и записываем его в переменную

    try:
        if file_path.endswith(".docx"):
            text = await extract_text_from_docx(doc)  # Вызываем функцию для получения текста
        elif file_path.endswith(".pdf"):
            text = await extract_text_from_pdf(doc)  # Вызываем функцию для получения текста
        else:
            await message.answer("Извините, я могу работать только с файлами .docx и .pdf.")
            return
        if len(text) > 0:
            await message.answer(f"Вот текст из файла:\n\n{text}")  # Отправляем полученный текст
        else:
            await message.answer("Файл пуст :(")

    except Exception as e:
        if e == TelegramBadRequest:
            await message.answer("Файл слишком длинный")
        else:
            if DEBUG:
                await message.answer(f"Упс! Ошибка: {e}")
            else:
                await message.answer("Ошибка!")


async def extract_text_from_docx(doc) -> str:
    """ Перебирает весь документ docx, достает текст и возвращает его. """
    document = Document(doc)

    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    return text


async def extract_text_from_pdf(doc) -> str:
    """ Перебирает весь документ pdf, достает текст и возвращает его. """
    file = doc

    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page in range(num_pages):
        pdf_page = pdf_reader.pages[page]
        text += pdf_page.extract_text()
    file.close()
    return text


async def main() -> None:
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher(
        bot=bot,
        engine=create_async_engine('postgresql+asyncpg:///base2.db', echo=True)

    )
    dp.include_router(router)
    return await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
