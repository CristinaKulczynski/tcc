import argparse
import json
import logging
import sys
from pathlib import Path

from src.io_reader import extract_document_properties
from src.extrair_dados_doc import dump_docx_xmls  


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("reci-checker")

def main() -> int:
    p = argparse.ArgumentParser(description="Leitura e extração de propriedades de arquivos .docx e .pdf.")
    p.add_argument("file_path", help="Caminho do manuscrito (.docx ou .pdf)")
    args = p.parse_args()

    manuscript = Path(args.file_path)
    if not manuscript.is_file():
        logger.error("Arquivo não encontrado: %s", manuscript); return 2

    ext = manuscript.suffix.lower()
    if ext not in [".docx", ".pdf"]:
        logger.error("Formato inválido (%s). Use apenas .docx ou .pdf", ext); return 3

    if ext == ".docx":
        dump_docx_xmls(manuscript)  # gera *_core.xml, *_app.xml, *_document.xml

    props = extract_document_properties(manuscript)
    print(json.dumps(props, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
