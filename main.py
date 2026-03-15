import requests
from bs4 import BeautifulSoup
import telebot
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"
bot = telebot.TeleBot(TOKEN)

# URL da página de ofertas (mais garantida que a de mais vendidos)
URL_OFERTAS = "https://www.mercadolivre.com.br/ofertas"

def buscar_melhor_oferta():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    try:
        res = requests.get(URL_OFERTAS, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Nova mira nos cards de produtos
        produtos = soup.find_all("div", {"class": "promotion-item__container"})[:5]
        
        # Se não achou com a classe acima, tenta a classe genérica
        if not produtos:
            produtos = soup.select(".poly-card__content")[:5]

        lista_posts = []
        for prod in produtos:
            try:
                # Tenta pegar o nome
                nome_tag = prod.find("p", {"class": "promotion-item__title"}) or prod.select_one(".poly-component__title")
                nome = nome_tag.text.strip()
                
                # Tenta pegar o link
                link = prod.find("a")['href']
                
                # Tenta pegar o preço
                preco_tag = prod.find("span", {"class": "promotion-item__price"}) or prod.select_one(".andes-money-amount__fraction")
                preco = preco_tag.text.strip()
                
                texto_post = (
                    f"🛍️ **OFERTA QUENTE NO MERCADO LIVRE**\n\n"
                    f"📦 {nome}\n"
                    f"💰 Por apenas: **R$ {preco}**\n\n"
                    f"🔗 Link: {link}\n\n"
                    f"🚀 *Sugestão do seu Bot de Ofertas*"
                )
                lista_posts.append(texto_post)
            except:
                continue
        return lista_posts
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return []

print("🚀 Bot de Ofertas MendeShop Ativo!")

while True:
    print("🔍 Tentando capturar ofertas agora...")
    posts = buscar_melhor_oferta()
    
    if posts:
        bot.send_message(CHAT_ID, "📢 **CONFIRA AS TENDÊNCIAS DE AGORA**")
        for p in posts:
            bot.send_message(CHAT_ID, p, parse_mode="Markdown")
            time.sleep(2)
        print(f"✅ Sucesso! {len(posts)} ofertas enviadas.")
    else:
        # Se falhou, avisa no log para a gente saber
        print("⚠️ Nenhuma oferta encontrada. Pode ser que o ML bloqueou ou mudou as classes.")
        bot.send_message(CHAT_ID, "⚠️ O robô tentou garimpar ofertas mas não encontrou nada nos códigos do site. Precisa de ajuste na mira!")
    
    print("⏳ Próxima tentativa em 6 horas...")
    time.sleep(21600)
