import datetime


class Prompt:
    def __init__(self):
        self.day = datetime.datetime.today().day
        self.picture_styles = [
            'pixel art', 'vivid, lively', 'pixar/disney', 'realistic photography', 'anime/manga',
            'watercolor and traditional art', 'cyberpunk and futuristic aesthetics', 'surreal and abstract',
            'minimalistic and flat', 'fantasy and mythological'
        ]
        self.style_id = self.day % len(self.picture_styles)
        self.style = self.picture_styles[self.style_id]

    def get_description_prompt(self, topic: str, art_item: str) -> list:
        system_prompt = f"""
        You are a very talent writer.
        """
        prompt = f"""
            Please write a text description of the {topic} {art_item}.
            Focus on abstract or symbolic representations of the themes and elements from the {art_item} story, 
            avoiding specific characters or identifiable references to copyrighted elements.
            Focus on Symbolism.
            Avoid Identifiable References: Steer clear of directly referencing the name {art_item} or its specific 
            characters. Instead, focus on universal ideas the story represents.
            Emphasize Environment and Emotion: Highlight the setting and the emotions the story conveys.
            The output should contain only the description. Please exclude other words, side notes, explanations or 
            introductions.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        return messages

    def get_picture_prompt(self, text: str) -> str:
        system_prompt = f"""
        You are an artist working at Pixar or Disney Studios.
        """
        prompt = f"""
            Please create a symbolic or thematic image/picture/illustration that captures the essence of the text in 
            a {self.style} style. The text is {text}.
            The image shouldn't contain any words or letters. 
            If you aren't able to generate such an image because it did not align with the content policy 
            guidelines, or  If it  is difficult to capture all of these elements in a single image,
            Please neglect some of the details and reflect environment and emotion. 
            Highlight the setting and the emotions the story convey.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        return messages[0]['content'] + messages[1]['content']
