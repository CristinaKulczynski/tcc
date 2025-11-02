from pathlib import Path
from typing import Dict, Any
import fitz  # PyMuPDF
import re
import unicodedata

# Extrai e normaliza todo o texto visível do PDF
def extrair_texto_pdf(caminho_arquivo: Path) -> str:
    with fitz.open(str(caminho_arquivo)) as documento_pdf:
        texto = "".join(pagina.get_text("text") for pagina in documento_pdf)

    # Normaliza para remover combinações Unicode (acentos compostos)
    texto = unicodedata.normalize("NFKC", texto)

    # Remove quebras, tabs, caracteres de controle e espaços invisíveis
    texto = re.sub(r"[\n\r\t\f\v\u200B\u200C\u200D\uFEFF\u00A0\u2028\u2029]", "", texto)

    # Remove hífens automáticos e ligaduras comuns
    texto = texto.replace("­", "").replace("‐", "").replace("–", "-")

    # Remove qualquer caractere de controle não imprimível (ASCII < 32)
    texto = "".join(c for c in texto if unicodedata.category(c)[0] != "C")

    # Reduz espaços múltiplos e remove bordas
    texto = re.sub(r" {2,}", " ", texto).strip()

    return texto

# Conta instâncias de imagens, incluindo duplicadas
def contar_imagens_pdf(caminho_arquivo: Path) -> int:
    with fitz.open(str(caminho_arquivo)) as documento_pdf:
        return sum(len(pagina.get_images(full=True)) for pagina in documento_pdf)

# Conta páginas do PDF
def contar_paginas_pdf(caminho_arquivo: Path) -> int:
    with fitz.open(str(caminho_arquivo)) as documento_pdf:
        return documento_pdf.page_count

# Retorna propriedades gerais do PDF
def extract_document_properties_pdf(caminho_arquivo: Path) -> Dict[str, Any]:
    texto = extrair_texto_pdf(caminho_arquivo)
    imagens = contar_imagens_pdf(caminho_arquivo)
    paginas = contar_paginas_pdf(caminho_arquivo)

    caracteres = len(texto)
    caracteres_sem_espaco = sum(1 for c in texto if not c.isspace())

    return {
        "characters_count": caracteres,
        "characters_no_space_count": caracteres_sem_espaco,
        "pages_count": paginas,
        "images_count": imagens,
    }
