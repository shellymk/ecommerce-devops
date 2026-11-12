import pytest
from fastapi.testclient import TestClient

from ecommerce_devops.api import create_app

pytestmark = pytest.mark.integration


@pytest.fixture
def client():
    with TestClient(create_app()) as cliente:
        yield cliente


def test_health(client):
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "version": "0.1.0"}


def test_catalogo_e_produto(client):
    assert len(client.get("/produtos").json()) == 3
    resposta = client.get("/produtos/1")
    assert resposta.status_code == 200
    assert resposta.json()["preco_centavos"] == 1590


def test_produto_ausente(client):
    assert client.get("/produtos/999").status_code == 404


def test_fluxo_completo_catalogo_carrinho_pedido(client):
    produto = client.get("/produtos").json()[0]
    corpo = {"itens": [{"produto_id": produto["id"], "quantidade": 2}]}
    carrinho = client.post("/carrinho", json=corpo)
    assert carrinho.status_code == 200
    assert carrinho.json()["total_centavos"] == 3180
    pedido = client.post("/pedidos", json=corpo)
    assert pedido.status_code == 201
    assert pedido.json()["status"] == "simulado"
    assert pedido.json()["total_centavos"] == carrinho.json()["total_centavos"]


@pytest.mark.parametrize("endpoint", ["/carrinho", "/pedidos"])
def test_estoque_insuficiente(client, endpoint):
    resposta = client.post(endpoint, json={"itens": [{"produto_id": 1, "quantidade": 31}]})
    assert resposta.status_code == 400


@pytest.mark.parametrize("endpoint", ["/carrinho", "/pedidos"])
def test_carrinho_produto_ausente(client, endpoint):
    resposta = client.post(endpoint, json={"itens": [{"produto_id": 999, "quantidade": 1}]})
    assert resposta.status_code == 404


@pytest.mark.parametrize(
    "corpo",
    [
        {"itens": []},
        {"itens": [{"produto_id": 1, "quantidade": 0}]},
        {"itens": [{"produto_id": 1, "quantidade": -1}]},
        {"itens": [{"produto_id": 1, "quantidade": 101}]},
        {"itens": [{"produto_id": 1, "quantidade": 1.5}]},
        {"itens": [{"produto_id": 1, "quantidade": "2"}]},
        {"itens": [{"produto_id": True, "quantidade": 1}]},
        {"itens": [{"produto_id": 0, "quantidade": 1}]},
        {"itens": [{"produto_id": 1}]},
        {"itens": [{"produto_id": 1, "quantidade": 1}] * 21},
        {"itens": [{"produto_id": 1, "quantidade": 1, "extra": "nao-aceito"}]},
        {"itens": [{"produto_id": 1, "quantidade": 1}], "cliente": "dado-ficticio"},
        {},
    ],
)
def test_entradas_invalidas(client, corpo):
    resposta = client.post("/carrinho", json=corpo)
    assert resposta.status_code == 422
    assert resposta.json() == {"detail": "Entrada inválida. Consulte /docs."}
    assert "dado-ficticio" not in resposta.text


def test_json_invalido(client):
    resposta = client.post(
        "/carrinho", content="{invalido", headers={"Content-Type": "application/json"}
    )
    assert resposta.status_code == 422


@pytest.mark.parametrize("caminho", ["/", "/static/app.js", "/static/style.css", "/docs"])
def test_pagina_e_arquivos(client, caminho):
    resposta = client.get(caminho)
    assert resposta.status_code == 200
    assert resposta.headers["x-content-type-options"] == "nosniff"


def test_pagina_sem_dependencias_externas(client):
    resposta = client.get("/")
    assert "script-src 'self'" in resposta.headers["content-security-policy"]
    assert 'src="/static/app.js"' in resposta.text


def test_nao_expoe_arquivo_local(client):
    assert client.get("/.env").status_code == 404
    assert client.get("/static/../api.py").status_code == 404
