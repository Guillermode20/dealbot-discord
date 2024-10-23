import unittest
from unittest.mock import AsyncMock, MagicMock
from bot import quiz, bot


class TestDicordBot(unittest.TestCase):
    def setUp(self):
        self.bot = bot  # The bot instance
        self.message = MagicMock()  # Mock the message object
        self.message.author = "TestUser"  # Set the author of the message
        self.message.channel.send = AsyncMock()  # Mock the send method of the channel

    async def test_quiz_sends_question(self):  # Test the quiz function
        global questions
        questions = [
            {
                "Question": "What is 2+2?",
                "AnswerA": "3",
                "AnswerB": "4",
                "AnswerC": "5",
                "AnswerD": "6",
                "Correct AnswerA": "4",
            }
        ]

        await quiz(self.message)  # Call the quiz function with the message

        self.message.channel.send.assert_called_once()  # Ensure the send method was called
        sent_message = self.message.channel.send.call_args[0][0]  # Get the message sent

        self.assertIn(
            "What is 2+2?", sent_message
        )  # Ensure the question is in the message

    async def test_quiz_command_recognition(self):
        message = MagicMock()
        self.message.content = "!quiz"
        message.author = (
            MagicMock()
        )  # Mock the author object with MagicMock because it does not have any awaitable methods
        message.channel = (
            AsyncMock()
        )  # Mock the channel object with AsyncMock because it has an awaitable method

        await self.bot.on_message(message)

        message.channel.send.assert_called_once()  # Ensure the send method was called

    async def test_quiz_incorrect_answer(self):
        global questions
        questions = [
            {
                "Question": "What is 2+2?",
                "AnswerA": "3",
                "AnswerB": "4",
                "AnswerC": "5",
                "AnswerD": "6",
                "Correct AnswerA": "4",
            }
        ]

        await quiz(self.message)  # Call the quiz function with the message

        self.message.channel.send.assert_called_once()  # Ensure the send method was called
        sent_message = self.message.channel.send.call_args[0][0]  # Get the message sent

        self.assertIn(
            "What is 2+2?", sent_message
        )  # Ensure the question is in the message

        # Simulate an incorrect answer
        response = MagicMock()
        response.content = "3"
        response.author = self.message.author
        response.channel = self.message.channel

        await self.bot.wait_for(
            "message",
            check=lambda m: m.author == self.message.author
            and m.channel == self.message.channel,
        )
        self.message.channel.send.assert_called_with(
            "Incorrect! The correct answer was 4."
        )

    async def test_quiz_timeout(self):
        global questions
        questions = [
            {
                "Question": "What is 2+2?",
                "AnswerA": "3",
                "AnswerB": "4",
                "AnswerC": "5",
                "AnswerD": "6",
                "Correct AnswerA": "4",
            }
        ]

        await quiz(self.message)  # Call the quiz function with the message

        self.message.channel.send.assert_called_once()  # Ensure the send method was called
        sent_message = self.message.channel.send.call_args[0][0]  # Get the message sent

        self.assertIn(
            "What is 2+2?", sent_message
        )  # Ensure the question is in the message

        # Simulate a timeout
        with self.assertRaises(asyncio.TimeoutError):
            await self.bot.wait_for(
                "message",
                check=lambda m: m.author == self.message.author
                and m.channel == self.message.channel,
                timeout=0.1,
            )

        self.message.channel.send.assert_called_with(
            "Time's up! The correct answer was 4."
        )

    async def test_no_questions_available(self):
        global questions
        questions = []

        await quiz(self.message)  # Call the quiz function with the message

        self.message.channel.send.assert_called_once_with("No questions available.")
