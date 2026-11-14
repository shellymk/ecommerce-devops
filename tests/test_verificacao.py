import importlib.util
from pathlib import Path

import pytest

arquivo = Path(__file__).resolve().parents[1] / "tools" / "verificar_segredos.py"
spec = importlib.util.spec_from_file_location("verificacao", arquivo)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)
pytestmark = pytest.mark.unit


@pytest.mark.parametrize("nome", [".env", ".env.local", "chave.pem", ".ssh/config", "secrets.json"])
def test_arquivo_local_proibido(nome):
    assert modulo.verificar(nome, "")


def test_detecta_token_sintetico_sem_gravar_credencial():
    sintetico = "gh" + "p_" + "X" * 36
    assert "token GitHub" in modulo.verificar("exemplo.py", sintetico)


def test_detecta_chave_privada_sintetica():
    sintetico = "-----BEGIN " + "PRIVATE KEY-----"
    assert "chave privada" in modulo.verificar("exemplo.txt", sintetico)


def test_codigo_sem_credenciais():
    assert modulo.verificar("operacoes.py", "resultado = 2 + 3") == []


@pytest.mark.parametrize("nome", list(modulo.IMAGENS_PERMITIDAS))
def test_aceita_somente_imagem_revisada(nome):
    dados = (arquivo.parents[1] / nome).read_bytes()
    assert modulo.verificar_arquivo(nome, dados) == []


@pytest.mark.parametrize("nome", list(modulo.IMAGENS_PERMITIDAS))
def test_rejeita_substituicao_de_imagem(nome):
    assert modulo.verificar_arquivo(nome, b"conteudo sintetico diferente")


def test_rejeita_binario_sem_autorizacao():
    assert modulo.verificar_arquivo("outro.png", b"\x89PNG\x00\xff")
