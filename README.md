# Loja de Estudos DevOps

E-commerce didático em Python para as Práticas 1 e 2 da disciplina de DevOps.
Permite consultar três produtos fictícios, montar um carrinho e simular um pedido.
Não recebe dados de clientes nem processa pagamentos. Os pedidos não são persistidos
e o estoque é demonstrativo, sem reserva ou baixa real.

## Comece por aqui

1. Abra o [guia passo a passo](docs/GUIA.md).
2. Consulte a [definição e o backlog](docs/PROJETO.md).
3. Revise a [estratégia Git](docs/GIT.md) e a [pipeline](docs/PIPELINE.md).
4. Antes de publicar, confira [os cuidados com informações sensíveis](docs/SEGURANCA.md).
5. Registre apenas evidências reais no [roteiro do relatório](docs/RELATORIO.md).

## Execução no Windows PowerShell

Use Python 3.12.14 e Git. As dependências estão fixadas em `requirements-dev.txt`,
com hashes de wheels para Windows x64 e Linux x64. A aplicação usa FastAPI e Uvicorn;
pytest, pytest-cov, Ruff e build são ferramentas de desenvolvimento.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes --only-binary=:all: -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
.\.venv\Scripts\python.exe -m uvicorn ecommerce_devops.api:create_app --factory --host 127.0.0.1 --port 8000
```

Abra <http://127.0.0.1:8000>. A documentação da API fica em <http://127.0.0.1:8000/docs>.
Encerre o servidor com Ctrl+C. Não é necessário ativar o ambiente virtual nem mudar
a política de execução do PowerShell.

## Verificação local

Em outro terminal, na pasta do projeto:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest -q --cov --cov-report=term-missing --cov-report=html:reports/html --cov-report=xml:reports/coverage.xml --junitxml=reports/junit.xml
.\.venv\Scripts\python.exe -m build --wheel --no-isolation
.\.venv\Scripts\python.exe tools/validar_artefato.py
```

O limite mínimo de cobertura combinada de linhas e ramificações é 90%, escolha do projeto;
o professor pede validação da cobertura, mas não define um percentual no roteiro recebido.
O pacote gerado é `dist/ecommerce_devops_academico-0.1.0-py3-none-any.whl`.

## API

| Método | Endereço | Função |
|---|---|---|
| GET | `/health` | Estado e versão |
| GET | `/produtos` | Catálogo fictício |
| GET | `/produtos/1` | Detalhes de um produto |
| POST | `/carrinho` | Validação e cálculo do total |
| POST | `/pedidos` | Pedido simulado |

Exemplo de corpo para os dois POST:

```json
{"itens": [{"produto_id": 1, "quantidade": 2}]}
```

Valores monetários são inteiros em centavos; por exemplo, 1590 representa R$ 15,90.
Produtos duplicados são somados antes da validação do estoque. Entradas inválidas
retornam 422, produto ausente retorna 404 e estoque insuficiente retorna 400.

## Estrutura

```text
src/ecommerce_devops/  domínio, API e página da loja
tests/                testes unitários e de integração HTTP
tools/                verificação básica de segredos e validação do wheel
docs/                 roteiro, backlog, Git, pipeline, segurança e relatório
.github/workflows/    integração contínua
```

Estratégia: Trunk-based Development com branches curtas, PR para `main` e Conventional
Commits. A CI executa Build → Testes → Artefato. As Práticas 3 a 6 ainda não estão
implementadas; o projeto pode evoluir para Docker, infraestrutura, observabilidade e DevSecOps.

## Referências

- [Roteiro do professor](docs/REQUISITOS.md), síntese das exigências recebidas.
- [FastAPI](https://fastapi.tiangolo.com/tutorial/).
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/reporting.html).
- [Ruff](https://docs.astral.sh/ruff/).
- [GitHub Actions e Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
- [Segurança no GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use).
