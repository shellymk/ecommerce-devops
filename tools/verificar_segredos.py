"""Barreira básica: confere o conteúdo do índice Git, sem imprimir valores.

Não cobre o histórico nem todos os formatos de segredos ou dados pessoais.
"""

import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGRAS = {
    "chave privada": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "token GitHub": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "identificador AWS": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "credencial atribuída": re.compile(
        r"(?i)\b(?:password|passwd|senha|api[_-]?key|access[_-]?token|secret[_-]?key)"
        r"\s*[:=]\s*[\"'][^\s\"']{8,}[\"']"
    ),
    "caminho pessoal Windows": re.compile(r"(?i)[a-z]:[\\/]Users[\\/](?!Public[\\/])"),
}
NOMES_PROIBIDOS = {
    ".env",
    "credentials.json",
    "secrets.json",
    ".netrc",
    ".pypirc",
    "pip.conf",
    "pip.ini",
}
PASTAS_PROIBIDAS = {".ssh", ".aws", ".secrets", ".venv", "venv", "evidencias-locais"}
EXTENSOES_PROIBIDAS = {".pem", ".key", ".p12", ".pfx"}
IMAGENS_PERMITIDAS = {
    "src/ecommerce_devops/static/imagens/caderno.png": (
        "3cbe2b8df20913c47c6004529f0edc2e05fde1a9e8f01969c9a04d1c826eba36"
    ),
    "src/ecommerce_devops/static/imagens/caneca.png": (
        "6b98a3e2b47b0b3ab7b0d19113f0eb667a75205de40ef3774a0b7f948d4f1f3b"
    ),
    "src/ecommerce_devops/static/imagens/caneta.png": (
        "65ec06603f5e15dae8672784127eb8bfa974e639e5b15e82be61007ca1c007ae"
    ),
}


def verificar(nome: str, conteudo: str) -> list[str]:
    caminho = Path(nome)
    problemas = []
    if (
        caminho.name.lower() in NOMES_PROIBIDOS
        or caminho.name.lower().startswith(".env.")
        or caminho.suffix.lower() in EXTENSOES_PROIBIDAS
        or any(parte.lower() in PASTAS_PROIBIDAS for parte in caminho.parts)
    ):
        problemas.append("arquivo local ou sensível no Git")
    for regra, padrao in REGRAS.items():
        if padrao.search(conteudo):
            problemas.append(regra)
    return problemas


def verificar_arquivo(nome: str, dados: bytes) -> list[str]:
    problemas = verificar(nome, "")
    if nome in IMAGENS_PERMITIDAS:
        if hashlib.sha256(dados).hexdigest() != IMAGENS_PERMITIDAS[nome]:
            problemas.append("imagem diferente da versão ilustrativa revisada")
        return problemas
    try:
        conteudo = dados.decode("utf-8")
        if "\x00" in conteudo:
            raise UnicodeDecodeError("utf-8", dados, 0, 1, "conteúdo binário")
    except UnicodeDecodeError:
        return problemas + ["arquivo binário fora do escopo desta verificação"]
    return verificar(nome, conteudo)


def git(*argumentos: str) -> bytes:
    return subprocess.run(
        ["git", *argumentos], cwd=ROOT, capture_output=True, check=True, timeout=30
    ).stdout


def main() -> int:
    try:
        # Lê o índice, inclusive mudanças preparadas ainda sem commit.
        nomes = git("ls-files", "--cached", "-z").decode("utf-8").split("\0")
        nomes = [nome for nome in nomes if nome]
        if not nomes:
            print("Nenhum arquivo no índice Git. Adicione os arquivos antes de conferir.")
            return 1
        falhou = False
        for nome in nomes:
            dados = git("show", f":{nome}")
            for problema in verificar_arquivo(nome, dados):
                print(f"REVISAR: {nome}: {problema}; conteúdo omitido")
                falhou = True
        if falhou:
            return 1
        print(f"Verificação básica: {len(nomes)} arquivos conferidos; nenhum padrão detectado.")
        return 0
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("Não foi possível conferir o índice Git. Execute na pasta do projeto após git add.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
