"""
=============================================================================
SISTEMA DE PRECIFICAÇÃO E VIABILIDADE - BAMBU LAB A1
Marketplaces: Mercado Livre e Shopee
=============================================================================
Objetivo:
Calcular o custo real de cada impressão 3D (filamento, energia, desgaste e embalagem)
e descobrir o preço exato de venda para garantir o lucro líquido desejado,
já descontando todas as taxas dos marketplaces.
=============================================================================
"""
import sys

# Garante suporte a UTF-8 e emojis no terminal do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def calcular_custo_impressao(
    peso_gramas: float,
    tempo_horas: float,
    preco_kg_filamento: float = 95.0,     # Preço médio de 1kg de PLA/PETG de boa qualidade
    potencia_watts: float = 140.0,         # Consumo médio real da Bambu Lab A1 (~140W)
    preco_kwh: float = 0.95,               # Custo médio da energia no Brasil por kWh (~R$ 0,95)
    custo_embalagem: float = 3.00,         # Caixinha de papelão + fita + saquinho/plástico bolha
    custo_impressora: float = 3800.0,      # Valor estimado da Bambu A1
    vida_util_horas: float = 5000.0        # Estimativa de vida útil da máquina para depreciação
) -> dict:
    """Calcula os custos de fabricação e insumos da peça."""

    # 1. Custo de matéria-prima (filamento usado)
    custo_filamento = (peso_gramas / 1000.0) * preco_kg_filamento

    # 2. Custo de energia elétrica consumida
    # Fórmula: (Potência em Watts / 1000) * horas * tarifa do kWh
    energia_kwh = (potencia_watts / 1000.0) * tempo_horas
    custo_energia = energia_kwh * preco_kwh

    # 3. Depreciação e manutenção da máquina (reserva para trocar bicos, correias e pagar a máquina)
    custo_depreciacao = (custo_impressora / vida_util_horas) * tempo_horas

    # 4. Custo total de produção (soma de tudo antes da venda)
    custo_total_producao = custo_filamento + custo_energia + custo_depreciacao + custo_embalagem

    return {
        "filamento": custo_filamento,
        "energia": custo_energia,
        "depreciacao": custo_depreciacao,
        "embalagem": custo_embalagem,
        "custo_total": custo_total_producao
    }


def sugerir_preco_venda(custo_producao: float, margem_lucro_desejada: float = 0.35, marketplace: str = "shopee") -> dict:
    """
    Calcula o preço de venda necessário para sobrar a margem limpa no seu bolso.
    
    Taxas padrão:
    - Shopee: ~20% (14% comissão + 6% programa de frete grátis) + R$ 4,00 taxa fixa por item.
    - Mercado Livre: ~14% (Clássico) ou ~19% (Premium) + R$ 6,50 taxa fixa por item abaixo de R$ 79.
    """
    if marketplace.lower() == "shopee":
        taxa_percentual = 0.20
        taxa_fixa = 4.00
    else: # Mercado Livre (Clássico)
        taxa_percentual = 0.14
        taxa_fixa = 6.50

    # Fórmula reversa para descobrir o Preço de Venda (PV):
    # PV = (Custo de Produção + Taxa Fixa) / (1 - Taxa Percentual - Margem de Lucro Desejada)
    divisor = 1.0 - taxa_percentual - margem_lucro_desejada
    if divisor <= 0:
        raise ValueError("A margem de lucro desejada somada às taxas ultrapassa 100%!")

    preco_venda = (custo_producao + taxa_fixa) / divisor
    comissao_marketplace = (preco_venda * taxa_percentual) + taxa_fixa
    lucro_liquido = preco_venda - custo_producao - comissao_marketplace

    return {
        "marketplace": marketplace.upper(),
        "preco_venda": preco_venda,
        "comissao_total": comissao_marketplace,
        "lucro_liquido": lucro_liquido,
        "margem_real_percentual": (lucro_liquido / preco_venda) * 100
    }


