import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
import discord
import requests
import random
from discord.ext import commands, tasks  # Add tasks import
import aiohttp
import difflib
from fuzzywuzzy import process, fuzz
from discord.ui import Button, View
from dotenv import load_dotenv
import sqlite3

# Load the environment variables from the .env file
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

conn = sqlite3.connect('sale_reminders.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                (discord_username_id INTEGER, game_title TEXT, channel_id INTEGER)''')

# Define the store ID to name mapping
store_id_to_name = {
    1: "Steam",
    2: "GamersGate",
    3: "GreenManGaming",
    4: "Amazon",
    5: "GameStop",
    6: "Direct2Drive",
    7: "GOG",
    8: "Origin",
    9: "Get Games",
    10: "Shiny Loot",
    11: "Humble Store",
    12: "Desura",
    13: "Uplay",
    14: "IndieGameStand",
    15: "Fanatical",
    16: "Gamesrocket",
    17: "Games Republic",
    18: "SilaGames",
    19: "Playfield",
    20: "ImperialGames",
    21: "WinGameStore",
    22: "FunStockDigital",
    23: "GameBillet",
    24: "Voidu",
    25: "Epic Games Store",
    26: "Razer Game Store",
    27: "Gamesplanet",
    28: "Gamesload",
    29: "2Game",
    30: "IndieGala",
    31: "Blizzard Shop",
    32: "AllYouPlay",
    33: "DLGamer",
    34: "Noctre",
    35: "DreamGame"
}

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

deal_url = "https://www.cheapshark.com/api/1.0/deals"

@bot.command()
async def info(ctx):
    """Provide information about the bot."""
    embed = discord.Embed(title="Game Sale Bot", description="I am a cool bot made by big willy himself to help you find sales for games", color=0x00ff00)
    embed.add_field(name="!sale <game name>", value="Find deals for a specific game", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def sale(ctx, *, game_name: str):
    """Fetch and display deals for the specified game."""
    async with aiohttp.ClientSession() as session:
        async with session.get(deal_url, params={"title": game_name}) as response:
            deals = await response.json()
            await handle_deals(ctx, game_name, deals)

async def handle_deals(ctx, game_name, deals, discord_username_id=None):
    """Handle the deals fetched for the specified game."""
    titles = [deal['title'] for deal in deals]
    close_matches = process.extract(game_name, titles, limit=5, scorer=fuzz.ratio)

    exact_matches = [match for match in close_matches if match[1] == 100]
    if exact_matches:
        await send_deal(ctx, deals, exact_matches[0][0], discord_username_id)
        return

    high_score_matches = [match for match in close_matches if match[1] > 80]
    if len(high_score_matches) == 1:
        await send_deal(ctx, deals, high_score_matches[0][0], discord_username_id)
        return

    if close_matches:
        if isinstance(ctx, discord.TextChannel):
            # Skip sending multiple matches message for automated checks
            return
        await handle_close_matches(ctx, game_name, deals, close_matches)
    else:
        if isinstance(ctx, discord.TextChannel):
            # Skip sending no deals message for automated checks
            return
        await send_no_deals_found(ctx, game_name)

async def handle_close_matches(ctx, game_name, deals, close_matches):
    """Handle multiple close matches found."""
    unique_titles = list(set([match[0] for match in close_matches]))
    
    if len(unique_titles) == 1:  # If there's only one unique title, use it
        await send_deal(ctx, deals, unique_titles[0])
    else:
        bullet_points = "\n".join([f"- {title}" for title in unique_titles])
        embed = discord.Embed(title=f"Multiple deals found for {game_name}", 
                              description=f"Did you mean:\n{bullet_points}\nPlease specify the title.", 
                              color=0xff0000)
        await ctx.send(content=f"{ctx.author.mention}", embed=embed)

async def send_deal(ctx, deals, best_match, discord_username_id=None):
    """Send the deal for the closest match found."""
    deal = next(deal for deal in deals if deal['title'] == best_match)
    store_name = store_id_to_name.get(int(deal['storeID']), "Unknown Store")
    sale_price = float(deal['salePrice'])
    normal_price = float(deal['normalPrice'])
    discount_percentage = round(((normal_price - sale_price) / normal_price) * 100)

    embed = discord.Embed(title=deal['title'], description=f"Sale Price: ${sale_price:.2f}", color=0x00ff00)
    embed.add_field(name="Store", value=store_name, inline=True)
    embed.set_thumbnail(url=deal.get('thumb', ''))

    if discount_percentage == 0:
        embed.add_field(name="Discount", value="No discount available", inline=True)
        
        # Only show the button if it's a command context (not an automated check)
        if not isinstance(ctx, discord.TextChannel):
            button = Button(label="Add Sale Reminder", style=discord.ButtonStyle.primary)
            
            async def button_callback(interaction):
                cursor.execute('INSERT INTO reminders (discord_username_id, game_title, channel_id) VALUES (?, ?, ?)', 
                               (interaction.user.id, deal['title'], interaction.channel.id))
                conn.commit()
                await interaction.response.send_message(f"Sale reminder added for {deal['title']}", ephemeral=True)
                await interaction.message.edit(view=None)
            
            button.callback = button_callback
            view = View()
            view.add_item(button)
            mention = ctx.author.mention
            await ctx.send(content=mention, embed=embed, view=view)
        else:
            await ctx.send(embed=embed)
    else:
        embed.add_field(name="Discount", value=f"{discount_percentage}%", inline=True)
        if isinstance(ctx, discord.TextChannel):
            mention = f"<@{discord_username_id}>" if discord_username_id else ""
        else:
            mention = ctx.author.mention
        await ctx.send(content=mention, embed=embed)

async def send_no_deals_found(ctx, game_name):
    """Send a message indicating no deals were found."""
    embed = discord.Embed(title=f"No deals found for {game_name}", color=0xff0000)
    print(f"Sending no deals found message for {game_name}")

from types import SimpleNamespace

async def check_sale_reminders():
    """Check sale reminders and notify users if their games are on sale."""
    print("Checking sale reminders...")
    cursor.execute('SELECT discord_username_id, game_title, channel_id FROM reminders')
    reminders = cursor.fetchall()
    print(f"Fetched {len(reminders)} reminders from the database")

    async with aiohttp.ClientSession() as session:
        for reminder in reminders:
            discord_username_id, game_title, channel_id = reminder
            print(f"Checking deals for {game_title} for user {discord_username_id} in channel {channel_id}")
            async with session.get(deal_url, params={"title": game_title}) as response:
                deals = await response.json()
                if deals:
                    channel = bot.get_channel(channel_id)
                    if channel:
                        print(f"Channel {channel_id} found")
                        await channel.send(f"<@{discord_username_id}>, deal found for {game_title}:")
                        await handle_deals(channel, game_title, deals)  # Removed discord_username_id parameter
                    else:
                        print(f"Channel {channel_id} not found")
                else:
                    print(f"No deals found for {game_title}")


# Start the task loop when the bot is ready
@bot.event
async def on_ready():
    print("Bot is ready")
    # Assuming you have a task loop to call check_sale_reminders periodically
    bot.loop.create_task(check_sale_reminders())

# Run the bot
print("Running the bot...")
bot.run(TOKEN)