"""
=============================================================================
BAMBU LAB A1 - INTELLIGENCE SUITE PRO
Plataforma SaaS de Precificação, Espionagem de Mercado e Copywriting com IA
=============================================================================
Design System: Modern Dark/Slate SaaS (Inspirado no ecossistema Bambu Lab & Helium10)
Cores: Deep Slate (#0F172A), Slate Cards (#1E293B), Bambu Emerald (#00AE42), Cyber Cyan (#06B6D4)
=============================================================================
"""

import os
import glob
import pandas as pd
import streamlit as st
from datetime import datetime

# Importa os módulos essenciais já consolidados
from precificador import calcular_custo_impressao, sugerir_preco_venda
from pesquisador_mercado import minerar_mercado_livre
from gerador_anuncios import criar_anuncio_com_ia
from atendimento_ia import responder_duvida_cliente


# ---------------------------------------------------------------------------
# CONFIGURAÇÃO GERAL DA PÁGINA
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Bambu Studio Intelligence Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# DESIGN SYSTEM & CSS PREMIUM (SaaS Level)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Principal */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    /* Top Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.98) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 50%, #00AE42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
    }
    .bambu-badge {
        background: rgba(0, 174, 66, 0.15);
        color: #00AE42;
        border: 1px solid rgba(0, 174, 66, 0.35);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
    }

    /* Card Metrics Customizados */
    .kpi-card {
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px 20px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 174, 66, 0.4);
        box-shadow: 0 8px 25px rgba(0, 174, 66, 0.1);
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F8FAFC;
    }
    .kpi-sub {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .kpi-positive { color: #10B981; }
    .kpi-neutral { color: #38BDF8; }
    .kpi-accent { color: #A855F7; }

    /* Estilo de Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #94A3B8;
        background: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 174, 66, 0.15) !important;
        color: #00AE42 !important;
        border: 1px solid rgba(0, 174, 66, 0.3) !important;
    }

    /* Botão Principal */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00AE42 0%, #008733 100%);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        box-shadow: 0 4px 15px rgba(0, 174, 66, 0.35);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #00C44B 0%, #00AE42 100%);
        box-shadow: 0 6px 20px rgba(0, 174, 66, 0.5);
        transform: translateY(-1px);
        color: #FFFFFF;
    }

    /* Veredito Card */
    .verdict-approved {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 95, 70, 0.15) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 12px;
        padding: 16px 20px;
        color: #6EE7B7;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .verdict-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(180, 83, 9, 0.15) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
        padding: 16px 20px;
        color: #FCD34D;
        font-weight: 700;
    }

    /* Caixa de Código e Anúncios */
    .stTextArea textarea {
        background-color: #0F172A !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }

    /* Tabelas */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HERO BANNER DE TOPO
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div>
        <div class="hero-title">⚡ Bambu Studio Intelligence Pro</div>
        <div class="hero-subtitle">Plataforma autônoma de análise de viabilidade, inteligência competitiva e geração de catálogo para Bambu Lab A1.</div>
    </div>
    <div>
        <span class="bambu-badge">PRO EDITION • 256mm³</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR COM PARÂMETROS OPERACIONAIS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Parâmetros da Máquina")
    st.caption("Custos de insumos e setup elétrico da Bambu Lab A1")

    preco_filamento = st.number_input("Custo do Filamento (R$/kg)", min_value=30.0, max_value=400.0, value=95.0, step=5.0)
    potencia_w = st.number_input("Consumo da Bambu A1 (Watts)", min_value=50.0, max_value=500.0, value=140.0, step=10.0)
    tarifa_kwh = st.number_input("Tarifa Elétrica (R$/kWh)", min_value=0.3, max_value=2.0, value=0.95, step=0.05)
    custo_embalagem = st.number_input("Caixa + Fita + Proteção (R$)", min_value=0.0, max_value=20.0, value=3.00, step=0.50)
    margem_meta = st.slider("Meta de Margem Líquida (%)", min_value=20, max_value=70, value=35, step=5) / 100.0

    st.markdown("---")
    st.markdown("### 💡 Guia Rápido")
    st.caption("1. Abra seu modelo no **Bambu Studio**\n2. Clique em **Fatiar (Slice)**\n3. Pegue os **gramas** e **minutos** e preencha no painel!")


# ---------------------------------------------------------------------------
# TABS PRINCIPAIS
# ---------------------------------------------------------------------------
tab_agente, tab_calculadora, tab_atendimento, tab_historico = st.tabs([
    "🤖 Agente Autônomo & IA",
    "🧮 Simulador de Margem e Taxas",
    "💬 Agente de Atendimento & Vendas",
    "📊 Histórico & Planilhas Excel"
])



# ===========================================================================
# ABA 1: AGENTE AUTÔNOMO COMPLETO
# ===========================================================================
with tab_agente:
    st.markdown("#### 🎯 Analisar Nova Oportunidade de Mercado")
    st.caption("O Agente cruzará a física de produção da sua máquina com a oferta real dos concorrentes no Mercado Livre.")

    c_nome, c_peso, c_tempo = st.columns([2.5, 1, 1])
    with c_nome:
        nome_produto = st.text_input("Nome da Peça ou Acessório", value="Suporte de Controle PS5 Gamer")
    with c_peso:
        peso_g = st.number_input("Peso Fatiado (g)", min_value=1.0, max_value=1500.0, value=85.0, step=5.0)
    with c_tempo:
        tempo_h = st.number_input("Tempo de Impressão (h)", min_value=0.1, max_value=50.0, value=2.2, step=0.2)

    termo_busca = st.text_input("Termo de Busca para o Robô Espião", value=f"{nome_produto} 3d")

    btn_executar = st.button("🚀 Executar Análise com Agente Autônomo", use_container_width=True)

    if btn_executar:
        # 1. Cálculo de Custos
        with st.spinner("⚙️ [1/3] Calculando custos exatos na Bambu Lab A1..."):
            custos = calcular_custo_impressao(
                peso_gramas=peso_g,
                tempo_horas=tempo_h,
                preco_kg_filamento=preco_filamento,
                potencia_watts=potencia_w,
                preco_kwh=tarifa_kwh,
                custo_embalagem=custo_embalagem
            )
            custo_total = custos["custo_total"]
            preco_min = sugerir_preco_venda(custo_total, margem_lucro_desejada=margem_meta, marketplace="mercadolivre")

        # 2. Web Scraping
        with st.spinner(f"🌐 [2/3] Robô abrindo o Chrome e minerando anúncios de '{termo_busca}'..."):
            produtos = minerar_mercado_livre(termo_busca, max_produtos=20)
            df_produtos = pd.DataFrame(produtos) if produtos else pd.DataFrame()

        # 3. Estatísticas e Decisão
        if not df_produtos.empty and "Preço (R$)" in df_produtos.columns:
            precos = df_produtos[df_produtos["Preço (R$)"] > 0]["Preço (R$)"]
            p_min = precos.min() if not precos.empty else 0.0
            p_med = precos.mean() if not precos.empty else 0.0
            p_max = precos.max() if not precos.empty else 0.0
        else:
            p_min, p_med, p_max = preco_min["preco_venda"], preco_min["preco_venda"] * 1.2, preco_min["preco_venda"] * 1.5

        taxa_ml = 0.14
        taxa_fixa = 6.50
        comissao_ao_preco_medio = (p_med * taxa_ml) + taxa_fixa
        lucro_ao_preco_medio = p_med - custo_total - comissao_ao_preco_medio
        margem_real = (lucro_ao_preco_medio / p_med) if p_med > 0 else 0

        st.markdown("<br>", unsafe_allow_html=True)

        # RENDERIZAÇÃO DOS CARDS ESTILIZADOS
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Custo de Produção</div>
                <div class="kpi-value">R$ {custo_total:.2f}</div>
                <div class="kpi-sub kpi-neutral">Filamento: R$ {custos['filamento']:.2f} | Luz: R$ {custos['energia']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Preço Médio Mercado</div>
                <div class="kpi-value">R$ {p_med:.2f}</div>
                <div class="kpi-sub kpi-accent">Mín: R$ {p_min:.0f} • Máx: R$ {p_max:.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Lucro Líquido no Bolso</div>
                <div class="kpi-value">R$ {lucro_ao_preco_medio:.2f}</div>
                <div class="kpi-sub kpi-positive">Margem Real: {margem_real*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with k4:
            if margem_real >= margem_meta:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: rgba(16, 185, 129, 0.5);">
                    <div class="kpi-label">Veredito do Agente</div>
                    <div class="kpi-value" style="color: #10B981; font-size: 1.4rem;">✅ APROVADO</div>
                    <div class="kpi-sub kpi-positive">Alta rentabilidade na A1</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="kpi-card" style="border-color: rgba(245, 158, 11, 0.5);">
                    <div class="kpi-label">Veredito do Agente</div>
                    <div class="kpi-value" style="color: #F59E0B; font-size: 1.3rem;">⚠️ ATENÇÃO</div>
                    <div class="kpi-sub" style="color: #FCD34D;">Margem abaixo da meta</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # TABELA DE CONCORRENTES
        if not df_produtos.empty:
            with st.expander(f"🔍 Ver {len(df_produtos)} Anúncios de Concorrentes Minerados em Tempo Real", expanded=False):
                st.dataframe(
                    df_produtos[["Título", "Preço (R$)", "Destaque", "Link"]],
                    use_container_width=True,
                    column_config={"Link": st.column_config.LinkColumn("Link do Anúncio")}
                )

        # GERAÇÃO DO ANÚNCIO COM IA
        with st.spinner("🧠 [3/3] Inteligência Artificial (Gemini) redigindo seu anúncio com copywriting persuasivo..."):
            contexto = ""
            if not df_produtos.empty:
                amostra = [f"- R$ {r['Preço (R$)']:.2f} | {r['Título']}" for _, r in df_produtos.head(8).iterrows()]
                contexto = "\n".join(amostra)
            
            preco_recomendado = max(preco_min["preco_venda"], p_med * 0.95)
            anuncio_gerado = criar_anuncio_com_ia(nome_produto, contexto, preco_sugerido=preco_recomendado)

        if anuncio_gerado:
            st.markdown("---")
            st.markdown("#### 📝 Anúncio Otimizado para Mercado Livre & Shopee")
            st.caption("Gerado com base nas palavras-chave mais buscadas e diferenciais da Bambu Lab A1.")
            st.text_area("Copie o anúncio completo pronto para publicar:", value=anuncio_gerado, height=360)


# ===========================================================================
# ABA 2: CALCULADORA RÁPIDA DE CUSTOS & TAXAS
# ===========================================================================
with tab_calculadora:
    st.markdown("#### 🧮 Simulação Imediata de Custos e Margem")
    st.caption("Calcule na hora o impacto das taxas do Mercado Livre e Shopee antes de ligar a impressora.")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        calc_peso = st.number_input("Peso do Modelo (g)", value=95.0, step=5.0, key="sim_p")
    with sc2:
        calc_tempo = st.number_input("Tempo na Bambu A1 (horas)", value=2.2, step=0.2, key="sim_t")
    with sc3:
        calc_margem = st.slider("Margem Desejada (%)", 20, 65, 35, 5, key="sim_m") / 100.0

    res_custos = calcular_custo_impressao(
        peso_gramas=calc_peso,
        tempo_horas=calc_tempo,
        preco_kg_filamento=preco_filamento,
        potencia_watts=potencia_w,
        preco_kwh=tarifa_kwh,
        custo_embalagem=custo_embalagem
    )

    st.markdown("<br>", unsafe_allow_html=True)
    c_f1, c_f2, c_f3, c_f4, c_f5 = st.columns(5)
    c_f1.metric("Filamento", f"R$ {res_custos['filamento']:.2f}")
    c_f2.metric("Energia Elétrica", f"R$ {res_custos['energia']:.2f}")
    c_f3.metric("Manutenção/Deprec.", f"R$ {res_custos['depreciacao']:.2f}")
    c_f4.metric("Embalagem", f"R$ {res_custos['embalagem']:.2f}")
    c_f5.metric("Custo Total", f"R$ {res_custos['custo_total']:.2f}")

    st.markdown("---")
    col_ml_box, col_sh_box = st.columns(2)

    with col_ml_box:
        v_ml = sugerir_preco_venda(res_custos["custo_total"], margem_lucro_desejada=calc_margem, marketplace="mercadolivre")
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #FFE600;">
            <div style="font-weight: 700; color: #FFE600; margin-bottom: 8px;">🟡 MERCADO LIVRE (Clássico)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">Vender por R$ {v_ml['preco_venda']:.2f}</div>
            <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 6px;">
                • Taxas Totais: -R$ {v_ml['comissao_total']:.2f}<br>
                • <b>Seu Lucro Limpo: R$ {v_ml['lucro_liquido']:.2f}</b> ({v_ml['margem_real_percentual']:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_sh_box:
        v_sh = sugerir_preco_venda(res_custos["custo_total"], margem_lucro_desejada=calc_margem, marketplace="shopee")
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #EE4D2D;">
            <div style="font-weight: 700; color: #EE4D2D; margin-bottom: 8px;">🟠 SHOPEE (Programa de Frete Grátis)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">Vender por R$ {v_sh['preco_venda']:.2f}</div>
            <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 6px;">
                • Taxas Totais: -R$ {v_sh['comissao_total']:.2f}<br>
                • <b>Seu Lucro Limpo: R$ {v_sh['lucro_liquido']:.2f}</b> ({v_sh['margem_real_percentual']:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)


# ===========================================================================
# ABA 3: AGENTE DE ATENDIMENTO & PRÉ-VENDA COM IA
# ===========================================================================
with tab_atendimento:
    st.markdown("#### 💬 Agente de Atendimento & Respostas de Alta Conversão")
    st.caption("Responda dúvidas de clientes no Mercado Livre e Shopee em segundos com copywriting profissional e gatilhos de fechamento.")

    c_atend_prod, c_atend_detalhes = st.columns([1.5, 2])
    with c_atend_prod:
        prod_atendimento = st.text_input("Produto Relacionado", value="Suporte de Controle PS5 Gamer de Mesa", key="atend_prod")
    with c_atend_detalhes:
        detalhes_custom = st.text_input("Detalhes da Peça (Opcional)", placeholder="Ex: Acompanha fita dupla face 3M, disponível em preto e branco...", key="atend_detalhes")

    st.markdown("##### ❓ Dúvida do Cliente no Anúncio:")
    
    # Botões rápidos com dúvidas comuns de compradores
    st.caption("Sugestões rápidas de perguntas frequentes:")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    pergunta_padrao = ""
    if col_b1.button("🎮 Serve com capa/capinha?"):
        st.session_state["duvida_cliente"] = "Serve no controle com capa de silicone ou fica muito apertado?"
    if col_b2.button("🚚 Tem pronta entrega / envia hoje?"):
        st.session_state["duvida_cliente"] = "Tem a pronta entrega na cor preta? Envia no mesmo dia?"
    if col_b3.button("🎨 Tem outras cores / faz personalizado?"):
        st.session_state["duvida_cliente"] = "Você faz em outras cores ou grava meu nome/gamertag na peça?"
    if col_b4.button("🏋️ Aguenta quanto peso / é resistente?"):
        st.session_state["duvida_cliente"] = "Esse suporte aguenta o peso sem quebrar com o tempo? O material é firme?"

    duvida_input = st.text_area(
        "Digite ou cole aqui a dúvida que o cliente perguntou no anúncio:",
        value=st.session_state.get("duvida_cliente", "Serve no controle com capa de silicone ou fica apertado?"),
        height=90,
        key="duvida_text_area"
    )

    btn_responder = st.button("⚡ Gerar Resposta Persuasiva com IA", type="primary", use_container_width=True)

    if btn_responder and duvida_input:
        with st.spinner("🤖 Agente analisando a dúvida e redigindo a melhor resposta de conversão..."):
            resposta_ia = responder_duvida_cliente(
                pergunta_cliente=duvida_input,
                nome_produto=prod_atendimento,
                detalhes_produto=detalhes_custom
            )

        if resposta_ia:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid #10B981;">
                <div style="font-weight: 700; color: #10B981; font-size: 1.1rem; margin-bottom: 8px;">
                    ✨ Resposta Pronta para Copiar e Colar
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.text_area("Selecione e copie o texto abaixo:", value=resposta_ia, height=350, key="resposta_box")


# ===========================================================================
# ABA 4: HISTÓRICO DE PESQUISAS & PLANILHAS
# ===========================================================================
with tab_historico:

    st.markdown("#### 📁 Central de Planilhas e Concorrentes")
    st.caption("Acesse os dados brutos minerados pelo robô para abrir no Excel ou cruzar dados.")

    arquivos_csv = glob.glob(os.path.join("pesquisas", "*.csv"))
    if arquivos_csv:
        escolha_csv = st.selectbox("Selecione um arquivo de pesquisa gravado:", arquivos_csv)
        if escolha_csv:
            df_hist = pd.read_csv(escolha_csv)
            st.dataframe(df_hist, use_container_width=True)

            with open(escolha_csv, "rb") as f:
                st.download_button(
                    label="📥 Baixar Planilha para o Excel (.CSV)",
                    data=f,
                    file_name=os.path.basename(escolha_csv),
                    mime="text/csv",
                    type="primary"
                )
    else:
        st.info("Nenhuma planilha encontrada na pasta 'pesquisas'. Execute uma análise com o Agente para minerar dados!")
