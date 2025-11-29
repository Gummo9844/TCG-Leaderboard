import requests
import telebot
import re
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_DO_BOT = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(CHAVE_DO_BOT)

@bot.message_handler(func=lambda mensagem: 'olá' in mensagem.text.lower())
def boas_vindas(mensagem):
    bot.reply_to(mensagem, "Seja bem-vindo a Liga Pokémon.\nComo posso ajudar?")

@bot.message_handler(func=lambda mensagem: 'ganhou' in mensagem.text.lower() and 'perdeu' in mensagem.text.lower())
def registrar_partida(mensagem):
    texto = mensagem.text
    padrao = r'(.+?) ganhou e (.+?) perdeu*'

    match = re.search(padrao, texto, re.IGNORECASE)
    vencedor = match.group(1).strip()
    perdedor = match.group(2).strip()

    

    bot.reply_to(mensagem, f"Anotado! 🏆\n Vencedor: {vencedor} | 💀 Perdedor: {perdedor}")

print("It's alive!")
bot.infinity_polling()