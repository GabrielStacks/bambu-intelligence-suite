"""
=============================================================================
GERADOR AUTÔNOMO DE ANÚNCIOS COM INTELIGÊNCIA ARTIFICIAL (GEMINI)
Bambu Lab A1 - Mercado Livre e Shopee
=============================================================================
Objetivo:
Utilizar a IA gratuita do Google (Gemini) para transformar dados brutos e pesquisas
de concorrentes em anúncios completos de alta conversão: títulos otimizados para SEO,
descrições persuasivas, fichas técnicas e tags de busca.
=============================================================================
"""

import sys
import os
import glob
import pandas as pd
from dotenv import load_dotenv

# Garante suporte a UTF-8 e emojis no terminal do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Carrega variáveis do arquivo .env
load_dotenv()


def obter_chave_api(forcar_nova: bool = False) -> str:
    """Verifica se a chave do Gemini existe ou solicita ao usuário para salvar."""
    if not forcar_nova:
        chave = os.getenv("GEMINI_API_KEY")
        if chave and len(chave.strip()) > 15:
            return chave.strip()

    print("\n" + "🔑 " + "=" * 60)
    print("   CONFIGURAÇÃO DA CHAVE GRATUITA DO GOOGLE GEMINI")
    print("=" * 64)
    print("Para usar a Inteligência Artificial, você só precisa de uma")
    print("chave gratuita do Google AI Studio (não precisa de cartão).")
    print("\n👉 Passo a passo rápido (leva 1 minuto):")
    print("   1. Acesse: https://aistudio.google.com/app/apikey")
    print("   2. Faça login com sua conta Google/Gmail")
    print("   3. Clique no botão 'Create API key' (ou 'Criar chave de API')")
    print("   4. Copie a chave gerada (começa com 'AIzaSy...')")
    print("=" * 64)

    while True:
        nova_chave = input("\n👉 Cole sua chave de API do Gemini aqui e aperte ENTER: ").strip()
        if not nova_chave:
            print("⚠️ Chave não pode ser vazia. Tente novamente.")
            continue
        if len(nova_chave) < 15:
            print("⚠️ Essa chave parece muito curta. As chaves do Google Gemini costumam ter cerca de 39 caracteres e começar com 'AIzaSy...'.")
            confirma = input("Tem certeza que essa é a chave correta? (s/n): ").strip().lower()
            if confirma != "s":
                continue

        # Salva no arquivo .env substituindo qualquer chave anterior
        linhas = []
        if os.path.exists(".env"):
            with open(".env", "r", encoding="utf-8") as f:
                linhas = [l for l in f.readlines() if not l.strip().startswith("GEMINI_API_KEY=")]
        
        linhas.append(f"GEMINI_API_KEY={nova_chave}\n")
        with open(".env", "w", encoding="utf-8") as f:
            f.writelines(linhas)

        os.environ["GEMINI_API_KEY"] = nova_chave
        print("✅ Chave salva com sucesso no arquivo .env!\n")
        return nova_chave



def criar_anuncio_com_ia(nome_produto: str, contexto_concorrentes: str = "", preco_sugerido: float = 0.0) -> str:
    """Conecta à API do Gemini e gera o anúncio completo com copywriting profissional."""
    api_key = obter_chave_api()
    if not api_key:
        return ""

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"⚠️ Erro ao inicializar cliente Google Gemini: {e}")
        return ""

    print("\n🧠 Conectando ao cérebro do Gemini para criar o anúncio...")

    prompt = f"""
Você é um especialista sênior em E-commerce, Copywriting e SEO para os marketplaces Mercado Livre e Shopee, focado em produtos de Impressão 3D de alta qualidade fabricados na impressora Bambu Lab A1.

Crie um anúncio completo e altamente persuasivo para o seguinte produto:
PRODUTO: {nome_produto}
PREÇO SUGERIDO: R$ {preco_sugerido:.2f} se houver

DADOS DE CONCORRENTES MAIS VENDIDOS NO MERCADO LIVRE (Inspire-se no vocabulário e nas palavras que os compradores buscam):
{contexto_concorrentes if contexto_concorrentes else "Não fornecido"}

Por favor, estruture a sua resposta exatamente com estas seções:

1. 🎯 3 OPÇÕES DE TÍTULOS (SEO):
   - Máximo de 60 caracteres por título (regra estrita do Mercado Livre).
   - Use palavras-chave fortes que as pessoas realmente buscam (ex: modelo compatível, utilidade, 3D, suporte, organizador).

2. 💡 DIFERENCIAIS DA PEÇA (Por que comprar esta e não a dos concorrentes):
   - Fabricada na moderna impressora Bambu Lab A1 (alta precisão dimensional, camadas uniformes e acabamento premium sem fiapos).
   - Material de alta resistência (PLA Premium ou PETG ecológico e durável).
   - Encaixe perfeito e testado.

3. 📝 DESCRIÇÃO COMPLETA DE VENDAS (Pronta para copiar e colar):
   - Título chamativo com emojis elegantes.
   - Parágrafo de gancho (resolvendo a dor: bagunça na mesa, risco de queda do acessório, organização elegante do setup).
   - Lista de Benefícios e Características Principais.
   - Ficha Técnica completa (Material, Dimensões aproximadas, Peso, Compatibilidade).
   - Conteúdo da Embalagem.
   - Observações e Cuidados (ex: limpeza com pano úmido, não expor a calor excessivo acima de 60°C).

4. 🏷️ 10 PALAVRAS-CHAVE / TAGS DE BUSCA:
   - Termos separados por vírgula para cadastrar nos campos de busca da Shopee e Mercado Livre.
"""

    try:
        # Usa o modelo Gemini 2.5 Flash (rápido, moderno e gratuito)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        msg_erro = str(e)
        print(f"\n⚠️ Erro na comunicação com o Gemini: {msg_erro}")
        if "API_KEY_INVALID" in msg_erro or "API key not valid" in msg_erro or "400" in msg_erro:
            print("\n🚨 Parece que a sua chave da API do Gemini está incorreta ou inválida!")
            trocar = input("👉 Deseja digitar uma nova chave agora? (s/n): ").strip().lower()
            if trocar == "s":
                nova_chave = obter_chave_api(forcar_nova=True)
                if nova_chave:
                    return criar_anuncio_com_ia(nome_produto, contexto_concorrentes, preco_sugerido)
        return ""


