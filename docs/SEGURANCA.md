# Proteção das informações

A loja não precisa de senhas, tokens ou dados pessoais. Não inserir tais dados no código,
nos testes, em capturas ou nos exemplos. Usar somente o catálogo fictício incluído.

## Antes de um commit ou push

1. Conferir a lista de arquivos e o diff; usar inclusão explícita de arquivos.
2. Executar a verificação básica do índice Git:

```powershell
python tools/verificar_segredos.py
git diff --cached --stat
git diff --cached
```

3. Revisar também dados pessoais, conteúdo de imagens, documentos e o histórico antes do primeiro push.
4. Confirmar nome de autor e e-mail noreply nos commits.

O verificador confere o conteúdo preparado no índice, inclusive antes do primeiro commit.
Reconhece alguns formatos de token, chave privada, atribuição de credencial e arquivos
locais. Omite os valores em mensagens. Não é um detector completo nem examina o histórico.
Um resultado aprovado não garante ausência de todo segredo ou dado pessoal.

O `.gitignore` não remove arquivos já rastreados. Se um arquivo local foi preparado por
engano antes do primeiro commit, retirá-lo do índice e rever o conteúdo antes de continuar.
Se um segredo real foi publicado, revogá-lo no serviço de origem e tratar o histórico;
apenas apagar a linha do código não resolve a exposição. Não enviar o segredo na conversa.

## Ambiente e artefatos

Dependências têm versões e hashes fixos. A CI usa ações oficiais com SHA completo,
permissão de leitura do código e checkout sem persistir credenciais. Não há secrets
personalizados nem publicação em PyPI. O wheel aceita somente fontes da aplicação,
seus três arquivos estáticos e metadados previstos. Não empacota a pasta inteira.

O aplicativo deve ser usado em laboratório, inicialmente no endereço local 127.0.0.1.
Ele não possui autenticação, persistência, controle antifraude nem transações comerciais.
Não expor a loja como um e-commerce de produção. Os campos da API não aceitam dados de
clientes e a resposta de validação não repete o valor rejeitado.
O armazenamento da sessão do navegador contém somente IDs de produtos, quantidades
e o resumo fictício do último pedido. Não inserir informações pessoais nesse estado.
Ele não substitui uma base de pedidos, autenticação ou controle real de estoque.

Não habilitar logs de corpo de requisição, variáveis de ambiente ou cabeçalhos de
autenticação. Logs de acesso do servidor podem registrar o endereço solicitado;
nunca enviar credenciais pela URL. A documentação automática de API pode carregar
recursos externos na página `/docs`; a página da loja usa somente arquivos locais.

Guardar capturas para o relatório em `evidencias-locais/`, ignorada pelo Git. Revisar
abas, notificações, e-mails, terminal e metadados antes de compartilhar uma captura.
