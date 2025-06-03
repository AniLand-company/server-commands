
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f'{bot.user} успешно запущен!')
    print(f'ID бота: {bot.user.id}')
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} серверов"
        ),
        status=discord.Status.online
    )
    
    await load_extensions()
    
    try:
        synced = await bot.tree.sync()
        print(f'Синхронизировано {len(synced)} команд')
    except Exception as e:
        print(f'Ошибка синхронизации команд: {e}')

async def load_extensions():
    cogs = [
        'Путь к файлу',
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f'✅ Ког {cog} загружен')
        except Exception as e:
            print(f'❌ Ошибка загрузки кога {cog}: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав для выполнения этой команды!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Пожалуйста, укажите все необходимые аргументы!')
    else:
        print(f'Произошла ошибка: {error}')

if __name__ == '__main__':
    bot.run('BOT-TOKEN')
