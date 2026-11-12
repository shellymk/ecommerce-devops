"""API HTTP e página da loja; todas as compras são simulações."""

from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from .dominio import (
    ProdutoNaoEncontrado,
    buscar_produto,
    criar_pedido,
    listar_produtos,
    montar_carrinho,
)

STATIC = Path(__file__).parent / "static"


class ItemEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    produto_id: int = Field(ge=1, le=9999)
    quantidade: int = Field(ge=1, le=100)


class CarrinhoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    itens: list[ItemEntrada] = Field(min_length=1, max_length=20)


def create_app() -> FastAPI:
    app = FastAPI(title="Loja DevOps Acadêmica", version="0.2.0")
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.middleware("http")
    async def cabecalhos(request: Request, call_next):
        resposta = await call_next(request)
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["Referrer-Policy"] = "no-referrer"
        if request.url.path in {"/", "/catalogo", "/carrinho", "/pedido-confirmado"}:
            resposta.headers["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
            )
        return resposta

    @app.exception_handler(RequestValidationError)
    async def entrada_invalida(_request: Request, _erro: RequestValidationError):
        # Não devolve o valor recebido nem dados pessoais enviados por engano.
        return JSONResponse(
            status_code=422, content={"detail": "Entrada inválida. Consulte /docs."}
        )

    @app.get("/", include_in_schema=False)
    @app.get("/catalogo", include_in_schema=False)
    @app.get("/carrinho", include_in_schema=False)
    @app.get("/pedido-confirmado", include_in_schema=False)
    def pagina():
        return FileResponse(STATIC / "index.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "version": "0.2.0"}

    @app.get("/produtos")
    def produtos():
        return listar_produtos()

    @app.get("/produtos/{produto_id}")
    def produto(produto_id: int):
        try:
            return asdict(buscar_produto(produto_id))
        except ProdutoNaoEncontrado as erro:
            raise HTTPException(status_code=404, detail=str(erro)) from erro

    def executar(entrada: CarrinhoEntrada, finalizar: bool):
        itens = [(item.produto_id, item.quantidade) for item in entrada.itens]
        try:
            return criar_pedido(itens) if finalizar else montar_carrinho(itens)
        except ProdutoNaoEncontrado as erro:
            raise HTTPException(status_code=404, detail=str(erro)) from erro
        except ValueError as erro:
            raise HTTPException(status_code=400, detail=str(erro)) from erro

    @app.post("/carrinho")
    def carrinho(entrada: CarrinhoEntrada):
        return executar(entrada, finalizar=False)

    @app.post("/pedidos", status_code=201)
    def pedidos(entrada: CarrinhoEntrada):
        return executar(entrada, finalizar=True)

    return app
