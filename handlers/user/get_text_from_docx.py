from aiogram import Router, F
from docx import Document

router = Router(name=__name__)


@router.message(F.document)
async def extract_text_from_docx(doc) -> str:
    """ Перебирает весь документ docx, достает текст и возвращает его. """
    document = Document(doc)

    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    return text
