"""Regras puras de catálogo, carrinho e pedido simulado.

Valores monetários usam centavos inteiros, sem arredondamento de ponto flutuante.
O catálogo é fictício e não há persistência nem reserva real de estoque.
"""

from dataclasses import asdict, dataclass
from uuid import uuid4


class ProdutoNaoEncontrado(ValueError):
    pass


@dataclass(frozen=True)
class Produto:
    id: int
    nome: str
    preco_centavos: int
    estoque: int


CATALOGO = (
    Produto(1, "Caderno de ideias", 1590, 30),
    Produto(2, "Caneta azul", 490, 100),
    Produto(3, "Caneca de estudos", 2990, 20),
)


def listar_produtos() -> list[dict]:
    return [asdict(produto) for produto in CATALOGO]


def buscar_produto(produto_id: int) -> Produto:
    for produto in CATALOGO:
        if produto.id == produto_id:
            return produto
    raise ProdutoNaoEncontrado("Produto não encontrado.")


def montar_carrinho(itens: list[tuple[int, int]]) -> dict:
    if not 1 <= len(itens) <= 20:
        raise ValueError("O carrinho deve conter de 1 a 20 itens.")
    quantidades: dict[int, int] = {}
    for produto_id, quantidade in itens:
        if type(produto_id) is not int or produto_id < 1:
            raise ValueError("Identificador de produto inválido.")
        if type(quantidade) is not int or not 1 <= quantidade <= 100:
            raise ValueError("A quantidade deve ser um inteiro entre 1 e 100.")
        quantidades[produto_id] = quantidades.get(produto_id, 0) + quantidade
    linhas = []
    for produto_id, quantidade in quantidades.items():
        produto = buscar_produto(produto_id)
        if quantidade > produto.estoque:
            raise ValueError("Quantidade superior ao estoque demonstrativo.")
        linhas.append(
            {
                "produto_id": produto.id,
                "nome": produto.nome,
                "quantidade": quantidade,
                "preco_unitario_centavos": produto.preco_centavos,
                "subtotal_centavos": produto.preco_centavos * quantidade,
            }
        )
    return {"itens": linhas, "total_centavos": sum(item["subtotal_centavos"] for item in linhas)}


def criar_pedido(itens: list[tuple[int, int]]) -> dict:
    carrinho = montar_carrinho(itens)
    return {
        "pedido_id": str(uuid4()),
        "status": "simulado",
        **carrinho,
    }
