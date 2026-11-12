"""Confere o wheel e executa o pacote instalado fora da árvore de fontes."""

import os
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from pathlib import Path

from verificar_segredos import verificar

ROOT = Path(__file__).resolve().parents[1]
PACOTE = {
    "ecommerce_devops/__init__.py",
    "ecommerce_devops/api.py",
    "ecommerce_devops/dominio.py",
    "ecommerce_devops/static/index.html",
    "ecommerce_devops/static/app.js",
    "ecommerce_devops/static/style.css",
}
METADADOS = {"METADATA", "WHEEL", "top_level.txt", "RECORD"}


def main() -> int:
    versao = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    wheels = list((ROOT / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit("Esperado exatamente um wheel em dist/.")
    wheel = wheels[0]
    prefixo = f"ecommerce_devops_academico-{versao}.dist-info/"
    with zipfile.ZipFile(wheel) as arquivo:
        nomes = set(arquivo.namelist())
        extras = nomes - PACOTE
        if (
            not PACOTE <= nomes
            or not extras
            or any(
                not nome.startswith(prefixo) or nome.removeprefix(prefixo) not in METADADOS
                for nome in extras
            )
        ):
            raise SystemExit("Conteúdo inesperado no wheel. Revisar antes de distribuir.")
        for nome in nomes:
            conteudo = arquivo.read(nome).decode("utf-8")
            if verificar(nome, conteudo):
                raise SystemExit("Padrão sensível detectado no wheel; conteúdo omitido.")
    with tempfile.TemporaryDirectory(prefix="loja-validacao-") as pasta:
        destino = str(Path(pasta) / "instalado")
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "--isolated",
                "install",
                "--no-index",
                "--no-deps",
                "--target",
                destino,
                str(wheel),
            ],
            cwd=pasta,
            env=env,
            check=True,
            capture_output=True,
            timeout=60,
        )
        # -I ignora diretório atual e PYTHONPATH. As dependências fixadas já estão
        # no ambiente; a origem da aplicação deve ser o wheel recém-instalado.
        codigo = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import ecommerce_devops
assert Path(ecommerce_devops.__file__).resolve().is_relative_to(Path(sys.argv[1]))
from fastapi.testclient import TestClient
from ecommerce_devops.api import create_app
with TestClient(create_app()) as client:
    assert client.get('/health').status_code == 200
    assert client.get('/').status_code == 200
    assert client.get('/static/app.js').status_code == 200
    r = client.post('/pedidos', json={'itens': [{'produto_id': 1, 'quantidade': 2}]})
    assert r.status_code == 201 and r.json()['total_centavos'] == 3180
"""
        subprocess.run(
            [sys.executable, "-I", "-c", codigo, destino],
            cwd=pasta,
            env=env,
            check=True,
            capture_output=True,
            timeout=30,
        )
    print(f"Wheel {versao}: conteúdo conferido, instalação e fluxo HTTP aprovados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
