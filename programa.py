import argparse
import logging
from pathlib import Path
import sys

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", handlers=[handler])
log = logging.getLogger("reci-checker")

def main() -> int:
    parser = argparse.ArgumentParser(description="CLI mínimo: carrega arquivo e confirma.")
    parser.add_argument("arquivo", help="Caminho do manuscrito (.docx ou .pdf)")
    args = parser.parse_args()

    arq = Path(args.arquivo)

    if not arq.is_file():
        log.error("Arquivo não encontrado: %s", arq)
        return 2

    if arq.suffix.lower() not in [".docx", ".pdf"]:
        log.error("Formato inválido (%s). Use apenas .docx ou .pdf", arq.suffix)
        return 3

    log.info("OK: arquivo carregado")
    return 0

if __name__ == "__main__":
    sys.exit(main())
