"use strict";
const CART_KEY = "loja-estudos:carrinho:v1";
const ORDER_KEY = "loja-estudos:pedido:v1";
const caminhos = {"/": "inicio", "/catalogo": "catalogo", "/carrinho": "carrinho", "/pedido-confirmado": "pedido"};
const pagina = caminhos[window.location.pathname] || "inicio";
const moeda = valor => new Intl.NumberFormat("pt-BR", {style: "currency", currency: "BRL"}).format(valor / 100);
let selecionados = new Map();
let ocupado = false;

function mensagem(texto) {
  document.querySelectorAll("[data-mensagem]").forEach(elemento => { elemento.textContent = texto; });
}
function atualizarBotoes() {
  document.querySelectorAll("[data-finalizar]").forEach(botao => {
    botao.disabled = ocupado || selecionados.size === 0;
    botao.textContent = ocupado ? "Aguarde…" : "Simular pedido";
    botao.setAttribute("aria-busy", String(ocupado));
  });
  document.querySelectorAll("[data-alterar], [data-adicionar], [data-limpar]").forEach(botao => { botao.disabled = ocupado; });
  const quantidade = Array.from(selecionados.values()).reduce((a, b) => a + b, 0);
  document.querySelectorAll("[data-contador]").forEach(elemento => { elemento.textContent = quantidade; });
}
function lerCarrinho() {
  try {
    const dados = JSON.parse(sessionStorage.getItem(CART_KEY) || "[]");
    if (!Array.isArray(dados) || dados.length > 20 || !dados.every(item =>
      Array.isArray(item) && item.length === 2 && Number.isInteger(item[0]) && item[0] > 0 && item[0] <= 9999 &&
      Number.isInteger(item[1]) && item[1] > 0 && item[1] <= 100)) throw new Error("Carrinho inválido.");
    selecionados = new Map(dados);
  } catch {
    selecionados = new Map();
    mensagem("Não foi possível recuperar o carrinho desta aba. Adicione os produtos novamente.");
  }
}
function salvarCarrinho() {
  try { sessionStorage.setItem(CART_KEY, JSON.stringify(Array.from(selecionados))); }
  catch { throw new Error("Permita o armazenamento desta aba para guardar seu carrinho."); }
}
function corpo() { return {itens: Array.from(selecionados, ([produto_id, quantidade]) => ({produto_id, quantidade}))}; }
async function enviar(caminho) {
  const resposta = await fetch(caminho, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(corpo())});
  const dados = await resposta.json();
  if (!resposta.ok) throw new Error(typeof dados.detail === "string" ? dados.detail : "Confira os itens do carrinho.");
  return dados;
}
function linhaProduto(item, editavel) {
  const linha = document.createElement("div"); linha.className = editavel ? "item-carrinho" : "linha";
  const descricao = document.createElement("div");
  const nome = document.createElement("strong"); nome.textContent = item.nome;
  const detalhe = document.createElement("p"); detalhe.textContent = `${item.quantidade} × ${moeda(item.preco_unitario_centavos)}`;
  descricao.append(nome, detalhe); linha.append(descricao);
  if (editavel) {
    const controles = document.createElement("div"); controles.className = "quantidade";
    for (const [texto, nova, rotulo] of [["−", item.quantidade - 1, "Diminuir"], ["+", item.quantidade + 1, "Aumentar"]]) {
      const botao = document.createElement("button"); botao.textContent = texto; botao.dataset.alterar = "true";
      botao.setAttribute("aria-label", `${rotulo} quantidade de ${item.nome}`);
      botao.addEventListener("click", () => alterar(item.produto_id, nova)); controles.append(botao);
    }
    const remover = document.createElement("button"); remover.className = "remover"; remover.textContent = "Remover";
    remover.dataset.alterar = "true"; remover.setAttribute("aria-label", `Remover ${item.nome}`);
    remover.addEventListener("click", () => alterar(item.produto_id, 0)); controles.append(remover); linha.append(controles);
  }
  const subtotal = document.createElement("strong"); subtotal.textContent = moeda(item.subtotal_centavos); linha.append(subtotal);
  return linha;
}
function renderizarCarrinho(carrinho) {
  document.querySelectorAll("[data-itens]").forEach(container => {
    container.replaceChildren();
    if (!carrinho.itens.length) {
      const vazio = document.createElement("p"); vazio.className = "vazio"; vazio.textContent = "Seu carrinho está vazio. Escolha um produto no catálogo."; container.append(vazio);
    } else carrinho.itens.forEach(item => container.append(linhaProduto(item, container.dataset.editavel === "true")));
  });
  document.querySelectorAll("[data-total]").forEach(elemento => { elemento.textContent = moeda(carrinho.total_centavos); });
  atualizarBotoes();
}
async function atualizarCarrinho() { renderizarCarrinho(selecionados.size ? await enviar("/carrinho") : {itens: [], total_centavos: 0}); }
async function alterar(id, quantidade) {
  if (ocupado) return;
  ocupado = true; atualizarBotoes();
  const anterior = new Map(selecionados);
  if (quantidade === 0) selecionados.delete(id); else selecionados.set(id, quantidade);
  try {
    const carrinho = selecionados.size ? await enviar("/carrinho") : {itens: [], total_centavos: 0};
    salvarCarrinho(); renderizarCarrinho(carrinho); mensagem(quantidade ? "Carrinho atualizado." : "Produto removido.");
  } catch (erro) { selecionados = anterior; mensagem(erro.message); }
  finally { ocupado = false; atualizarBotoes(); }
}
async function carregarProdutos() {
  const resposta = await fetch("/produtos");
  if (!resposta.ok) throw new Error("Não foi possível carregar o catálogo.");
  const produtos = await resposta.json();
  const icones = {1: "📓", 2: "🖊️", 3: "☕"};
  document.querySelectorAll(`[data-view="${pagina}"] [data-produtos]`).forEach(container => {
    container.replaceChildren();
    produtos.forEach(produto => {
      const card = document.createElement("article"); card.className = "produto";
      const icone = document.createElement("div"); icone.className = `icone produto-${produto.id}`; icone.textContent = icones[produto.id] || "📦"; icone.setAttribute("aria-hidden", "true");
      const titulo = document.createElement("h3"); titulo.textContent = produto.nome;
      const preco = document.createElement("div"); preco.className = "preco"; preco.textContent = moeda(produto.preco_centavos);
      const estoque = document.createElement("p"); estoque.className = "estoque"; estoque.textContent = `${produto.estoque} unidades demonstrativas`;
      const botao = document.createElement("button"); botao.textContent = "Adicionar ao carrinho"; botao.dataset.adicionar = "true";
      botao.setAttribute("aria-label", `Adicionar ${produto.nome}`);
      botao.addEventListener("click", () => alterar(produto.id, (selecionados.get(produto.id) || 0) + 1));
      card.append(icone, titulo, preco, estoque, botao); container.append(card);
    });
  });
}
function mostrarPedido() {
  try {
    const pedido = JSON.parse(sessionStorage.getItem(ORDER_KEY) || "null");
    if (!pedido || pedido.status !== "simulado" || !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(pedido.pedido_id) ||
      !Number.isSafeInteger(pedido.total_centavos) || pedido.total_centavos < 0 || !Array.isArray(pedido.itens) ||
      !pedido.itens.length || pedido.itens.length > 20 || !pedido.itens.every(item => typeof item.nome === "string" && item.nome.length <= 80 &&
        Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 100 &&
        Number.isSafeInteger(item.preco_unitario_centavos) && item.preco_unitario_centavos > 0 &&
        item.subtotal_centavos === item.preco_unitario_centavos * item.quantidade) ||
      pedido.total_centavos !== pedido.itens.reduce((total, item) => total + item.subtotal_centavos, 0)) throw new Error("Pedido ausente.");
    document.getElementById("pedido-numero").textContent = pedido.pedido_id;
    document.getElementById("pedido-total").textContent = moeda(pedido.total_centavos);
    document.getElementById("pedido-itens").replaceChildren(...pedido.itens.map(item => linhaProduto(item, false)));
    document.getElementById("pedido-confirmado").hidden = false;
  } catch { document.getElementById("pedido-ausente").hidden = false; }
}
async function finalizarPedido() {
  if (ocupado || selecionados.size === 0) return;
  ocupado = true; atualizarBotoes(); mensagem("Criando seu pedido simulado…");
  try {
    const pedido = await enviar("/pedidos");
    try { sessionStorage.setItem(ORDER_KEY, JSON.stringify(pedido)); }
    catch { throw new Error("Permita o armazenamento desta aba para abrir a confirmação do pedido."); }
    const anterior = selecionados; selecionados = new Map();
    try { salvarCarrinho(); } catch (erro) { selecionados = anterior; throw erro; }
    window.location.assign("/pedido-confirmado");
  } catch (erro) { mensagem(erro.message); }
  finally { ocupado = false; atualizarBotoes(); }
}
document.querySelector(`[data-view="${pagina}"]`).hidden = false;
document.querySelectorAll(`[data-nav="${pagina}"]`).forEach(link => link.setAttribute("aria-current", "page"));
document.title = {inicio: "Loja de estudos — início", catalogo: "Catálogo — Loja de estudos", carrinho: "Carrinho — Loja de estudos", pedido: "Seu pedido — Loja de estudos"}[pagina];
document.querySelectorAll("[data-finalizar]").forEach(botao => botao.addEventListener("click", finalizarPedido));
document.querySelectorAll("[data-limpar]").forEach(botao => botao.addEventListener("click", () => {
  if (ocupado) return;
  const anterior = selecionados; selecionados = new Map();
  try { salvarCarrinho(); renderizarCarrinho({itens: [], total_centavos: 0}); mensagem("Carrinho limpo."); }
  catch (erro) { selecionados = anterior; atualizarBotoes(); mensagem(erro.message); }
}));
async function iniciar() {
  lerCarrinho(); atualizarBotoes();
  if (pagina === "pedido") { mostrarPedido(); return; }
  try { if (pagina === "inicio" || pagina === "catalogo") await carregarProdutos(); await atualizarCarrinho(); }
  catch (erro) { mensagem(erro.message); }
}
window.addEventListener("pageshow", evento => { if (evento.persisted) iniciar(); });
iniciar();
