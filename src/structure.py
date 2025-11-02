import re
from typing import Dict

# Detecta seções em textos de artigos científicos multilíngues
def detectar_secoes(texto: str) -> Dict[str, str]:
    # Normaliza quebras e espaços
    texto = re.sub(r"\s+", " ", texto.strip())

    # Padrões multilíngues de títulos de seção
    padroes = {
   
    "TÍTULO / ORIGINAL ARTICLE": r"(?:(?:^|[\n\r\s])(?:ARTIGO\s*ORIGINAL|ORIGINAL\s*ARTICLE|T[ÍI]TULO))(?=\s|$)",
   
    "RESUMO": r"(?:(?:^|[\n\r\s])RESUMO)(?=\s|$)",
   
    "ABSTRACT": r"(?:(?:^|[\n\r\s])ABSTRACT)(?=\s|$)",
    "RESUMEN": r"(?:(?:^|[\n\r\s])RESUMEN)(?=\s|$)",
    "RESUMEN": r"(?:^|[\.\n])\s*RESUMEN\s+(?=[A-Z])",
    "INTRODUÇÃO / INTRODUCTION": r"(?:^|[\.\n])\s*INTRODU[CÇ][AÃ]O\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|(?:^|[\.\n])\s*INTRODUCTION\s+(?=[A-Z])",
    "MÉTODOS / METHODS": r"(?:^|[\.\n])\s*M[ÉE]TODOS?\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|(?:^|[\.\n])\s*METHODS?\s+(?=[A-Z])",
    "RESULTADOS / RESULTS": r"(?:^|[\.\n])\s*RESULTADOS?\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|(?:^|[\.\n])\s*RESULTS?\s+(?=[A-Z])",
    "DISCUSSÃO / DISCUSSION": r"(?:^|[\.\n])\s*DISCUSS[AÃ]O\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|(?:^|[\.\n])\s*DISCUSSION\s+(?=[A-Z])",
    "CONCLUSÃO / CONCLUSION": r"(?:^|[\.\n])\s*CONCLUS[AÃ]O\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])|(?:^|[\.\n])\s*CONCLUSION\s+(?=[A-Z])|(?:^|[\.\n])\s*CONSIDERA[CÇ][OÕ]ES\s*FINAIS\s+(?=[A-Z])",
    "REFERÊNCIAS / REFERENCE": r"(?:^|[\.\n])\s*REFER[ÊE]NCIAS\s*(?=$|\s)|(?:^|[\.\n])\s*REFERENCE[S]?\s*(?=$|\s)|(?:^|[\.\n])\s*BIBLIOGRAFIA\s*(?=$|\s)",
  }




    # Localiza posições de cada seção
    indices = []
    for nome, regex in padroes.items():
        for m in re.finditer(regex, texto, flags=re.IGNORECASE):
            indices.append((m.start(), nome))
    indices.sort(key=lambda x: x[0])

    # Divide o texto em blocos delimitados
    secoes = {}
    for i, (pos, nome) in enumerate(indices):
        fim = indices[i + 1][0] if i + 1 < len(indices) else len(texto)
        bloco = texto[pos:fim].strip()
        secoes[nome] = bloco

    return secoes


# Execução isolada: python src/structure.py caminho.txt
if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Uso: python src/structure.py caminho_arquivo.txt")
        sys.exit(1)

    caminho = Path(sys.argv[1])
    if not caminho.is_file():
        print("Arquivo não encontrado.")
        sys.exit(1)

    conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
    secoes = detectar_secoes(conteudo)

    for nome, trecho in secoes.items():
        print(f"\n=== {nome} ===")
        print(trecho[:600], "..." if len(trecho) > 600 else "")
