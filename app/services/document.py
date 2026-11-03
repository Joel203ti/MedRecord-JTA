from io import BytesIO
from pypdf import PdfReader
def extract_pdf_text(data: bytes) -> str:
    reader=PdfReader(BytesIO(data))
    pages=[]
    for i,page in enumerate(reader.pages,1):
        pages.append(f"[Página {i}]\n{page.extract_text() or ''}")
    return "\n\n".join(pages)
