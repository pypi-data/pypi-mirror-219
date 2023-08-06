from .device import device

sid = None

class Headers:
    def __init__(self, user_agent: str = None):

        if user_agent:
            dev = device(user_agent)
        else:
            dev = device()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://my.tiu.edu.iq/",
            "User-Agent": dev.user_agent,
            }

        if sid: headers["Cookie"] = f"PHPSESSID={sid}"
        self.headers = headers
