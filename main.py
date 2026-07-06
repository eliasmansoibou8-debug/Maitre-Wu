import discord
from discord.ext import commands
import asyncio
import random
import json

from config import TOKEN, OWNER_ID, EMBED_COLOR

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

NEN_TYPES = {
    "💪 Enhancement": "You excel at strengthening your body and physical abilities.",
    "⚡ Emission": "You can project your aura over long distances.",
    "💎 Transmutation": "Your aura can imitate the properties of other substances.",
    "🎭 Conjuration": "You can materialize objects using your aura.",
    "🎮 Manipulation": "You can control living beings or objects with your aura.",
    "👁️ Specialization": "Your Nen is unique and extremely rare."
}


def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"{bot.user} is online!")
    print(f"{len(synced)} slash command(s) synced.")


@bot.tree.command(name="ping", description="Check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


@bot.tree.command(name="eveil", description="Awaken your Nen.")
async def eveil(interaction: discord.Interaction):

    data = load_data()
    user_id = str(interaction.user.id)

    if user_id in data:
        await interaction.response.send_message(
            "❌ You have already awakened your Nen.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "🌊 Awakening your Nen..."
    )

    await asyncio.sleep(2)

    nen = random.choices(
        population=list(NEN_TYPES.keys()),
        weights=[23, 20, 20, 18, 17, 2],
        k=1
    )[0]

    data[user_id] = {
        "nen": nen
    }

    save_data(data)

    embed = discord.Embed(
        title="✨ Nen Awakened ✨",
        description=f"**{nen}**\n\n{NEN_TYPES[nen]}",
        color=EMBED_COLOR
    )

    embed.set_footer(
        text="Your journey has just begun..."
    )

    await interaction.edit_original_response(
        content="",
        embed=embed
    )


@bot.tree.command(
    name="reseteveil",
    description="Reset a player's Nen awakening."
)
async def reseteveil(
    interaction: discord.Interaction,
    member: discord.Member
):

    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ You are not allowed to use this command.",
            ephemeral=True
        )
        return

    data = load_data()

    user_id = str(member.id)

    if user_id not in data:
        await interaction.response.send_message(
            "❌ This player has not awakened their Nen yet.",
            ephemeral=True
        )
        return

    del data[user_id]

    save_data(data)

    await interaction.response.send_message(
        f"✅ {member.display_name}'s Nen awakening has been reset."
    )


bot.run(TOKEN)
