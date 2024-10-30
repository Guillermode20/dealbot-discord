import os
import discord
import requests
import random
from discord.ext import commands
import aiohttp
import difflib
from fuzzywuzzy import process, fuzz

# Load the token from the token.txt file
with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()

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

# Define a command that listens for !sale
@bot.command()
async def sale(ctx, *, game_name: str):
    # Fetch deals for the specified game
    async with aiohttp.ClientSession() as session:
        async with session.get(deal_url, params={"title": game_name}) as response:
            deals = await response.json()
            # Find close matches for the game title
            titles = [deal['title'] for deal in deals]
            close_matches = process.extract(game_name, titles, limit=5, scorer=fuzz.ratio)
            
            # Check for a 100% match
            exact_matches = [match for match in close_matches if match[1] == 100]
            if exact_matches:
                best_match = exact_matches[0][0]
                deal = next(deal for deal in deals if deal['title'] == best_match)
                store_name = store_id_to_name.get(int(deal['storeID']), "Unknown Store")
                embed = discord.Embed(title=deal['title'], description=f"Sale Price: {deal['salePrice']}", color=0x00ff00)
                embed.add_field(name="Store", value=store_name, inline=True)
                embed.set_thumbnail(url=deal.get('thumb', ''))
                await ctx.send(embed=embed)
                return
            
            if close_matches:
                best_match = close_matches[0][0]
                # Check if there are multiple close matches with a high score
                high_score_matches = [match for match in close_matches if match[1] > 80]
                if len(high_score_matches) == 1:
                    # Send the deal for the closest match found
                    deal = next(deal for deal in deals if deal['title'] == best_match)
                    store_name = store_id_to_name.get(int(deal['storeID']), "Unknown Store")
                    embed = discord.Embed(title=deal['title'], description=f"Sale Price: {deal['salePrice']}", color=0x00ff00)
                    embed.add_field(name="Store", value=store_name, inline=True)
                    embed.set_thumbnail(url=deal.get('thumb', ''))
                    await ctx.send(embed=embed)
                else:
                    # Ask the user to specify the title
                    unique_titles = list(set([match[0] for match in close_matches]))
                    bullet_points = "\n".join([f"- {title}" for title in unique_titles])
                    embed = discord.Embed(title=f"Multiple deals found for {game_name}", description=f"Did you mean:\n{bullet_points}\nPlease specify the title.", color=0xff0000)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"No deals found for {game_name}", color=0xff0000)
                await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)