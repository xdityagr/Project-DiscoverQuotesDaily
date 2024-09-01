# DiscoverQuotesDaily Bot

DiscoverQuotesDaily Bot is a Python-based bot that generates and posts inspirational quotes daily on Twitter. It can fetch quotes from various categories and generate visually appealing images featuring these quotes. The bot schedules daily posts and interacts with the Twitter API to share the generated images.

## Features

- **Daily Inspirational Quotes**: Automatically posts a new quote each day.
- **Customizable Quotes**: Fetches quotes based on various tags from the Quotable API.
- **Image Generation**: Creates images with quotes using the Pillow library.
- **Twitter Integration**: Posts images and quotes on Twitter using Tweepy.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/DiscoverQuoteBot.git
    cd DiscoverQuoteBot
    ```

2. **Install Dependencies**

    Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration**

    - **Quotes API**: No additional configuration required.
    - **Twitter API**: Create a `twitterCredentials.json` file in the root directory with the following structure:

      ```json
      {
          "api_key": "YOUR_API_KEY",
          "api_key_secret": "YOUR_API_KEY_SECRET",
          "access_token": "YOUR_ACCESS_TOKEN",
          "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
      }
      ```

4. **Run the Bot**

    Start the bot using:

    ```bash
    python discoverquotebot.py
    ```

## Code Overview

- **discoverquotebot.py**: Main script that runs the bot, schedules daily posts, and handles image generation and Twitter posting.
- **bot_utils.py**: Contains utility classes for interacting with the Quotable API, generating quote images, and posting to Twitter.

### `discoverquotebot.py`

The main function `daily_post_loop` fetches a quote, generates an image with the quote, saves it, and posts it to Twitter. The bot is scheduled to run this function daily.

### `bot_utils.py`

- **Quote**: Retrieves a random quote from the Quotable API and handles tag selection.
- **QuoteImageGenerator**: Generates images with quotes using the Pillow library, adjusting text wrapping and font size dynamically.
- **TwitterConnHandler**: Manages Twitter API connections and handles posting of tweets with images.

## Usage

- The bot runs continuously and posts a new quote daily.
- Modify `tags.json` to change the categories of quotes.
- Adjust image generation settings by editing the `QuoteImageGenerator` class.

## Contributing

If you want to contribute to DiscoverQuoteBot, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes and push them to your fork.
4. Open a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Quotable API for providing the quotes.
- Pillow library for image generation.
- Tweepy for Twitter API integration.

## Contact

For questions or feedback, please contact:

- **Email**: adityagaur.home@gmail.com
- **GitHub**: [xdityagr](https://github.com/xdityagr)
