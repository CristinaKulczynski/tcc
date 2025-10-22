import subprocess
import sys
from pathlib import Path

def test_reci_checker_loads_docx(tmp_path: Path):
    
    doc = tmp_path / "manuscrito_teste.docx"
    doc.write_bytes(b"conteudo ficticio")

    completed = subprocess.run(
        [sys.executable, "programa.py", str(doc)],
        capture_output=True,
        text=True
    )

    assert completed.returncode == 0
    assert "OK: arquivo carregado" in completed.stdout
