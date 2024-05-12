from aiogram import F, Router
import PyPDF2

router = Router(name=__name__)


@router.message(F.document)
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
