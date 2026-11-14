# Navegação da versão 0.3.0

A primeira versão criava um pedido e mostrava uma mensagem na mesma tela. Agora,
Simular pedido abre uma página de confirmação com número, itens e total.

| Página | Comportamento |
|---|---|
| `/` | Início, apresentação da loja, produtos em destaque e resumo do carrinho. |
| `/catalogo` | Catálogo completo e inclusão de produtos. |
| `/carrinho` com GET | Página para aumentar, diminuir, remover e conferir o pedido. |
| `/pedido-confirmado` | Confirmação da última simulação nesta aba; sem pedido, mostra orientação para começar pelo catálogo. |

## Vitrine e apresentação

A página inicial tem um banner em carrossel com três slides: caderno, caneta e caneca.
Setas, indicadores e teclas direcionais nos controles permitem navegar, sem reprodução
automática. Cada slide apresenta imagem, preço por unidade e acesso ao catálogo.
Os preços são atualizados com os dados da API. Produtos em destaque aparecem abaixo,
com imagens ilustrativas locais e botões para adicionar ao carrinho.

A versão 0.3.0 substitui os ícones por imagens geradas para os produtos fictícios e
usa cores vinho, creme e tons neutros. A origem e os prompts estão em ASSETS.md.

POST `/carrinho` continua calculando as regras da API. POST `/pedidos` continua
criando apenas uma simulação. O navegador salva o retorno antes de navegar à confirmação.
Campos recebidos são exibidos como texto, sem interpretar HTML.

O carrinho é conservado na sessão da aba, inclusive ao mudar de página ou recarregar.
Depois da confirmação, o carrinho fica vazio. A última confirmação permanece disponível
nessa aba para recarregar a página; não há histórico de compras no servidor.

Verificação local em 13 de novembro de 2026: 76 testes Python aprovados, 100% de cobertura Python de API e domínio,
lint e sintaxe JavaScript aprovados. No navegador, foi verificada a inclusão de produtos,
troca entre Início e Catálogo, ajuste de quantidade no Carrinho, recarga com preservação
dos itens e confirmação de um caderno e duas canetas, no total de R$ 25,70.

Também foram conferidos os três slides, setas, indicadores e navegação por teclado.
No celular (390 × 844), início, catálogo e carrinho não apresentaram rolagem horizontal.
Os testes de navegador não mediram cobertura JavaScript. A suíte inclui 27 testes
de domínio, 15 do verificador básico e 34 de integração HTTP.
