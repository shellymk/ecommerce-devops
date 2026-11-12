# Integração contínua

O arquivo `.github/workflows/ci.yml` executa em push da main, PR para
main ou acionamento manual. Cada etapa usa o mesmo commit e Python 3.12.14.

## Ordem de execução

```text
Build e lint → Testes e cobertura → Artefato versionado
```

| Job | Steps principais | Condição para avançar |
|---|---|---|
| build | Checkout; Python; verificação básica de segredos; dependências com hashes; lint e formatação; build preliminar. | Todos os steps aprovados. |
| test | Dependências; instalação editável; testes unitários e de integração HTTP; relatórios XML, HTML e JUnit. | Testes aprovados e cobertura combinada de linhas/ramificações de pelo menos 90%. |
| artifact | Dependências; geração do wheel final; conferência do conteúdo; instalação em diretório temporário e teste HTTP; upload. | Teste de instalação aprovado e wheel presente. |

O primeiro build verifica o empacotamento sem disponibilizar pacote. Após os testes,
o último job gera e disponibiliza o artefato final versionado. Essa divisão preserva
a ordem Build → Test → Artifact e só distribui o pacote após a aprovação dos testes.

No GitHub Actions os estágios são representados por jobs ligados por `needs`; não há
uma chave `stages` nesse formato. Um job contém steps sequenciais. O padrão de `needs`
impede jobs seguintes de executar diante de falha, aplicando Fail Fast entre etapas.

O nome do wheel contém a versão 0.1.0. O upload também identifica o commit pelo SHA.
Pacote e relatórios aprovados são mantidos por sete dias no GitHub, conforme configuração.
Aumentar o prazo antes da entrega se o período de avaliação exigir disponibilidade maior.

## Proteção da branch principal

Uma CI reprovada interrompe a esteira, mas bloquear o merge depende de configurar uma
regra de proteção no GitHub exigindo PR e os checks da CI. Essa regra precisa ser
verificada no repositório real; a disponibilidade varia com o plano e a visibilidade.
Não declarar bloqueio de merge ou revisão obrigatória antes de configurar e conferir.

## Evidências ainda necessárias no GitHub

Registrar URL do run, commit, jobs aprovados, resumo dos testes, relatório de cobertura
e link do artefato. A configuração local do YAML não comprova execução hospedada.
Uma falha de teste pode ser demonstrada em branch de laboratório sem mesclar uma
versão reprovada na main; registrar também o run corrigido. Não simular falha usando
credenciais reais ou dados de clientes.