def listar_pesquisas_disponiveis() -> list[str]:
    """Busca planilhas CSV geradas pelo nosso robô espião de mercado."""
    arquivos = glob.glob(os.path.join("pesquisas", "pesquisa_*.csv"))
    return sorted(arquivos, key=os.path.getmtime, reverse=True)


def carregar_dados_pesquisa(caminho_csv: str) -> tuple[str, str, float]:
    """Lê a planilha de concorrentes para usar como base para a IA."""
    df = pd.read_csv(caminho_csv)
    nome_base = os.path.basename(caminho_csv).replace("pesquisa_", "").split("_202")[0].replace("_", " ").title()

    precos = df[df["Preço (R$)"] > 0]["Preço (R$)"]
    preco_medio = precos.mean() if not precos.empty else 0.0

    amostra_titulos = []
    for _, row in df.head(8).iterrows():
        amostra_titulos.append(f"- R$ {row['Preço (R$)']:.2f} | {row['Título']}")

    contexto = "\n".join(amostra_titulos)
    return nome_base, contexto, preco_medio


def salvar_anuncio(nome_produto: str, conteudo_anuncio: str):
    pasta_anuncios = "anuncios"
    os.makedirs(pasta_anuncios, exist_ok=True)

    nome_arquivo = "".join(c for c in nome_produto if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_").lower()
    caminho = os.path.join(pasta_anuncios, f"anuncio_{nome_arquivo}.txt")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo_anuncio)

    print("\n" + "💾 " + "=" * 60)
    print("   ANÚNCIO SALVO COM SUCESSO!")
    print("=" * 64)
    print(f"   👉 Arquivo: {os.path.abspath(caminho)}")
    print("   (Você pode abrir no Bloco de Notas ou VS Code para copiar e colar)")
    print("=" * 64)


def menu():
    print("\n" + "🚀 " + "=" * 60)
    print("   GERADOR AUTÔNOMO DE ANÚNCIOS COM IA - GEMINI")
    print("   Bambu Lab A1 - Mercado Livre & Shopee")
    print("=" * 64)
    print("1 - Criar anúncio a partir de uma pesquisa recente de mercado")
    print("2 - Criar anúncio digitando o produto manualmente")
    print("3 - Redefinir / Alterar chave da API do Gemini")
    print("4 - Sair")

    while True:
        op = input("\n👉 Escolha uma opção (1, 2, 3 ou 4): ").strip()

        if op == "1":
            pesquisas = listar_pesquisas_disponiveis()
            if not pesquisas:
                print("\n⚠️ Nenhuma pesquisa encontrada na pasta 'pesquisas'.")
                print("   Rode primeiro o 'pesquisador_mercado.py' para minerar concorrentes.")
                continue

            print("\n📁 PLANILHAS DE CONCORRENTES ENCONTRADAS:")
            for i, p in enumerate(pesquisas[:5], 1):
                nome = os.path.basename(p)
                print(f"   {i} - {nome}")

            escolha = input("\nEscolha o número da pesquisa (ex: 1): ").strip()
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(pesquisas):
                    caminho_escolhido = pesquisas[idx]
                    nome_prod, contexto, preco_med = carregar_dados_pesquisa(caminho_escolhido)
                    print(f"\n📊 Analisando dados minerados de: {nome_prod}")
                    print(f"💰 Preço médio dos concorrentes: R$ {preco_med:.2f}")

                    anuncio = criar_anuncio_com_ia(nome_prod, contexto, preco_med)
                    if anuncio:
                        print("\n" + "=" * 64)
                        print(anuncio)
                        print("=" * 64)
                        salvar_anuncio(nome_prod, anuncio)
                else:
                    print("⚠️ Número inválido.")
            except ValueError:
                print("⚠️ Digite um número válido.")

        elif op == "2":
            nome = input("\nDigite o nome da peça/produto que vai imprimir: ").strip()
            if not nome:
                print("⚠️ Nome do produto não pode ser vazio.")
                continue
            anuncio = criar_anuncio_com_ia(nome)
            if anuncio:
                print("\n" + "=" * 64)
                print(anuncio)
                print("=" * 64)
                salvar_anuncio(nome, anuncio)

        elif op == "3":
            obter_chave_api(forcar_nova=True)

        elif op == "4":
            print("\n👋 Gerador encerrado. Boas vendas com a sua Bambu Lab A1!")
            break
        else:
            print("⚠️ Opção inválida. Digite 1, 2, 3 ou 4.")


if __name__ == "__main__":
    menu()

