from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from handlers.user.get_text_from_docx import extract_text_from_docx
from handlers.user.get_text_from_pdf import extract_text_from_pdf
from services.settings import DEBUG

router = Router(name=__name__)


@router.message(F.document)
async def document_handling(message: Message, bot: Bot) -> None:
    """
    Достает из файла docx или pdf текст

    (при помощи функций extract_text_from_docx и extract_text_from_docx)

     и возврщает его пользователю
    """
    file_id = message.document.file_id  # Достаем file_id из отправленного документа
    file = await bot.get_file(file_id)
    file_path = file.file_path  # Получаем file_path
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
