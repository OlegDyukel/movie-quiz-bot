import json
import asyncio
import logging
import sys
from datetime import datetime
import random

from prompts import Picture
from openai_api import OpenaiAPI
from gemini_api import GeminiAPI
from config import Config
from tg_api import TelegramBot
from topics import Topic, Intro


LANGUAGES = ['english', 'spanish']

SCHEDULE = {'Monday': Topic.movies,
            'Tuesday': Topic.books,
            'Wednesday': Topic.tv_shows,
            'Thursday': Topic.songs,
            'Friday': Topic.movies,
            'Saturday': Topic.books,
            'Sunday': Topic.tv_shows}

N_options = 5

# Configure logging to use StreamHandler to direct logs to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def get_quiz() -> dict:
    dt = datetime.today()
    day_name = dt.strftime("%A")
    intro = Intro()
    topic = Topic()
    question = intro.pick_random(SCHEDULE[day_name])
    options = topic.pick_random(SCHEDULE[day_name])
    correct_id = random.randint(0, len(options))
    return {'question': question, 'options': options,
            'correct_id': correct_id, "correct_option": options[correct_id]}


def get_description(topic: str) -> str:
    return 'Titanic'


def generate_image(image_model, topic: str) -> dict:
    picture = Picture()
    picture_prompt = picture.get_picture_prompt(text=json.dumps(topic))
    image = image_model.generate_image(prompt=picture_prompt)
    return image


if __name__ == "__main__":
    openai = OpenaiAPI(api_key=Config.OPENAI_API_KEY, model='gpt-4o')
    gemini = GeminiAPI(api_key=Config.GEMINI_API_KEY, model='gemini-1.5-flash')
    bot = TelegramBot(token=Config.TG_TOKEN)

    #### TOPIC SELECTION AND A QUIZ QUESTION ASSEMBLING
    quiz = get_quiz()

    #### DESCRIPTION GENERATION
    description = get_description(quiz['correct_option'])

    #### PICTURE GENERATION
    images = generate_image(image_model=openai, topic=description)

    #### TG
    asyncio.run(bot.send_image_quizzes(chats=Config.CHANNEL_ID,
                                       questions=quiz,
                                       images=images))
