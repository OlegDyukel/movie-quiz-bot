import os


class Config:
    SECRET_KEY = os.urandom(44)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TG_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    LOG_CHANNEL_ID = {'log': os.getenv('LOG_CHANNEL_ID')}
    CHANNEL_ID = {'book_film_song': os.getenv('book_CHANNEL_ID')}
