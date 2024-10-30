# 🎮 Game Sale Bot

Game Sale Bot is a Discord bot designed to help users find the best deals on video games from various online stores. The bot fetches and displays deals for specified games, providing users with the latest discounts and offers.

## ✨ Features

- 🛒 Fetch and display deals for specified games.
- 🔍 Handle multiple close matches and prompt users to specify the title.
- 📊 Display detailed information about the best match found.
- 🚫 Notify users when no deals are found for a specified game.
- ℹ️ Provide information about the bot and its commands.
- 🔔 Check sale reminders and notify users if their games are on sale.

## 📋 Commands

- `!sale <game name>`: Fetch and display deals for the specified game.
- `!info`: Provide information about the bot.

## 🚀 Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `token.txt` file in the root directory and add your Discord bot token to it.
4. Run the bot:
    ```sh
    python bot.py
    ```

## 🧪 Running Tests

To run the tests, use the following command:
```sh
python -m unittest discover
```

## 🛠️ Built With

- [discord.py](https://github.com/Rapptz/discord.py) - Python wrapper for the Discord API
- [aiohttp](https://github.com/aio-libs/aiohttp) - Asynchronous HTTP client/server framework
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) - Fuzzy string matching in Python

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Visit my [Website](will-hick-cv.click) for contacts and my other works.

## 🙏 Acknowledgments

- Thanks to [CheapShark](https://www.cheapshark.com/) for providing the API for game deals.
- Inspiration and guidance from the Discord.py community.