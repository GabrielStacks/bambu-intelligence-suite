"""
=============================================================================
ROBÔ ESPIÃO DE MERCADO - MERCADO LIVRE
Bambu Lab A1 - Análise Competitiva de Concorrentes
=============================================================================
Objetivo:
Pesquisar em tempo real produtos concorrentes no Mercado Livre, coletar títulos,
preços, fretes e links dos anúncios mais vendidos, calcular métricas de mercado
e gerar planilhas prontas no Excel para validar peças impressas na Bambu A1.
=============================================================================
"""

import sys
import os
import re
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

# Garante suporte a UTF-8 e emojis no terminal do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def extrair_preco(texto: str) -> float:
    """Limpa e converte strings de preço (ex: 'R$ 99,90' ou '99') em float."""
    if not texto:
        return 0.0
    limpo = re.sub(r"[^\d,\.]", "", texto).strip()
    if not limpo:
        return 0.0
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return 0.0


def minerar_mercado_livre(termo_busca: str, max_produtos: int = 25) -> list[dict]:
    """
    Abre o Chrome no Mercado Livre, digita a busca e extrai os anúncios concorrentes.
    Roda liso, sem captcha e sem necessidade de login.
    """
    print("\n" + "🔍 " + "=" * 58)
    print(f"   PESQUISANDO NO MERCADO LIVRE: '{termo_busca.upper()}'")
    print("=" * 62)

    produtos = []

    with sync_playwright() as p:
        print("🤖 [1/3] Inicializando o navegador Chrome...")
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(locale="pt-BR")
        page = context.new_page()

        print("🌐 [2/3] Acessando o Mercado Livre e buscando anúncios...")
        page.goto("https://www.mercadolivre.com.br", timeout=60000)

        search_input = page.locator("input.nav-search-input")
        search_input.fill(termo_busca)
        search_input.press("Enter")

        # Aguarda 3.5 segundos para os resultados carregarem
        page.wait_for_timeout(3500)

        print("📦 [3/3] Minerando títulos, preços e links...")
        cards = page.locator(".ui-search-layout__item, .poly-card").all()

        vistos = set()
        for card in cards:
            if len(produtos) >= max_produtos:
                break

            el_titulo = card.locator("h2, .poly-component__title, a.ui-search-link").first
            titulo = el_titulo.inner_text().strip() if el_titulo.count() else ""
            if not titulo or titulo in vistos:
                continue
            vistos.add(titulo)

            el_preco = card.locator(".andes-money-amount__fraction").first
            preco = extrair_preco(el_preco.inner_text()) if el_preco.count() else 0.0

            el_link = card.locator("a.ui-search-link, .poly-component__title a, a[href*='MLB']").first
            link = el_link.get_attribute("href") if el_link.count() else ""
            if link and "#" in link:
                link = link.split("#")[0]
            if link and "?" in link:
                link = link.split("?")[0]

            is_full = card.locator("svg[aria-label*='Full'], span:has-text('FULL')").count() > 0
            frete_gratis = card.locator("span:has-text('Frete grátis')").count() > 0
            destaque = "FULL ⚡" if is_full else ("Frete Grátis" if frete_gratis else "Padrão")

            produtos.append({
                "Plataforma": "Mercado Livre",
                "Título": titulo,
                "Preço (R$)": preco,
                "Destaque": destaque,
                "Link": link
            })

        browser.close()

    return produtos


def gerar_relatorio_e_salvar(termo: str, produtos: list[dict]):
    if not produtos:
        print("\n⚠️ Nenhum produto encontrado para este termo.")
        return

    df = pd.DataFrame(produtos)

    # Cria pasta 'pesquisas'
    pasta_saida = "pesquisas"
    os.makedirs(pasta_saida, exist_ok=True)

    termo_limpo = re.sub(r"[^\w\s-]", "", termo).strip().replace(" ", "_").lower()
    data_str = datetime.now().strftime("%Y%m%d_%H%M")
    caminho_csv = os.path.join(pasta_saida, f"pesquisa_{termo_limpo}_{data_str}.csv")

    # Salva CSV com codificação UTF-8 com BOM para abrir direto no Excel no Brasil
    df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

    precos_validos = df[df["Preço (R$)"] > 0]["Preço (R$)"]
    preco_min = precos_validos.min() if not precos_validos.empty else 0.0
    preco_medio = precos_validos.mean() if not precos_validos.empty else 0.0
    preco_max = precos_validos.max() if not precos_validos.empty else 0.0

    print("\n" + "📊 " + "=" * 58)
    print(f"   RELATÓRIO DE MERCADO: {termo.upper()}")
    print("=" * 62)
    print(f"   • Total de anúncios analisados: {len(df)}")
    print(f"   • Menor Preço Encontrado:       R$ {preco_min:.2f}")
    print(f"   • Preço Médio Praticado:        R$ {preco_medio:.2f}")
    print(f"   • Maior Preço Encontrado:       R$ {preco_max:.2f}")
    print("=" * 62)

    print("\n🏆 TOP 5 ANÚNCIOS MAIS RELEVANTES:")
    for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
        print(f"   {i}. R$ {row['Preço (R$)']:>6.2f} | {row['Título'][:50]}... ({row['Destaque']})")

    print("\n📁 PLANILHA GERADA COM SUCESSO:")
    print(f"   👉 {os.path.abspath(caminho_csv)}")
    print("   (Você pode abrir esse arquivo direto no Excel com 2 cliques!)")
    print("=" * 62)


def menu():
    print("\n" + "🚀 " + "=" * 58)
    print("   ROBÔ ESPIÃO DE MERCADO - MERCADO LIVRE")
    print("=" * 62)
    print("1 - Pesquisar produto e gerar planilha")
    print("2 - Sair")

    while True:
        op = input("\n👉 Escolha uma opção (1 ou 2): ").strip()
        if op == "1":
            termo = input("\nDigite o que deseja pesquisar (ex: suporte headset gamer 3d): ").strip()
            if not termo:
                termo = "suporte headset gamer 3d"
            prods = minerar_mercado_livre(termo, max_produtos=25)
            gerar_relatorio_e_salvar(termo, prods)
        elif op == "2":
            print("\n👋 Robô finalizado. Bons lucros!")
            break
        else:
            print("⚠️ Opção inválida. Digite 1 ou 2.")


if __name__ == "__main__":
    menu()
