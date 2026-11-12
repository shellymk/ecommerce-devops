# Passo a passo das Práticas 1 e 2

## 1 Conferir a proposta

Ler `REQUISITOS.md` e `PROJETO.md`. O tema é e-commerce, com dados fictícios e pedidos
simulados. Confirmar com o tutor as funções esperadas e a distribuição de papéis.

## 2 Preparar o ambiente

Na pasta do projeto, conferir `git --version` e `python --version`.
Se Python não executar, instalar Python 3.12 a partir de <https://www.python.org/downloads/>
ou selecionar uma instalação existente. O projeto foi verificado com 3.12.14.
Não baixar instaladores de anúncios ou sites de terceiros.

Seguir os comandos de instalação e execução do README. O ambiente `.venv` é local e
ignorado pelo Git. Não requer senhas, GitHub ou configurações de nuvem.

## 3 Experimentar a loja

Abrir a página local. Adicionar um caderno e duas canetas, conferir o total de R$ 25,70,
simular o pedido e confirmar a mensagem de que não houve cobrança. Limpar o carrinho.
Em `/docs`, consultar o catálogo e testar quantidade zero para receber erro de validação.

## 4 Conferir testes e build

Executar os comandos do README para lint, formatação, pytest com cobertura e build.
Abrir `reports/html/index.html` para o relatório. Conferir o wheel com
`tools/validar_artefato.py`. Guardar capturas locais sem dados pessoais.

## 5 Entender o histórico local

Se recebeu a pasta com o repositório já inicializado, usar `git status`, `git branch`
e `git log --oneline --all --graph` para conferir main e feat/loja.
Não repetir a inicialização e não apagar o histórico existente.

Se extraiu apenas o ZIP de fontes, ele não contém `.git`. Criar o histórico do zero:

```powershell
git init -b main
git config --local user.name shellymk
git config --local user.email 86502172+shellymk@users.noreply.github.com
git add .gitignore .gitattributes .python-version README.md
python tools/verificar_segredos.py
git diff --cached
git commit -m "chore(repo): inicia estrutura e documentacao"
git switch -c feat/loja
git add pyproject.toml requirements-dev.txt src tests tools docs .github
python tools/verificar_segredos.py
git diff --cached --stat
git diff --cached
git commit -m "feat(loja): adiciona ecommerce com testes e CI"
```

## 6 Criar repositório e PR no GitHub

Conferir visibilidade e a forma de acesso do professor, criar repositório vazio e
seguir `GIT.md`. A publicação, o PR e o merge devem existir de verdade; arquivos
locais não substituem essas evidências. Fazer login apenas na interface oficial.

## 7 Conferir a esteira

No GitHub, abrir Actions e o run correspondente ao PR. Conferir Build e lint,
Testes e cobertura, Artefato versionado. Baixar o wheel e os relatórios e registrar
links e capturas. Se algo falhar, corrigir na mesma branch e acompanhar o novo run.

## 8 Montar a entrega

Preencher `RELATORIO.md` com as evidências reais e reunir tudo em um único documento
para o AVA, conforme o enunciado. Não publicar identificação acadêmica no repositório.
O prazo é contado da aula prática, cuja data ainda não foi fornecida.