def exibir_relatorio(nome_produto: str, peso_g: float, tempo_h: float):
    print("=" * 65)
    print(f"📦 ANÁLISE DE PRODUTO: {nome_produto.upper()}")
    print(f"⚙️  Dados da Bambu A1: {peso_g}g de filamento | {tempo_h:.1f} horas de impressão")
    print("=" * 65)

    custos = calcular_custo_impressao(peso_gramas=peso_g, tempo_horas=tempo_h)
    print("\n💰 1. CUSTOS DE PRODUÇÃO:")
    print(f"   • Filamento:     R$ {custos['filamento']:.2f}")
    print(f"   • Energia:       R$ {custos['energia']:.2f}")
    print(f"   • Depreciação:   R$ {custos['depreciacao']:.2f}")
    print(f"   • Embalagem:     R$ {custos['embalagem']:.2f}")
    print(f"   👉 CUSTO TOTAL:  R$ {custos['custo_total']:.2f}")

    print("\n🏷️  2. SIMULAÇÃO DE PREÇO DE VENDA (Margem desejada: 35% líquido):")
    for mkt in ["Shopee", "Mercado Livre"]:
        res = sugerir_preco_venda(custos['custo_total'], margem_lucro_desejada=0.35, marketplace=mkt)
        print(f"\n   [{res['marketplace']}]:")
        print(f"   • Preço sugerido de venda: R$ {res['preco_venda']:.2f}")
        print(f"   • Taxas do marketplace:   -R$ {res['comissao_total']:.2f}")
        print(f"   • Seu Lucro Limpo no bolso: R$ {res['lucro_liquido']:.2f} ({res['margem_real_percentual']:.1f}%)")
    print("=" * 65)


def ler_float(mensagem: str, padrao: float = None) -> float:
    """Função auxiliar para ler números do teclado sem travar se o usuário errar."""
    while True:
        sugestao = f" [Padrão: {padrao}]" if padrao is not None else ""
        entrada = input(f"{mensagem}{sugestao}: ").strip().replace(",", ".")
        if not entrada and padrao is not None:
            return padrao
        try:
            valor = float(entrada)
            if valor <= 0:
                print("   ⚠️  O valor deve ser maior que zero. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("   ⚠️  Entrada inválida. Digite apenas números (ex: 85.5 ou 2).")


def menu_interativo():
    print("\n" + "🚀 " + "=" * 50)
    print("   CALCULADORA DE PREÇO REAL - BAMBU LAB A1")
    print("=" * 54)
    print("1 - Calcular novo produto personalizado")
    print("2 - Ver exemplos prontos (Headset Gamer e Alexa)")
    print("3 - Sair")
    
    while True:
        opcao = input("\n👉 Escolha uma opção (1, 2 ou 3): ").strip()
        
        if opcao == "1":
            print("\n--- NOVO CÁLCULO DE PRODUTO ---")
            nome = input("Nome da peça/produto: ").strip() or "Produto sem nome"
            peso = ler_float("Peso da peça fatiada no Bambu Studio (em gramas)")
            tempo = ler_float("Tempo de impressão na Bambu A1 (em horas decimais, ex: 2.5 para 2h30)")
            margem = ler_float("Margem de lucro desejada em %", padrao=35.0) / 100.0
            preco_filamento = ler_float("Custo do carretel de filamento (R$/kg)", padrao=95.0)

            # Executa o cálculo com os dados informados
            custos = calcular_custo_impressao(
                peso_gramas=peso,
                tempo_horas=tempo,
                preco_kg_filamento=preco_filamento
            )

            print("\n" + "=" * 65)
            print(f"📦 ANÁLISE: {nome.upper()}")
            print(f"⚙️  Bambu A1: {peso}g | {tempo:.1f}h | Filamento: R$ {preco_filamento:.2f}/kg")
            print("=" * 65)
            print("💰 1. CUSTOS DE PRODUÇÃO:")
            print(f"   • Filamento:     R$ {custos['filamento']:.2f}")
            print(f"   • Energia:       R$ {custos['energia']:.2f}")
            print(f"   • Depreciação:   R$ {custos['depreciacao']:.2f}")
            print(f"   • Embalagem:     R$ {custos['embalagem']:.2f}")
            print(f"   👉 CUSTO TOTAL:  R$ {custos['custo_total']:.2f}")

            print(f"\n🏷️  2. PREÇOS RECOMENDADOS (Margem: {margem*100:.0f}% líquido):")
            for mkt in ["Shopee", "Mercado Livre"]:
                res = sugerir_preco_venda(custos['custo_total'], margem_lucro_desejada=margem, marketplace=mkt)
                print(f"\n   [{res['marketplace']}]:")
                print(f"   • Preço sugerido de venda: R$ {res['preco_venda']:.2f}")
                print(f"   • Taxas do marketplace:   -R$ {res['comissao_total']:.2f}")
                print(f"   • Seu Lucro Limpo no bolso: R$ {res['lucro_liquido']:.2f} ({res['margem_real_percentual']:.1f}%)")
            print("=" * 65)

        elif opcao == "2":
            exibir_relatorio("Suporte de Fone/Headset Gamer", peso_g=110.0, tempo_h=2.5)
            exibir_relatorio("Suporte de Tomada para Alexa Echo Dot", peso_g=65.0, tempo_h=1.4)
            
        elif opcao == "3":
            print("\n👋 Encerrando. Bons lucros com a sua Bambu Lab A1!")
            break
        else:
            print("⚠️ Opção inválida. Digite 1, 2 ou 3.")


if __name__ == "__main__":
    menu_interativo()

