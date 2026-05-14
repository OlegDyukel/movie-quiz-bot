from openai import OpenAI
import openai
from io import BytesIO
from PIL import Image
import requests
import logging
import base64

class OpenaiAPI:

    def __init__(self, **kwargs):
        self.client = OpenAI(api_key=kwargs.get('api_key'))
        self.model = kwargs.get('model', 'gpt-4o')
        self.temperature = kwargs.get('temperature', 0.65)
        self.max_tokens = kwargs.get('max_tokens', 1200)

    def generate_response(self, messages):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            content = response.choices[0].message.content.strip()
            logging.info(f"Generated answer: {content}")
            return content
        except openai.APIError as e:
            logging.error(f"An error occurred: {e}")
            return None

    def generate_image(self, prompt, model="gpt-image-2"):
        # https://github.com/openai/openai-python/blob/main/examples/picture.py
        try:
            img_resp = self.client.images.generate(prompt=prompt, model=model)
            data = img_resp.data[0]
            if getattr(data, "b64_json", None):
                image_bytes = base64.b64decode(data.b64_json)
                return Image.open(BytesIO(image_bytes))
            if getattr(data, "url", None):
                response = requests.get(data.url)
                return Image.open(BytesIO(response.content))
            logging.error("OpenAI generate_image: no image data in response")
            return None
        except openai.OpenAIError as e:
            logging.error(f"An error occurred: {e}")
            return None
