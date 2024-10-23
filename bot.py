import csv
import random
import discord
import os
import logging
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")

# Updated intents configuration
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.messages = True  # Ensure the bot can read messages
intents.guild_messages = True  # Enable guild (server) messages
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

# Read questions from CSV file
questions = []
try:
    with open("questions.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Strip keys to remove any leading/trailing spaces
            stripped_row = {
                key.strip(): value.strip() for key, value in row.items()
            }  # Strip values too
            questions.append(stripped_row)
    logging.info("Questions loaded successfully from questions.csv")
except Exception as e:
    logging.error(f"Failed to load questions: {e}")


# Event that runs when the bot has connected to Discord
@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")


# Store the correct answer globally
current_question = None
current_correct_answer = None


async def quiz(message):
    global current_question, current_correct_answer

    if questions:
        current_question = random.choice(questions)
        current_correct_answer = current_question["Correct AnswerA"].strip().lower()

        question_text = f"**{current_question['Question']}**\n"
        question_text += f"- {current_question['AnswerA']}\n"
        question_text += f"- {current_question['AnswerB']}\n"
        question_text += f"- {current_question['AnswerC']}\n"
        question_text += f"- {current_question['AnswerD']}\n"
        await message.channel.send(question_text)
        logging.info(f"Sent question: {current_question['Question']}")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            response = await bot.wait_for("message", check=check, timeout=30.0)
            if response.content.strip().lower() == current_correct_answer:
                await message.channel.send("Correct!")
                logging.info(f"User {response.author} answered correctly")
            else:
                await message.channel.send(
                    f"Incorrect! The correct answer was {current_correct_answer.capitalize()}."
                )
                logging.info(f"User {response.author} answered incorrectly")
        except asyncio.TimeoutError:
            await message.channel.send(
                f"Time's up! The correct answer was {current_correct_answer.capitalize()}."
            )
            logging.info("User did not respond in time")
    else:
        await message.channel.send("No questions available.")
        logging.warning("No questions available to send")


# Event that checks for messages and responds if they say "!quiz"
@bot.event
async def on_message(message):
    # Ensure the bot does not reply to itself
    if message.author == bot.user:
        return

    # Check if the message is "!quiz"
    if message.content.lower() == "!quiz":
        await quiz(message)
        logging.info(f"Received quiz command from {message.author}")

    # This is needed to allow commands to run
    await bot.process_commands(message)


# Run the bot with your token
try:
    bot.run(TMDB_API_TOKEN)  # Make sure to replace this with your actual bot token
except Exception as e:
    logging.error(f"Failed to run the bot: {e}")
