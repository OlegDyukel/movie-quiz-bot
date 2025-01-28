import os


class Config:
    SECRET_KEY = os.urandom(44)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TG_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    LOG_CHANNEL_ID = {'log': os.getenv('LOG_CHANNEL_ID')}
    CHANNEL_ID = os.getenv('BOOK_CHANNEL_ID')


class Parameter:
    N_options = 5
    SCHEDULE = {'Monday': 'movie',
                'Tuesday': 'book',
                'Wednesday': 'tv_show',
                'Thursday': 'song',
                'Friday': 'movie',
                'Saturday': 'book',
                'Sunday': 'tv_show'}
