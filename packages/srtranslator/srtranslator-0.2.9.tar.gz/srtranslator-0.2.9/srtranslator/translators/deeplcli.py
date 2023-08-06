from deepl import DeepLCLI
from .base import Translator


class DeeplCli(Translator):
    max_char = 3000

    def translate(self, text: str, source_language: str, destination_language: str):
        deepl = DeepLCLI(source_language, destination_language)
        return deepl.translate(text)
