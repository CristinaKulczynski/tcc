from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from docx import Document as WordDocument
import fitz  # PyMuPDF

SUPPORTED_EXTENSIONS = {".docx", ".pdf"}


def validate_supported_file_type(file_path: Path) -> None:
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato não suportado: {file_path.suffix}. Use .docx ou .pdf")
    if not file_path.is_file():
        raise FileNotFoundError(str(file_path))


# -------- DOCX --------
def extract_docx_text(file_path: Path) -> str:
    doc = WordDocument(str(file_path))
    text_parts: list[str] = []

    # corpo principal
    for p in doc.paragraphs:
        if p.text:
            text_parts.append(p.text)

    # tabelas
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text_parts.append(cell.text.strip())

    # cabeçalhos e rodapés
    for sec in doc.sections:
        for header_paragraph in sec.header.paragraphs:
            if header_paragraph.text:
                text_parts.append(header_paragraph.text)
        for footer_paragraph in sec.footer.paragraphs:
            if footer_paragraph.text:
                text_parts.append(footer_paragraph.text)

    return "\n".join(text_parts)


def count_docx_images(file_path: Path) -> int:
    doc = WordDocument(str(file_path))
    rel_parts = getattr(doc.part, "related_parts", {})
    return sum(1 for p in rel_parts.values() if getattr(p, "content_type", "").startswith("image/"))


# -------- PDF --------
def extract_pdf_text(file_path: Path) -> str:
    with fitz.open(str(file_path)) as pdf:
        return "\n".join(page.get_text("text") for page in pdf)


def count_pdf_images(file_path: Path) -> int:
    with fitz.open(str(file_path)) as pdf:
        xrefs = set()
        for page in pdf:
            for img in page.get_images(full=True):
                xrefs.add(img[0])
        return len(xrefs)


def get_pdf_pages(file_path: Path) -> int:
    with fitz.open(str(file_path)) as pdf:
        return pdf.page_count


# -------- Orquestrador --------
def extract_document_properties(file_path: Path) -> Dict[str, Any]:
    validate_supported_file_type(file_path)
    ext = file_path.suffix.lower()

    if ext == ".docx":
        text = extract_docx_text(file_path)
        images = count_docx_images(file_path)
        pages = None  # ainda será tratado depois
    else:
        text = extract_pdf_text(file_path)
        images = count_pdf_images(file_path)
        pages = get_pdf_pages(file_path)

    # Contadores simples de caracteres
    char_count = 0
    char_no_space = 0
    for ch in text:
        char_count += 1
        if not ch.isspace():
            char_no_space += 1

    return {
        "characters_count": char_count,
        "characters_no_space_count": char_no_space,
        "pages_count": pages,
        "images_count": images,
    }
