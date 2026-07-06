import discord
from discord.ext import commands
from discord import app_commands

from config import TOKEN

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commande(s) synchronisée(s).")
    except Exception as e:
        print(e)


@bot.tree.command(name="ping", description="Teste si le bot fonctionne.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")


bot.run(TOKEN)
