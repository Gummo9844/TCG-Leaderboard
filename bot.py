import requests
import telebot
import re
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_DO_BOT = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(CHAVE_DO_BOT)

@bot.message_handler(commands=['start'])
def boas_vindas(mensagem):
    bot.reply_to(mensagem, "Seja bem-vindo a Liga Pokémon.\nComo posso ajudar?")

@bot.message_handler(commands=['help'])
def help(mensagem):
    bot.reply_to(mensagem, "Para registrar o resultado de uma partida, use o formato:\n\n<nome_do_vencedor> ganhou e <nome_do_perdedor> perdeu\n\nExemplo:\nGummo ganhou e Rafa perdeu")

@bot.message_handler(func=lambda mensagem: 'ganhou' in mensagem.text.lower() and 'perdeu' in mensagem.text.lower())
def registrar_partida(mensagem):
    texto = mensagem.text
    padrao = r'(.+?) ganhou e (.+?) perdeu*'

    match = re.search(padrao, texto, re.IGNORECASE)
    vencedor = match.group(1).strip()
    perdedor = match.group(2).strip()

    requests.get(f'tcg-leaderboard-production.up.railway.app/update?winner={vencedor}&loser={perdedor}')

    bot.reply_to(mensagem, f"Anotado! 🏆\n Vencedor: {vencedor} | 💀 Perdedor: {perdedor}")

print("It's alive!")
bot.infinity_polling()