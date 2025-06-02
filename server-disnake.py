import disnake
from disnake.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="server", description="👑 | Показать информацию о сервере")
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild
        
        if not guild:
            await inter.response.send_message("Команда доступна только на сервере!", ephemeral=True)
            return
        
        total_members = guild.member_count
        bot_count = sum(1 for member in guild.members if member.bot)
        human_count = total_members - bot_count
        
        online = sum(1 for member in guild.members if member.status == disnake.Status.online)
        idle = sum(1 for member in guild.members if member.status == disnake.Status.idle)
        dnd = sum(1 for member in guild.members if member.status == disnake.Status.dnd)
        offline = sum(1 for member in guild.members if member.status == disnake.Status.offline)
        
        news_channels = len([c for c in guild.text_channels if c.type == disnake.ChannelType.news])
        text_channels = len([c for c in guild.text_channels if c.type != disnake.ChannelType.news])
        voice_channels = len([c for c in guild.channels if isinstance(c, disnake.VoiceChannel)])
        stage_channels = len([c for c in guild.channels if isinstance(c, disnake.StageChannel)])
        forum_channels = len([c for c in guild.channels if isinstance(c, disnake.ForumChannel)])
        total_channels = text_channels + voice_channels + forum_channels + news_channels + stage_channels
        
        if guild.verification_level == disnake.VerificationLevel.none:
            verification_level = "Отсутствует"
        elif guild.verification_level == disnake.VerificationLevel.low:
            verification_level = "Низкий"
        elif guild.verification_level == disnake.VerificationLevel.medium:
            verification_level = "Средний"
        elif guild.verification_level == disnake.VerificationLevel.high:
            verification_level = "Высокий"
        elif guild.verification_level == disnake.VerificationLevel.highest:
            verification_level = "Максимальный"
        else:
            verification_level = "Неизвестно"
        
        embed = disnake.Embed(
            title=f"Информация о сервере **{guild.name}**",
            color=0x2B2D31
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        
        embed.add_field(
            name="Участники:",
            value=f"Всего: **{total_members}**\n"
                  f"Людей: **{human_count}**\n"
                  f"Ботов: **{bot_count}**",
            inline=True
        )
        
        status_lines = []
        if online > 0:
            status_lines.append(f"В сети: **{online}**")
        if idle > 0:
            status_lines.append(f"Неактивен: **{idle}**")
        if dnd > 0:
            status_lines.append(f"Не беспокоить: **{dnd}**")
        if offline > 0:
            status_lines.append(f"Не в сети: **{offline}**")
        
        if status_lines:
            embed.add_field(
                name="По статусам:",
                value="\n".join(status_lines),
                inline=True
            )
        
        channel_lines = [f"Всего: **{total_channels}**"]
        if text_channels > 0:
            channel_lines.append(f"Текстовых: **{text_channels}**")
        if news_channels > 0:
            channel_lines.append(f"Объявления: **{news_channels}**")
        if forum_channels > 0:
            channel_lines.append(f"Форумов: **{forum_channels}**")
        if voice_channels > 0:
            channel_lines.append(f"Голосовых: **{voice_channels}**")
        if stage_channels > 0:
            channel_lines.append(f"Трибун: **{stage_channels}**")
        
        embed.add_field(
            name="Каналы:",
            value="\n".join(channel_lines),
            inline=True
        )
        
        embed.add_field(
            name="Владелец:",
            value=guild.owner.display_name.replace("_", "\\_") if guild.owner else "Неизвестно",
            inline=True
        )
        
        embed.add_field(
            name="Уровень проверки:",
            value=verification_level,
            inline=True
        )
        
        created_timestamp = int(guild.created_at.timestamp())
        embed.add_field(
            name="Дата создания:",
            value=f"<t:{created_timestamp}:D>\n<t:{created_timestamp}:R>",
            inline=True
        )
        
        await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(ServerInfo(bot))
