# Telegram ROM Build Bot 🤖

A Telegram bot to automate ROM build release posts. Built with `python-telegram-bot` and packaged for Docker.

## Features

- Step-by-step ROM post builder
- Markdown-formatted output
- Posts directly to a channel or group
- Only responds to authorized user (overlord mode)

## Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Jashkirat/auto-rom-post-bot
cd rom-bot
```

### 2. Create `.env`

```bash
cp .env.example .env
```

Edit `.env` and add your:
- Telegram Bot Token
- Channel or Group Chat ID

### 3. Build the Docker Image

```bash
docker build -t rom-bot .
```

### 4. Run the Bot

```bash
docker run -d --name rom-bot-container   --env-file .env   rom-bot
```

## Only You Can Use It 🛡

Set your Telegram user ID in `bot.py`:
```python
AUTHORIZED_USER_ID = 123456789  # Replace with your ID
```

You can get your ID from [@userinfobot](https://t.me/userinfobot)

## License

MIT
