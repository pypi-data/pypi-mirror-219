user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

class device:
    def __init__(self, user_agent: str = user_agent):
        self.user_agent = user_agent