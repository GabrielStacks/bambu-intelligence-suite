"""
=============================================================================
AGENTE DE ATENDIMENTO E CONVERSÃO - MERCADO LIVRE & SHOPEE
Bambu Lab A1 - Respostas Rápidas de Alta Conversão com IA
=============================================================================
Objetivo:
Receber dúvidas reais de clientes feitas no anúncio (ex: "Serve no modelo X?",
"Tem na cor branca?", "Aguenta quantos kg?"), consultar as características
da peça impressa na Bambu Lab A1 e redigir respostas imediatas, educadas e
com gatilhos de fechamento de venda.
=============================================================================
"""

import sys
import os
from dotenv import load_dotenv

# Garante suporte a UTF-8 e emojis no terminal do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from gerador_anuncios import obter_chave_api


def responder_duvida_cliente(
    pergunta_cliente: str,
    nome_produto: str = "Peça em Impressão 3D Bambu Lab A1",
    detalhes_produto: str = ""
) -> str:
    """
    Aciona o Gemini para redigir uma resposta profissional com gatilhos de fechamento.
    """
    api_key = obter_chave_api()
    if not api_key:
        return "⚠️ Chave de API do Gemini não configurada."

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"⚠️ Erro ao inicializar cliente Google Gemini: {e}"

    prompt = f"""
Você é o atendente de pós-venda e pré-venda número 1 de uma loja profissional de e-commerce no Mercado Livre e Shopee, especializada em produtos de alta precisão feitos na impressora 3D Bambu Lab A1.

Sua missão: Responder à dúvida de um cliente de forma extremamente educada, rápida, segura e com um gatilho de fechamento que estimule a compra imediata.

DADOS DO PRODUTO:
- Nome do Produto: {nome_produto}
- Detalhes / Especificações: {detalhes_produto if detalhes_produto else "Fabricado em material de alta resistência (PLA Premium ou PETG ecológico), acabamento premium uniforme sem rebarbas, encaixe sob medida, testado rigorosamente."}

DÚVIDA DO CLIENTE:
"{pergunta_cliente}"

REGRAS ESTREITAS DE ATENDIMENTO DE MARKETPLACE:
1. NUNCA dê respostas secas como apenas "Sim" ou "Não".
2. Comece com uma saudação calorosa (ex: "Olá! Tudo bem? Agradecemos o seu contato!").
3. Responda diretamente e com segurança à pergunta técnica.
4. Destaque a qualidade superior da impressão na Bambu Lab A1 (acabamento impecável e alta resistência).
5. Inclua um gatilho de fechamento sutil (ex: "Temos a pronta entrega e postamos rapidamente para você!", "Garanta o seu hoje mesmo!", "Qualquer outra dúvida estamos à total disposição.").
6. Respeite as regras do Mercado Livre: NUNCA mencione telefone, WhatsApp, dados de contato externos ou outros sites.

Entregue:
1. 🌟 RESPOSTA PRINCIPAL RECOMENDADA (Ideal para copiar e colar no campo de perguntas)
2. ⚡ OPÇÃO MAIS CURTA (Para respostas rápidas no chat da Shopee)
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Erro na geração da IA: {e}"


def menu():
    print("\n" + "💬 " + "=" * 60)
    print("   AGENTE DE ATENDIMENTO E VENDAS COM IA")
    print("   Bambu Lab A1 - Mercado Livre & Shopee")
    print("=" * 64)
    print("1 - Responder dúvida de cliente")
    print("2 - Testar perguntas frequentes de exemplo")
    print("3 - Sair")

    while True:
        op = input("\n👉 Escolha uma opção (1, 2 ou 3): ").strip()

        if op == "1":
            nome = input("\nNome do produto anunciado (ex: Suporte de Controle PS5): ").strip()
            if not nome:
                nome = "Suporte de Controle PS5"
            pergunta = input("Cole a pergunta que o cliente fez: ").strip()
            if not pergunta:
                print("⚠️ A pergunta não pode estar vazia.")
                continue

            print("\n🤖 O Agente está redigindo a melhor resposta de conversão...")
            resposta = responder_duvida_cliente(pergunta, nome_produto=nome)
            print("\n" + "=" * 64)
            print(resposta)
            print("=" * 64)

        elif op == "2":
            exemplos = [
                ("Suporte Controle PS5 Gamer", "Serve no controle com capinha de silicone ou fica apertado?"),
                ("Suporte Tomada Alexa Echo Dot", "Vocês têm na cor preta a pronta entrega? Envia hoje?"),
                ("Suporte de Headset de Mesa", "Aguenta fone pesado tipo HyperX Cloud sem tombar?")
            ]
            print("\n📋 SELECIONE UM EXEMPLO REAL PARA TESTAR:")
            for i, (prod, perg) in enumerate(exemplos, 1):
                print(f"   {i} - [{prod}]: '{perg}'")

            escolha = input("\nEscolha o exemplo (1, 2 ou 3): ").strip()
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(exemplos):
                    prod, perg = exemplos[idx]
                    print(f"\n🔍 Analisando: '{perg}' para o produto '{prod}'...")
                    resposta = responder_duvida_cliente(perg, nome_produto=prod)
                    print("\n" + "=" * 64)
                    print(resposta)
                    print("=" * 64)
                else:
                    print("⚠️ Opção inválida.")
            except ValueError:
                print("⚠️ Digite um número válido.")

        elif op == "3":
            print("\n👋 Agente de atendimento finalizado. Boas vendas!")
            break
        else:
            print("⚠️ Opção inválida. Digite 1, 2 ou 3.")


if __name__ == "__main__":
    menu()
