from PyDeepLX import PyDeepLX
from .base import Translator
from .selenium_utils import create_proxy


class DeeplX(Translator):
    max_char = 3000

    def __init__(self, use_proxy=False):
        self.proxy = None
        if use_proxy:
            self._rotate_proxy()

    def _rotate_proxy(self):
        self.proxy = create_proxy()

    def _translate(self, text: str, source_language: str, destination_language: str):
        return PyDeepLX.translate(
            text,
            sourceLang=source_language.upper(),
            targetLang=destination_language.upper(),
            # proxies=self.proxy.httpProx,
            # proxies="socks5://68.1.210.163:4145",
        )

    def translate(self, text: str, source_language: str, destination_language: str):
        # try:
        return self._translate(text, source_language, destination_language)
        # except:
        #     if self.proxy is not None:
        #         self._rotate_proxy()

        #     return self._translate(text, source_language, destination_language)
