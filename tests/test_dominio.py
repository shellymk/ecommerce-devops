from uuid import UUID

import pytest

from ecommerce_devops.dominio import (
    ProdutoNaoEncontrado,
    buscar_produto,
    criar_pedido,
    listar_produtos,
    montar_carrinho,
)

pytestmark = pytest.mark.unit


def test_catalogo_tem_produtos_ficticios():
    produtos = listar_produtos()
    assert len(produtos) == 3
    assert all(p["preco_centavos"] > 0 for p in produtos)


def test_catalogo_nao_expoe_objetos_mutaveis():
    produtos = listar_produtos()
    produtos[0]["nome"] = "alterado"
    assert buscar_produto(1).nome == "Caderno de ideias"


def test_busca_produto():
    assert buscar_produto(2).preco_centavos == 490


def test_produto_inexistente():
    with pytest.raises(ProdutoNaoEncontrado):
        buscar_produto(999)


def test_carrinho_calcula_centavos_exatos():
    carrinho = montar_carrinho([(1, 2), (2, 3)])
    assert carrinho["total_centavos"] == 4650
    assert carrinho["itens"][0]["subtotal_centavos"] == 3180


def test_agrupa_itens_duplicados():
    carrinho = montar_carrinho([(1, 2), (1, 3)])
    assert len(carrinho["itens"]) == 1
    assert carrinho["itens"][0]["quantidade"] == 5
    assert carrinho["total_centavos"] == 7950


@pytest.mark.parametrize("itens", [[], [(1, 1)] * 21])
def test_tamanho_carrinho_invalido(itens):
    with pytest.raises(ValueError, match="1 a 20"):
        montar_carrinho(itens)


@pytest.mark.parametrize("quantidade", [0, -1, 101, 1.5, "2", True, None])
def test_quantidade_invalida(quantidade):
    with pytest.raises(ValueError, match="quantidade"):
        montar_carrinho([(1, quantidade)])


@pytest.mark.parametrize("produto_id", [0, -1, 1.5, "1", True, None])
def test_identificador_invalido(produto_id):
    with pytest.raises(ValueError, match="Identificador"):
        montar_carrinho([(produto_id, 1)])


@pytest.mark.parametrize("itens", [[(1, 31)], [(1, 20), (1, 20)]])
def test_estoque_e_soma_de_duplicados(itens):
    with pytest.raises(ValueError, match="estoque"):
        montar_carrinho(itens)


def test_carrinho_com_produto_inexistente():
    with pytest.raises(ProdutoNaoEncontrado):
        montar_carrinho([(999, 1)])


def test_limite_estoque_aceito():
    assert montar_carrinho([(2, 100)])["total_centavos"] == 49000


def test_pedido_simulado_com_identificador_unico():
    pedido = criar_pedido([(3, 1)])
    assert pedido["status"] == "simulado"
    assert UUID(pedido["pedido_id"]).version == 4
    assert pedido["pedido_id"] != criar_pedido([(3, 1)])["pedido_id"]
    assert pedido["total_centavos"] == 2990
    assert set(pedido) == {"pedido_id", "status", "itens", "total_centavos"}


def test_simulacao_nao_altera_estoque():
    criar_pedido([(3, 2)])
    assert buscar_produto(3).estoque == 20
