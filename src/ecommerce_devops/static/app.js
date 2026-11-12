"use strict";
const selecionados = new Map();
const moeda = valor => new Intl.NumberFormat("pt-BR", {style: "currency", currency: "BRL"}).format(valor / 100);
const mensagem = document.getElementById("mensagem");
const finalizar = document.getElementById("finalizar");
let ocupado = false;

function corpo() {
  return {itens: Array.from(selecionados, ([produto_id, quantidade]) => ({produto_id, quantidade}))};
}
async function enviar(caminho) {
  const resposta = await fetch(caminho, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(corpo())});
  const dados = await resposta.json();
  if (!resposta.ok) throw new Error(typeof dados.detail === "string" ? dados.detail : "Confira os itens do carrinho.");
  return dados;
}
function limpar() {
  selecionados.clear();
  document.getElementById("carrinho").textContent = "Escolha um produto para começar.";
  document.getElementById("total").textContent = moeda(0);
  finalizar.disabled = true;
}
async function adicionar(id) {
  if (ocupado) return;
  ocupado = true;
  const anterior = selecionados.get(id) || 0;
  selecionados.set(id, anterior + 1);
  try {
    const carrinho = await enviar("/carrinho");
    const container = document.getElementById("carrinho");
    container.replaceChildren();
    for (const item of carrinho.itens) {
      const linha = document.createElement("p");
      linha.className = "linha";
      linha.textContent = `${item.quantidade} × ${item.nome} — ${moeda(item.subtotal_centavos)}`;
      container.append(linha);
    }
    document.getElementById("total").textContent = moeda(carrinho.total_centavos);
    mensagem.textContent = "";
  } catch (erro) {
    if (anterior) selecionados.set(id, anterior); else selecionados.delete(id);
    mensagem.textContent = erro.message;
  } finally {
    ocupado = false;
    finalizar.disabled = selecionados.size === 0;
  }
}
async function carregar() {
  try {
    const resposta = await fetch("/produtos");
    if (!resposta.ok) throw new Error("Não foi possível carregar o catálogo.");
    const produtos = await resposta.json();
    const icones = ["📓", "🖊️", "☕"];
    produtos.forEach((produto, indice) => {
      const card = document.createElement("article"); card.className = "produto";
      const icone = document.createElement("div"); icone.className = "icone"; icone.textContent = icones[indice]; icone.setAttribute("aria-hidden", "true");
      const titulo = document.createElement("h3"); titulo.textContent = produto.nome;
      const preco = document.createElement("div"); preco.className = "preco"; preco.textContent = moeda(produto.preco_centavos);
      const estoque = document.createElement("p"); estoque.className = "estoque"; estoque.textContent = `${produto.estoque} unidades demonstrativas`;
      const botao = document.createElement("button"); botao.textContent = "Adicionar"; botao.setAttribute("aria-label", `Adicionar ${produto.nome}`); botao.addEventListener("click", () => adicionar(produto.id));
      card.append(icone, titulo, preco, estoque, botao); document.getElementById("produtos").append(card);
    });
  } catch (erro) { mensagem.textContent = erro.message; }
}
document.getElementById("limpar").addEventListener("click", () => {
  if (ocupado) return;
  limpar(); mensagem.textContent = "";
});
finalizar.addEventListener("click", async () => {
  if (ocupado || selecionados.size === 0) return;
  ocupado = true; finalizar.disabled = true;
  try {
    const pedido = await enviar("/pedidos");
    limpar(); mensagem.textContent = `Pedido simulado criado: ${pedido.pedido_id}. Nenhuma cobrança foi realizada.`;
  } catch (erro) { mensagem.textContent = erro.message; }
  finally { ocupado = false; finalizar.disabled = selecionados.size === 0; }
});
carregar();
