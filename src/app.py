import asyncio
import logging
import sys
from datetime import datetime
import random

from prompts import Prompt
from openai_api import OpenaiAPI
# from gemini_api import GeminiAPI
from config import Config, Parameter
from tg_api import TelegramBot
from topics import Topic, Intro


# Configure logging to use StreamHandler to direct logs to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def get_quiz() -> dict:
    intro = Intro()
    topic = Topic()
    params = Parameter()
    dt = datetime.today()
    day_name = dt.strftime("%A")
    question = intro.pick_random(params.SCHEDULE[day_name])
    options = topic.pick_random(params.SCHEDULE[day_name], n_options=params.N_options)
    correct_id = random.randint(0, len(options))
    explanation = intro.get_explanation()
    return {'topic': params.SCHEDULE[day_name], 'question': question, 'options': options,
            'correct_option_id': correct_id, "correct_option": options[correct_id], 'explanation': explanation}


def get_description(model, topic: str, art_item: str) -> str:
    ### GET PROMPT
    prompt = Prompt()
    description_prompt = prompt.get_description_prompt(topic, art_item)
    ### REQUEST A DESCRIPTION / PROMPT FOR AN IMAGE
    description = model.generate_response(messages=description_prompt)
    return description


def generate_image(image_model, description: str) -> dict:
    picture = Prompt()
    picture_prompt = picture.get_picture_prompt(text=description)
    image = image_model.generate_image(prompt=picture_prompt)
    return image


if __name__ == "__main__":
    openai = OpenaiAPI(api_key=Config.OPENAI_API_KEY, model='gpt-4o')
    # gemini = GeminiAPI(api_key=Config.GEMINI_API_KEY, model='gemini-1.5-flash')
    bot = TelegramBot(token=Config.TG_TOKEN)

    #### TOPIC SELECTION AND A QUIZ QUESTION ASSEMBLING
    quiz = get_quiz()

    #### DESCRIPTION GENERATION
    description = get_description(model=openai, topic=quiz['topic'], art_item=quiz['correct_option'])

    #### PICTURE GENERATION
    images = generate_image(image_model=openai, description=description)

    #### TG
    asyncio.run(bot.send_image_quizzes(chat=Config.CHANNEL_ID,
                                       quiz=quiz,
                                       image=images))
