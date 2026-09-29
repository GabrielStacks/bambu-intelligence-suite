"""
=============================================================================
AGENTE AUTÔNOMO GERENTE - BAMBU LAB A1
Orquestração Inteligente: Custos + Concorrentes + Decisão + IA
=============================================================================
Objetivo:
O Agente recebe uma ideia de produto em linguagem natural, aciona as ferramentas
necessárias (precificador e robô espião), analisa se a margem de lucro compensa
o investimento e, se for aprovado, gera automaticamente o anúncio e o dossiê completo.
=============================================================================
"""

import sys
import os
import re
import glob
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Garante suporte a UTF-8 e emojis no terminal do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

# Importa as ferramentas que construímos nos projetos anteriores
from precificador import calcular_custo_impressao, sugerir_preco_venda
from pesquisador_mercado import minerar_mercado_livre, extrair_preco
from gerador_anuncios import obter_chave_api, criar_anuncio_com_ia


class AgenteGerente3D:
    def __init__(self, margem_minima: float = 0.35):
        self.margem_minima = margem_minima
        self.pasta_dossies = "dossies"
        os.makedirs(self.pasta_dossies, exist_ok=True)

    def analisar_oportunidade(self, nome_produto: str, peso_g: float, tempo_h: float, termo_pesquisa: str = None) -> dict:
        """
        Ciclo Autônomo Completo do Agente:
        1. Calcula custos de fabricação na Bambu Lab A1
        2. Pesquisa preços reais praticados pelos concorrentes no Mercado Livre
        3. Compara custos vs preços de mercado e toma a decisão
        4. Se viável, gera anúncio persuasivo com IA
        5. Consolida um Dossiê Executivo completo
        """
        if not termo_pesquisa:
            termo_pesquisa = f"{nome_produto} 3d"

        print("\n" + "🤖 " + "=" * 65)
        print(f"   AGENTE GERENTE ATIVADO: '{nome_produto.upper()}'")
        print(f"   Peso: {peso_g}g | Tempo Bambu A1: {tempo_h:.1f}h | Margem Alvo: {self.margem_minima*100:.0f}%")
        print("=" * 69)

        # -------------------------------------------------------------
        # ETAPA 1: CÁLCULO DE CUSTOS DE FABRICAÇÃO
        # -------------------------------------------------------------
        print("\n⚙️  [1/4] Calculando custos de produção na Bambu Lab A1...")
        custos = calcular_custo_impressao(peso_gramas=peso_g, tempo_horas=tempo_h)
        custo_total = custos["custo_total"]
        preco_min_ml = sugerir_preco_venda(custo_total, margem_lucro_desejada=self.margem_minima, marketplace="mercadolivre")

        print(f"   • Custo Total de Produção: R$ {custo_total:.2f} (Filamento: R$ {custos['filamento']:.2f} | Luz: R$ {custos['energia']:.2f})")
        print(f"   • Preço Mínimo para atingir {self.margem_minima*100:.0f}% de lucro: R$ {preco_min_ml['preco_venda']:.2f}")

        # -------------------------------------------------------------
        # ETAPA 2: MINERAÇÃO DE CONCORRENTES NO MERCADO LIVRE
        # -------------------------------------------------------------
        print(f"\n🌐 [2/4] Enviando robô espião para pesquisar '{termo_pesquisa}'...")
        produtos_mercado = minerar_mercado_livre(termo_pesquisa, max_produtos=20)

        if not produtos_mercado:
            print("   ⚠️ Robô não encontrou concorrentes suficientes. Usando estimativa base.")
            preco_medio_mercado = preco_min_ml["preco_venda"] * 1.2
            menor_preco = preco_min_ml["preco_venda"]
            maior_preco = preco_min_ml["preco_venda"] * 1.5
        else:
            df = pd.DataFrame(produtos_mercado)
            precos = df[df["Preço (R$)"] > 0]["Preço (R$)"]
            preco_medio_mercado = precos.mean() if not precos.empty else preco_min_ml["preco_venda"]
            menor_preco = precos.min() if not precos.empty else 0.0
            maior_preco = precos.max() if not precos.empty else 0.0

            print(f"   • {len(produtos_mercado)} concorrentes minerados.")
            print(f"   • Preço Médio de Mercado: R$ {preco_medio_mercado:.2f} (Faixa: R$ {menor_preco:.2f} a R$ {maior_preco:.2f})")

        # -------------------------------------------------------------
        # ETAPA 3: TOMADA DE DECISÃO AUTÔNOMA
        # -------------------------------------------------------------
        print("\n🧠 [3/4] Agente avaliando viabilidade de negócio...")
        # Simula vender pelo preço médio praticado no mercado
        taxa_ml = 0.14
        taxa_fixa_ml = 6.50
        comissao_ao_preco_medio = (preco_medio_mercado * taxa_ml) + taxa_fixa_ml
        lucro_liquido_ao_preco_medio = preco_medio_mercado - custo_total - comissao_ao_preco_medio
        margem_real_ao_preco_medio = (lucro_liquido_ao_preco_medio / preco_medio_mercado) if preco_medio_mercado > 0 else 0

        viavel = margem_real_ao_preco_medio >= self.margem_minima

        if viavel:
            status_veredito = "✅ APROVADO COM EXCELENTE LUCRO"
            print(f"   👉 VEREDITO: {status_veredito}!")
            print(f"   • Vendendo pelo preço médio (R$ {preco_medio_mercado:.2f}), sobra R$ {lucro_liquido_ao_preco_medio:.2f} no bolso.")
            print(f"   • Margem líquida real de {margem_real_ao_preco_medio*100:.1f}% (Meta era {self.margem_minima*100:.0f}%).")
        else:
            status_veredito = "⚠️ ALERTA DE MARGEM BAIXA"
            print(f"   👉 VEREDITO: {status_veredito}!")
            print(f"   • O preço médio de mercado (R$ {preco_medio_mercado:.2f}) só dá margem de {margem_real_ao_preco_medio*100:.1f}%.")
            print(f"   • Recomendação: criar diferencial temático/personalizado para cobrar no mínimo R$ {preco_min_ml['preco_venda']:.2f}.")

        # -------------------------------------------------------------
        # ETAPA 4: GERAÇÃO DO ANÚNCIO COM IA (Se aprovado ou solicitado)
        # -------------------------------------------------------------
        print("\n✍️  [4/4] Agente acionando a IA para gerar anúncio otimizado...")
        contexto_concorrentes = ""
        if produtos_mercado:
            amostra = [f"- R$ {p['Preço (R$)']:.2f} | {p['Título']}" for p in produtos_mercado[:8]]
            contexto_concorrentes = "\n".join(amostra)

        preco_recomendado = max(preco_min_ml["preco_venda"], preco_medio_mercado * 0.95)
        anuncio = criar_anuncio_com_ia(nome_produto, contexto_concorrentes, preco_sugerido=preco_recomendado)

        # -------------------------------------------------------------
        # ETAPA 5: CONSOLIDAÇÃO DO DOSSIÊ
        # -------------------------------------------------------------
        nome_pasta = "".join(c for c in nome_produto if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_").lower()
        pasta_saida_produto = os.path.join(self.pasta_dossies, nome_pasta)
        os.makedirs(pasta_saida_produto, exist_ok=True)

        # Salva planilha de concorrentes na pasta do dossiê
        if produtos_mercado:
            df.to_csv(os.path.join(pasta_saida_produto, "concorrentes_analisados.csv"), index=False, encoding="utf-8-sig")

        # Salva o anúncio gerado
        if anuncio:
            with open(os.path.join(pasta_saida_produto, "anuncio_pronto.txt"), "w", encoding="utf-8") as f:
                f.write(anuncio)

        # Salva o Relatório Executivo do Agente
        relatorio_md = f"""# DOSSIÊ EXECUTIVO DE PRODUTO - BAMBU LAB A1
**Produto:** {nome_produto}  
**Data da Análise:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Veredito do Agente:** {status_veredito}  

---

### 1. Custos de Fabricação
- **Peso de Filamento:** {peso_g}g
- **Tempo de Impressão:** {tempo_h:.1f} horas
- **Custo de Matéria-Prima:** R$ {custos['filamento']:.2f}
- **Custo de Energia Elétrica:** R$ {custos['energia']:.2f}
- **Reserva de Manutenção/Máquina:** R$ {custos['depreciacao']:.2f}
- **Embalagem:** R$ {custos['embalagem']:.2f}
- **CUSTO TOTAL DE PRODUÇÃO:** R$ {custo_total:.2f}

---

### 2. Análise de Concorrentes no Mercado Livre
- **Anúncios Analisados:** {len(produtos_mercado)}
- **Menor Preço Encontrado:** R$ {menor_preco:.2f}
- **Preço Médio Praticado:** R$ {preco_medio_mercado:.2f}
- **Maior Preço Encontrado:** R$ {maior_preco:.2f}

---

### 3. Recomendação Estratégica do Agente
- **Preço Sugerido de Venda:** R$ {preco_recomendado:.2f}
- **Lucro Líquido Estimado por Peça:** R$ {preco_recomendado - custo_total - ((preco_recomendado * taxa_ml) + taxa_fixa_ml):.2f}
- **Margem de Lucro Real:** {((preco_recomendado - custo_total - ((preco_recomendado * taxa_ml) + taxa_fixa_ml)) / preco_recomendado) * 100:.1f}%

---

*Arquivos anexos nesta pasta:*
- `concorrentes_analisados.csv` (Planilha para abrir no Excel)
- `anuncio_pronto.txt` (Anúncio com títulos SEO e descrição para copiar e colar)
"""
        caminho_resumo = os.path.join(pasta_saida_produto, "resumo_executivo.md")
        with open(caminho_resumo, "w", encoding="utf-8") as f:
            f.write(relatorio_md)

        print("\n" + "🎉 " + "=" * 65)
        print(f"   DOSSIÊ COMPLETO GERADO PELO AGENTE COM SUCESSO!")
        print("=" * 69)
        print(f"   📁 Pasta do Projeto: {os.path.abspath(pasta_saida_produto)}")
        print(f"   📄 Resumo Executivo: {os.path.abspath(caminho_resumo)}")
        print("=" * 69)

        return {
            "status": status_veredito,
            "custo": custo_total,
            "preco_recomendado": preco_recomendado,
            "pasta": pasta_saida_produto
        }


def menu():
    agente = AgenteGerente3D(margem_minima=0.35)

    print("\n" + "🤖 " + "=" * 65)
    print("   AGENTE AUTÔNOMO GERENTE - BAMBU LAB A1")
    print("   Automação Ponta a Ponta: Custos + Concorrentes + Anúncio")
    print("=" * 69)
    print("1 - Analisar nova oportunidade de produto (Modo Completo)")
    print("2 - Ajustar meta de margem de lucro mínima (Atual: 35%)")
    print("3 - Sair")

    while True:
        op = input("\n👉 Escolha uma opção (1, 2 ou 3): ").strip()

        if op == "1":
            print("\n--- INFORME OS DADOS DA PEÇA (Obtidos no Bambu Studio) ---")
            nome = input("Nome da peça (ex: Suporte de Fone Gamer): ").strip()
            if not nome:
                nome = "Suporte de Fone Gamer"

            try:
                peso = float(input("Peso da peça fatiada em gramas (ex: 85): ").strip().replace(",", "."))
                tempo = float(input("Tempo de impressão em horas (ex: 2.2): ").strip().replace(",", "."))
            except ValueError:
                print("⚠️ Valores numéricos inválidos. Tente novamente.")
                continue

            termo = input(f"Termo para pesquisar concorrentes [Padrão: {nome} 3d]: ").strip()
            if not termo:
                termo = f"{nome} 3d"

            agente.analisar_oportunidade(
                nome_produto=nome,
                peso_g=peso,
                tempo_h=tempo,
                termo_pesquisa=termo
            )

        elif op == "2":
            try:
                nova_margem = float(input("Digite a nova margem mínima em % (ex: 40 para 40%): ").strip().replace(",", "."))
                agente.margem_minima = nova_margem / 100.0
                print(f"✅ Margem mínima atualizada para {nova_margem:.0f}%!")
            except ValueError:
                print("⚠️ Valor inválido.")

        elif op == "3":
            print("\n👋 Agente Gerente desativado. Boas vendas com a sua Bambu Lab A1!")
            break
        else:
            print("⚠️ Opção inválida. Digite 1, 2 ou 3.")


if __name__ == "__main__":
    menu()
