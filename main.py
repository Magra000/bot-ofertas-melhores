import requests
from bs4 import BeautifulSoup
import telebot
import time

# --- CONFIGURAÇÃO ---
TOKEN = "8710482509:AAFIqDYVg00TZYJ5ydrLPzeVehXoPS28t_Q"
CHAT_ID = "982976668"
bot = telebot.TeleBot(TOKEN)

# Seus dados de afiliado extraídos do link que você enviou
MATT_TOOL = "42893323"
MATT_WORD = "pinterest"

URL_OFERTAS = "https://www.mercadolivre.com.br/ofertas"

def buscar_melhor_oferta():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(URL_OFERTAS, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        produtos = soup.find_all("div", {"class": "promotion-item__container"})[:5]
        if not produtos:
            produtos = soup.select(".poly-card__content")[:5]

        lista_posts = []
        for prod in produtos:
            try:
                nome_tag = prod.find("p", {"class": "promotion-item__title"}) or prod.select_one(".poly-component__title")
                nome = nome_tag.text.strip()
                
                # Link original do produto
                link_original = prod.find("a")['href']
                
                # Transformando em link de AFILIADO MENDESHOP
                # Limpamos o link de parâmetros antigos e colocamos os seus
                link_limpo = link_original.split('#')[0].split('?')[0]
                link_afiliado = f"{link_limpo}?matt_tool={MATT_TOOL}&matt_word={MATT_WORD}&forceInApp=true"
                
                preco_tag = prod.find("span", {"class": "promotion-item__price"}) or prod.select_one(".andes-money-amount__fraction")
                preco = preco_tag.text.strip()
                
                texto_post = (
                    f"<b>🛍️ OFERTA MAIS VENDIDA - MENDESHOP</b>\n\n"
                    f"📦 {nome}\n"
                    f"💰 Por apenas: <b>R$ {preco}</b>\n\n"
                    f"🛒 <b>COMPRE AQUI:</b> {link_afiliado}\n\n"
                    f"🚀 <i>Copie e poste no seu Status!</i>"
                )
                lista_posts.append(texto_post)
            except:
                continue
        return lista_posts
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return []

print("🚀 Bot de Afiliado MendeShop Ativo!")

while True:
    print("🔍 Gerando links de afiliado...")
    posts = buscar_melhor_oferta()
    
    if posts:
        bot.send_message(CHAT_ID, "<b>💰 NOVAS OFERTAS COM SEU LINK DE AFILIADO</b>", parse_mode='HTML')
        for p in posts:
            try:
                bot.send_message(CHAT_ID, p, parse_mode='HTML')
                time.sleep(2)
            except Exception as e:
                print(f"Erro ao mandar post: {e}")
        print(f"✅ Sucesso! Ofertas enviadas com link de afiliado.")
    else:
        print("⚠️ Nenhuma oferta encontrada.")
    
    print("⏳ Próxima garimpagem em 6 horas...")
    time.sleep(21600)
