import requests
from bs4 import BeautifulSoup
import telebot
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"
bot = telebot.TeleBot(TOKEN)

URL_MAIS_VENDIDOS = "https://www.mercadolivre.com.br/mais-vendidos"

def buscar_melhor_oferta():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(URL_MAIS_VENDIDOS, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Pega os cards de produtos mais vendidos
        produtos = soup.select(".poly-card__content")[:5] 
        
        lista_posts = []
        for prod in produtos:
            try:
                nome = prod.select_one(".poly-component__title").text
                link = prod.select_one(".poly-component__title")['href']
                preco = prod.select_one(".andes-money-amount__fraction").text
                
                texto_post = (
                    f"🛍️ **OFERTA MAIS VENDIDA**\n\n"
                    f"📦 {nome}\n"
                    f"💰 Por apenas: **R$ {preco}**\n\n"
                    f"🔗 Link: {link}\n\n"
                    f"🚀 *Sugestão do seu Bot de Ofertas*"
                )
                lista_posts.append(texto_post)
            except:
                continue
        return lista_posts
    except:
        return []

print("🚀 Bot de Ofertas MendeShop Rodando!")

while True:
    posts = buscar_melhor_oferta()
    if posts:
        bot.send_message(CHAT_ID, "📢 **CONFIRA AS TENDÊNCIAS DE HOJE**")
        for p in posts:
            bot.send_message(CHAT_ID, p, parse_mode="Markdown")
            time.sleep(2)
    
    print("⏳ Aguardando 6 horas para a próxima atualização...")
    time.sleep(21600)
