import argparse
import json
import logging
import sys
from pathlib import Path

from src.io_reader_docx import extract_document_properties_docx
from src.io_reader_pdf import extract_document_properties_pdf
from src.extrair_dados_doc import dump_docx_xmls
from src.structure import detectar_secoes

# Testando novas funcionalidades de logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("reci-checker")

def main() -> int:
    parser_argumentos = argparse.ArgumentParser(description="Extrai propriedades de arquivos .docx ou .pdf")
    parser_argumentos.add_argument("caminho_arquivo", help="Caminho para o manuscrito")
    argumentos = parser_argumentos.parse_args()

    caminho_manuscrito = Path(argumentos.caminho_arquivo)
    if not caminho_manuscrito.is_file():
        logger.error("Arquivo não encontrado: %s", caminho_manuscrito)
        return 2

    extensao = caminho_manuscrito.suffix.lower()
    if extensao not in [".docx", ".pdf"]:
        logger.error("Formato inválido (%s). Use apenas .docx ou .pdf", extensao)
        return 3

    if extensao == ".docx":
        dump_docx_xmls(caminho_manuscrito)
        propriedades = extract_document_properties_docx(caminho_manuscrito)
    else:
        propriedades = extract_document_properties_pdf(caminho_manuscrito)

    texto = propriedades.get("text", "")
    if texto:
        propriedades["sections"] = detectar_secoes(texto)

    # Remove o texto completo do output final
    propriedades.pop("text", None)

    print(json.dumps(propriedades, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
