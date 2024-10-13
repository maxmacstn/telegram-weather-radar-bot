
# TMD Radar Telegram Bot
Simple Python script to check the Thai Meteorological Department weather radar image. If the radar image contains cloud area more than a certain threshold, send a notification message and a radar image via Telegram bot.

![header](https://raw.githubusercontent.com/maxmacstn/telegram-weather-radar-bot/refs/heads/main/banner.jpg)

## Pre-requisites
1. Python 3 with packages in `requirements.txt` installed.
2. Your Telegram `BOT_TOKEN` and `CHAT_ID` added into `credentials.py` file.

## Running the bot
Run continuously on your computer/server using `nohop` command.

```
nohup python3 radar_bot.py &
```

