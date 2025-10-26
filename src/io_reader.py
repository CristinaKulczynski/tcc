from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from docx import Document as WordDocument
import fitz  


SUPPORTED_EXTENSIONS = {".docx", ".pdf"}


def validate_supported_file_type(file_path: Path) -> None:
    """Verifica se o arquivo existe e possui extensão suportada (.docx ou .pdf)."""
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato não suportado: {file_path.suffix}. Use .docx ou .pdf")
    if not file_path.is_file():
        raise FileNotFoundError(str(file_path))


def extract_full_text(file_path: Path) -> str:
    """Extrai e retorna todo o texto de um arquivo .docx ou .pdf."""
    validate_supported_file_type(file_path)
    file_extension = file_path.suffix.lower()

    if file_extension == ".docx":
        word_document = WordDocument(str(file_path))
        document_paragraphs_and_cells: list[str] = [
            paragraph.text for paragraph in word_document.paragraphs if paragraph.text
        ]

        for table in word_document.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        document_paragraphs_and_cells.append(cell_text)
        return "\n".join(document_paragraphs_and_cells)


    with fitz.open(str(file_path)) as pdf_document:
        extracted_pages = [page.get_text("text") for page in pdf_document]
        return "\n".join(extracted_pages)


def count_embedded_images(file_path: Path) -> int:
    """Conta o número de imagens incorporadas em um .docx ou .pdf."""
    validate_supported_file_type(file_path)
    file_extension = file_path.suffix.lower()

    if file_extension == ".docx":
        word_document = WordDocument(str(file_path))
        related_parts = getattr(word_document.part, "related_parts", {})
        image_count = sum(
            1 for part in related_parts.values()
            if getattr(part, "content_type", "").startswith("image/")
        )
        return image_count


    with fitz.open(str(file_path)) as pdf_document:
        unique_image_references = set()
        for page in pdf_document:
            for image in page.get_images(full=True):
                unique_image_references.add(image[0])  # xref (cross-reference)
        return len(unique_image_references)


def extract_document_properties(file_path: Path) -> Dict[str, Any]:
    """Extrai propriedades normalizadas do documento: número de caracteres, páginas e imagens."""
    validate_supported_file_type(file_path)
    file_extension = file_path.suffix.lower()

    if file_extension == ".docx":
        word_document = WordDocument(str(file_path))
        total_pages = None  
    else:
        with fitz.open(str(file_path)) as pdf_document:
            total_pages = pdf_document.page_count

    full_text_content = extract_full_text(file_path)
    total_image_count = count_embedded_images(file_path)

    return {
        "characters_count": len(full_text_content),
        "pages_count": total_pages,
        "images_count": total_image_count
    }
