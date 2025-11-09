import re
from typing import Dict, Any, List

ORCID_REGEX = re.compile(
    r"(?:https?://orcid\.org/)?\b\d{4}-\d{4}-\d{4}-\d{3}[0-9X]\b"
)
LATTES_REGEX = re.compile(
    r"https?://lattes\.cnpq\.br/[0-9]{10,}"
)
AFILIACAO_REGEX = re.compile(
    r"(Universidade|Centro|Hospital|Instituto|Faculdade)[^\n]{0,100}?(?:, ?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+, ?[A-Z]{2}|, ?Brazil|, ?Brasil)",
    re.IGNORECASE,
)
BIO_REGEX = re.compile(
    r"(Médic|Enfermeir|Farmacêutic|Professor|Pesquisador|Doutor|Graduad|Especialista)",
    re.IGNORECASE,
)

def extrair_bloco_autoria(texto: str) -> str:
    inicio = 0
    for padrao in [r"(?i)(ORCID|Universidade|Instituto|Centro|Hospital)"]:
        m = re.search(padrao, texto)
        if m:
            inicio = max(0, texto.rfind("\n", 0, m.start()))
            break
    fim = texto.find("RESUMO")
    if fim == -1:
        fim = texto.find("ABSTRACT")
    if fim == -1:
        fim = len(texto)
    return texto[inicio:fim].strip()

def extrair_autores(bloco: str) -> List[str]:
    candidatos = re.split(r"[\n;,]", bloco)
    nomes = []
    for c in candidatos:
        c = c.strip()
        if len(c) > 5 and re.search(r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+ [A-ZÁÉÍÓÚÂÊÔÃÕÇ]", c):
            nomes.append(c)
    return nomes

def validar_metadados(texto: str) -> Dict[str, Any]:
    bloco = extrair_bloco_autoria(texto)
    autores = extrair_autores(bloco)
    qtd = len(autores)

    orcids = re.findall(ORCID_REGEX, texto)
    lattes = re.findall(LATTES_REGEX, texto)
    afiliacoes = re.findall(AFILIACAO_REGEX, texto)
    bios = re.findall(BIO_REGEX, texto)

    status = {
        "1_autores_limite": "Atende" if 1 <= qtd <= 6 else "Não atende",
        "2_nomes_completos": "Atende" if qtd > 0 and all(" " in a for a in autores) else "Não atende",
        "3_orcid_lattes": (
            "Atende"
            if qtd > 0 and (len(orcids) >= qtd or len(lattes) >= qtd)
            else "Atende Parcialmente"
            if orcids or lattes
            else "Não atende"
        ),
        "4_afiliacao_cidade_uf": "Atende" if afiliacoes else "Não atende",
        "5_resumo_biografico": "Atende" if bios else "Não atende",
    }

    return {
        "autores": autores,
        "orcids": orcids,
        "lattes": lattes,
        "afiliacoes": afiliacoes,
        "bios_detectadas": bios,
        "status": status,
    }

if __name__ == "__main__":
    import sys, json
    from pathlib import Path
    caminho = Path(sys.argv[1])
    texto = caminho.read_text(encoding="utf-8", errors="ignore")
    print(json.dumps(validar_metadados(texto), ensure_ascii=False, indent=2))
