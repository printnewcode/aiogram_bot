import asyncio

from docx import Document
import PyPDF2


class DocumentReader:
    def __init__(self):
        pass

    def get_file_id(self, message):
        file_id = message.document.file_id

    def extract_text_from_docx(self, doc):
        """ Перебирает весь документ docx, достает текст и возвращает его. """
        document = Document(doc)

        text = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return text

    def extract_text_from_pdf(self, doc):
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

    async def to_thread(self):
        await asyncio.to_thread(DocumentReader.extract_text_from_docx)
        await asyncio.to_thread(DocumentReader.extract_text_from_pdf)
