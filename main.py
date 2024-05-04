import os

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from docx import Document
from dotenv import load_dotenv
import logging
import PyPDF2

from settings import DEBUG

load_dotenv()

logging.basicConfig(level=logging.INFO)  # Включаем логирование
bot = Bot(token=os.getenv("TOKEN"))  # Токен для нашего бота
dp = Dispatcher()  # Активируем диспетчер


@dp.message(Command("start"))
async def start(message: Message):
    """ Отправляет приветственное сообщение. """
    await message.answer(text="Привет! Отправь мне файл с расширением .docx или .pdf и я достану из него текст.")


@dp.message()
async def document_handling(message: Message) -> None:
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
        if e == "Telegram server says - Bad Request: text is too long":
            await message.answer("Файл слишком длинный")
        else:
            if DEBUG:
                await message.answer(f"Упс! Ошибка :{e} ")
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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
