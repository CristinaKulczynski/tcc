import argparse
import json
import logging
import sys
from pathlib import Path

from src.io_reader_docx import extract_document_properties_docx
from src.io_reader_pdf import extract_document_properties_pdf
from src.extrair_dados_doc import dump_docx_xmls
from src.structure import detectar_secoes
from src.checks.metadata import validar_metadados

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("reci-checker")

def main() -> int:
    parser = argparse.ArgumentParser(description="Extrai propriedades e valida metadados de arquivos .docx/.pdf")
    parser.add_argument("caminho_arquivo", help="Caminho para o manuscrito (.docx ou .pdf)")
    args = parser.parse_args()

    caminho = Path(args.caminho_arquivo)
    if not caminho.is_file():
        logger.error("Arquivo não encontrado: %s", caminho)
        return 2

    extensao = caminho.suffix.lower()
    if extensao not in [".docx", ".pdf"]:
        logger.error("Formato inválido (%s). Use apenas .docx ou .pdf", extensao)
        return 3

    if extensao == ".docx":
        dump_docx_xmls(caminho)
        propriedades = extract_document_properties_docx(caminho)
    else:
        propriedades = extract_document_properties_pdf(caminho)

    texto = propriedades.get("text", "")
    if texto:
        propriedades["sections"] = detectar_secoes(texto)
        propriedades["metadata_validation"] = validar_metadados(texto)

    propriedades.pop("text", None)
    print(json.dumps(propriedades, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
