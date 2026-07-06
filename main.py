import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import json

from config import TOKEN

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

types_nen = {
    "💪 Renforcement": "Vous excellez dans le renforcement de votre corps et de vos capacités physiques.",
    "⚡ Émission": "Vous pouvez projeter votre aura à distance.",
    "💎 Transmutation": "Votre aura peut reproduire les propriétés d'autres matières.",
    "🎭 Matérialisation": "Vous pouvez matérialiser des objets grâce à votre Nen.",
    "🎮 Manipulation": "Vous pouvez contrôler des êtres vivants ou des objets.",
    "👁️ Spécialisation": "Votre Nen est unique et extrêmement rare."
}


def charger_donnees():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def sauvegarder_donnees(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"{bot.user} est connecté !")
    print(f"{len(synced)} commande(s) synchronisée(s).")


@bot.tree.command(name="ping", description="Vérifie si le bot fonctionne")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong !")


@bot.tree.command(name="eveil", description="Éveille votre Nen")
async def eveil(interaction: discord.Interaction):

    data = charger_donnees()
    user_id = str(interaction.user.id)

    if user_id in data:
        await interaction.response.send_message(
            "❌ Vous avez déjà éveillé votre Nen.",
            ephemeral=True
        )
        return

    await interaction.response.send_message("🌊 Début de l'éveil du Nen...")

    await asyncio.sleep(2)

    nen = random.choices(
        population=[
            "💪 Renforcement",
            "⚡ Émission",
            "💎 Transmutation",
            "🎭 Matérialisation",
            "🎮 Manipulation",
            "👁️ Spécialisation"
        ],
        weights=[23, 20, 20, 18, 17, 2],
        k=1
    )[0]

    data[user_id] = {
        "nen": nen
    }

    sauvegarder_donnees(data)

    embed = discord.Embed(
        title="✨ Éveil du Nen ✨",
        description=f"Votre catégorie est **{nen}**\n\n{types_nen[nen]}",
        color=0x6B46C1
    )

    embed.set_footer(
        text="Le véritable entraînement commence maintenant..."
    )

    await interaction.edit_original_response(
        content="",
        embed=embed
    )


bot.run(TOKEN)

bot.run(TOKEN)
