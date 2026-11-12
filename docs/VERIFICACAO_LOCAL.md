# Verificação local da versão 0.1.0

Verificações executadas em 12 de novembro de 2026, no Windows x64, com Python 3.12.14.

| Verificação | Resultado observado |
|---|---|
| Ruff | Código e formatação aprovados. |
| pytest | 63 testes aprovados. |
| Cobertura Python | 100% nas 98 instruções e 18 ramificações de API e domínio; mínimo configurado de 90%. |
| Build | Wheel da versão 0.1.0 gerado. |
| Instalação do wheel | Origem do módulo confirmada no diretório de instalação temporário, sem usar os fontes locais. |
| Conteúdo do wheel | Apenas fontes da aplicação, arquivos estáticos previstos e metadados. |
| Navegador | Catálogo, carrinho, total, pedido simulado e limpeza aprovados. |
| Telas | Conferência em 1280 × 900 e 390 × 844, sem rolagem horizontal no celular. |

A cobertura mede somente Python; os testes de navegador verificaram a interface e
não mediram cobertura JavaScript. Os testes de integração usam HTTP em processo com
TestClient; a verificação adicional de navegador usou servidor Uvicorn real.

O ambiente de teste emitiu aviso de descontinuação do uso de httpx pelo TestClient
da versão atual de Starlette, sem falhas de teste. Uma futura atualização deve rever
essa dependência e executar novamente as verificações.

Esses resultados locais não substituem evidências de execução no GitHub. Registrar
links, commit e resultado hospedado no relatório somente após o run concluir.
