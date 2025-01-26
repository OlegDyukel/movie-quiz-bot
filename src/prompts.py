import datetime


PICTURE_STYLES = [
    'pixel art', 'vivid, lively', 'pixar/disney', 'realistic photography', 'anime/manga',
    'watercolor and traditional art', 'cyberpunk and futuristic aesthetics', 'surreal and abstract',
    'minimalistic and flat', 'fantasy and mythological']


class Picture:
    def __init__(self):
        super().__init__()
        self.day = datetime.datetime.today().day
        self.style_id = self.day % len(PICTURE_STYLES)
        self.style = PICTURE_STYLES[self.style_id]

    def get_picture_prompt(self, text: str) -> str:
        system_prompt = f"""
        You are an artist working at Pixar or Disney Studios.
        """
        prompt = f"""
            Please create a symbolic or thematic illustration that captures the essence of the text in 
            a {self.style} style. The text is {text}.
            The image shouldn't contain any words or letters. 
            If you aren't able to generate such an image because it did not align with the content policy 
            guidelines, please do a symbolic or thematic illustration that relates to {text}.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        return messages[0]['content'] + messages[1]['content']
