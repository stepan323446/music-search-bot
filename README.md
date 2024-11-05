# Music Search Bot

This bot is designed to enhance the music sharing experience in chat platforms by automatically identifying music track links from popular streaming services and providing alternative links to the same track on different platforms.

* [Features](#features)
* [Technologies Used](#technologies-used)
* [Getting started](#getting-started)
* [Services](#services)
    * [Spotify](#spotify)
    * [Deezer](#deezer)
    * [Apple Music](#apple-music)
    * [Amazon Music](#amazon-music)
    * [Yandex Music](#yandex-music)
    * [Youtube Music](#youtube-music)


## Features

* **Link Detection:** The bot scans messages for links to music tracks, specifically targeting services like Apple Music.
* **Track Information Extraction:** It retrieves essential track information such as title, artist, and album from the detected link.
* **Alternative Links Search:** Using various music service APIs, the bot finds and provides links to the same track on other platforms (e.g., Deezer, Spotify).
* **User-Friendly Responses:** The bot replies with a neatly formatted message containing alternative links, making it easy for users to explore different streaming options.

## Technologies Used
* Python
* Python-telegram-bot
* APIs from various music streaming services (e.g., Apple Music, Deezer, Spotify)

## Getting Started

1. Clone the repository:

```shell
git clone https://github.com/stepan323446/music-search-bot.git

cd music-track-link-finder-bot
```

2. Create environment and install the required dependencies:
```shell
python3 -m venv .venv

# Activate venv

pip install -r requirements.txt
```

3. Create file `.env` and place Bot token
```env
BOT_TOKEN=<bot_token>
```

4. Place [your services](#services) that you will use in `config.py`
```py
SERVICES_ENABLED = (
    # Services
)
```

5. Run bot
```shell
python3 main.py
```

## Services

### Spotify

### Deezer

### Apple Music

### Amazon Music

### Yandex Music

> [!IMPORTANT]
> API avaible only on ru region

### Youtube Music