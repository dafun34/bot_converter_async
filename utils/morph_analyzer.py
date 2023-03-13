"""Модуль морфологического анализатора."""
import pymorphy2
from pymorphy2 import MorphAnalyzer
from pymorphy2.shapes import restore_capitalization


class MorphSingleton:
    """Синглтон pymorhy2."""

    _instance: pymorphy2.MorphAnalyzer = None

    def __new__(cls, *args: tuple, **kwargs: dict) -> MorphAnalyzer:
        """Создание нового экземпляра класса."""
        if not cls._instance:
            cls._instance = pymorphy2.MorphAnalyzer()
        return cls._instance


class MorphParser:
    """Класс - парсер для работы со словами и их формами."""

    morph = MorphSingleton()

    def normalize_phrase(self, phrase: str) -> str:
        """Привести фразу к нормальной форме с сохранением рода."""
        normalized = []
        for word in phrase.split():
            gender = str(self.morph.parse(word)[0].tag.gender)
            word = self.morph.parse(word)[0].normalized.inflect({gender}).word
            normalized.append(word)

        return " ".join(normalized)

    def change_case(self, currency_name: str) -> str:
        """Поменять фразу на нужный падеж."""
        changed = []
        case = "gent"
        for word in currency_name.split():
            parsed_word = self.morph.parse(word)[0]
            gent_case_word = parsed_word.inflect({case})
            restored_word = restore_capitalization(gent_case_word.word, word)
            changed.append(restored_word)
        return " ".join(changed)
