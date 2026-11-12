# Fluxo Git adotado

Adotamos Trunk-based Development com branches de curta duração e integração por Pull
Request na main. Isso reduz divergências e mantém mudanças pequenas para uma equipe
acadêmica. Não usamos uma develop permanente nem o fluxo de releases do Gitflow.

## Convenções

Branches: `feat/loja`, `fix/estoque`, `docs/relatorio`, `test/carrinho`, `ci/pipeline`.
Commits: `feat(carrinho): calcula total em centavos`, `test(api): valida pedido simulado`,
`ci(pipeline): automatiza build testes e artefato`, `docs(projeto): documenta a pratica`.

O ciclo é: atualizar main → criar branch curta → implementar e testar → revisar o diff
→ push da branch → PR para main → CI → revisão → merge → atualização da main local.
Em equipe, pedir revisão por pares. Em trabalho individual, registrar a revisão própria
com honestidade, sem atribuir aprovação a outra pessoa.

## Privacidade do autor

A identidade local usa o identificador público shellymk e o endereço noreply associado
ao ID público confirmado no GitHub. Não altera a configuração global do computador:

```powershell
git config --local user.name shellymk
git config --local user.email 86502172+shellymk@users.noreply.github.com
```

Na conta GitHub, conferir Settings → Emails para manter o e-mail particular privado e,
se disponível, bloquear pushes que exponham esse endereço. O noreply não é senha,
token nem chave de acesso. Conferir autores antes de enviar o histórico.

## Publicação futura

O nome proposto é `ecommerce-devops`, no perfil shellymk. Não há remoto configurado
antes da escolha da visibilidade e criação do repositório. Preferir privado durante a
revisão inicial e verificar como o professor receberá acesso, caso permaneça privado.
Um repositório público expõe código, documentação e histórico.

Criar o repositório vazio no GitHub, sem README adicional, licença ou .gitignore.
Após confirmar seu endereço real, associar o origin e enviar main e feat/loja.
Abrir PR de feat/loja para main. Não integrar antes de conferir a CI e as evidências.
Não colar token em URL nem no terminal: usar a autenticação do GitHub no navegador.
