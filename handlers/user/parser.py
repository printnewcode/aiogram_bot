from os import remove
from typing import Union

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from services.settings import DEBUG

router = Router(name=__name__)


@router.message(F.document)
async def document_handling(message: Message, bot: Bot, doc_reader) -> Union[None, Message]:
    """
                Достает из файла docx или pdf текст

                (при помощи функций extract_text_from_docx и extract_text_from_docx)

                 и возвращает его пользователю
                """
    # Достаем file_id из отправленного документа
    file_id = await doc_reader.get_file_id_to_thread(message)
    print(file_id)
    file = await bot.get_file(str(file_id))
    file_path = file.file_path  # Получаем file_path
    doc = await bot.download_file(file_path)  # Скачиваем документ и записываем его в переменную

    try:
        if file_path.endswith(".docx"):
            text = await doc_reader.docx_to_thread(doc)  # Вызываем функцию для получения текста
        elif file_path.endswith(".pdf"):
            text = await doc_reader.pdf_to_thread(doc)  # Вызываем функцию для получения текста
        else:
            await message.answer("Извините, я могу работать только с файлами .docx и .pdf.")
            return
        if len(text) > 0:
            await message.answer(f"Вот текст из файла:\n\n{text}")  # Отправляем полученный текст
        else:
            await message.answer("Файл пуст :(")

    except TelegramBadRequest:
        return await message.answer("Файл слишком длинный")
    except Exception as _ex:
        if DEBUG:
            return await message.answer(f"Упс! Ошибка: {_ex}")
        else:
            return await message.answer("Ошибка!")

    finally:
        remove(file_path)
