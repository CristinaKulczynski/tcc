from pathlib import Path
from zipfile import ZipFile
import xml.dom.minidom

CORE = "docProps/core.xml"
APP  = "docProps/app.xml"
DOC  = "word/document.xml"

def _read_entry(docx: Path, entry: str) -> str | None:
    with ZipFile(docx) as zf:
        if entry not in zf.namelist():
            return None
        with zf.open(entry) as f:
            raw = f.read().decode("utf-8", errors="replace")
            try:
                return xml.dom.minidom.parseString(raw).toprettyxml(indent="  ")
            except Exception:
                return raw

def dump_docx_xmls(docx_path: Path) -> None:
    core = _read_entry(docx_path, CORE) or ""
    app  = _read_entry(docx_path, APP)  or ""
    doc  = _read_entry(docx_path, DOC)  or ""

    output_dir = Path(__file__).resolve().parent.parent

    (output_dir / "core.xml").write_text(core, encoding="utf-8")
    (output_dir / "app.xml").write_text(app, encoding="utf-8")
    (output_dir / "document.xml").write_text(doc, encoding="utf-8")
