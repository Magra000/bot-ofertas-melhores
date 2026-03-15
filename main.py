import requests
from bs4 import BeautifulSoup
import telebot
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"
bot = telebot.TeleBot(TOKEN)

URL_OFERTAS = "https://www.mercadolivre.com.br/ofertas"

def buscar_melhor_oferta():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(URL_OFERTAS, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Mira nos produtos da página de ofertas
        produtos = soup.find_all("div", {"class": "promotion-item__container"})[:5]
        
        if not produtos:
            produtos = soup.select(".poly-card__content")[:5]

        lista_posts = []
        for prod in produtos:
            try:
                nome_tag = prod.find("p", {"class": "promotion-item__title"}) or prod.select_one(".poly-component__title")
                nome = nome_tag.text.strip()
                
                link = prod.find("a")['href']
                
                preco_tag = prod.find("span", {"class": "promotion-item__price"}) or prod.select_one(".andes-money-amount__fraction")
                preco = preco_tag.text.strip()
                
                # Mudamos para HTML simples para evitar o erro de Markdown
                texto_post = (
                    f"<b>🛍️ OFERTA QUENTE NO MERCADO LIVRE</b>\n\n"
                    f"📦 {nome}\n"
                    f"💰 Por apenas: <b>R$ {preco}</b>\n\n"
                    f"🔗 Link: {link}\n\n"
                    f"🚀 <i>Sugestão do seu Bot de Ofertas</i>"
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
        # Usamos parse_mode='HTML' que é mais resistente a erros
        bot.send_message(CHAT_ID, "<b>📢 CONFIRA AS TENDÊNCIAS DE AGORA</b>", parse_mode='HTML')
        for p in posts:
            try:
                bot.send_message(CHAT_ID, p, parse_mode='HTML')
                time.sleep(2)
            except Exception as e:
                print(f"Erro ao mandar um post específico: {e}")
        print(f"✅ Sucesso! Ofertas processadas.")
    else:
        print("⚠️ Nenhuma oferta encontrada.")
    
    print("⏳ Próxima tentativa em 6 horas...")
    time.sleep(21600)
