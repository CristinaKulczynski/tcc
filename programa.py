
import argparse
import json
import logging
import sys
from pathlib import Path

from src.io_reader import extract_document_properties

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("reci-checker")


def main() -> int:
   
    
    argument_parser = argparse.ArgumentParser(
        description="Leitura e extração de propriedades de arquivos .docx e .pdf."
    )
    argument_parser.add_argument(
        "file_path",
        help="Caminho completo do manuscrito (.docx ou .pdf) a ser processado."
    )
    parsed_arguments = argument_parser.parse_args()

    manuscript_path = Path(parsed_arguments.file_path)

    if not manuscript_path.is_file():
        logger.error("Arquivo não encontrado: %s", manuscript_path)
        return 2

    if manuscript_path.suffix.lower() not in [".docx", ".pdf"]:
        logger.error(
            "Formato inválido (%s). Use apenas .docx ou .pdf",
            manuscript_path.suffix
        )
        return 3

    document_properties = extract_document_properties(manuscript_path)

    print(json.dumps(document_properties, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
