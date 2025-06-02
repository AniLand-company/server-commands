import os
import disnake
from disnake.ext import commands

BOT_TOKEN = "TOKEN"

intents = disnake.Intents.default()
intents.messages = True
intents.members = True
intents.presences = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, status=disnake.Status.offline)
try:
    bot.load_extension("Путь к файлу")



except Exception as e:
    print(f"Ошибка при загрузке расширения': {e}")

bot.run(BOT_TOKEN)
