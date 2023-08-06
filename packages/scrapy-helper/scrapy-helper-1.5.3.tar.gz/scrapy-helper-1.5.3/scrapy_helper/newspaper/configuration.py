import logging

from .parsers import Parser
from .text import (StopWords, StopWordsArabic, StopWordsChinese,
                   StopWordsKorean, StopWordsHindi, StopWordsJapanese, StopWordsThai)

log = logging.getLogger(__name__)


class Configuration(object):
    def __init__(self):
        """
        Modify any of these Article / Source properties
        TODO: Have a separate ArticleConfig and SourceConfig extend this!
        """
        self.MAX_TITLE = 200  # num of chars
        self.MAX_TEXT = 100000  # num of chars
        self.MAX_AUTHORS = 10  # num strings in list

        # Don't toggle this variable, done internally
        self.use_meta_language = True

        # You may keep the html of just the main article body
        self.keep_article_html = True

        # English is the fallback
        self._language = 'zh'

        # Unique stopword classes for oriental languages, don't toggle
        self.stopwords_class = self.get_stopwords_class(self._language)

        self.verbose = False  # for debugging

    def get_language(self):
        return self._language

    def del_language(self):
        raise Exception('wtf are you doing?')

    def set_language(self, language):
        """Language setting must be set in this method b/c non-occidental
        (western) languages require a separate stopwords class.
        """
        if not language or len(language) != 2:
            raise Exception("Your input language must be a 2 char language code, \
                for example: english-->en \n and german-->de")

        # If explicitly set language, don't use meta
        self.use_meta_language = False

        # Set oriental language stopword class
        self._language = language
        self.stopwords_class = self.get_stopwords_class(language)

    language = property(get_language, set_language,
                        del_language, "language prop")

    @staticmethod
    def get_stopwords_class(language):
        if language == 'ko':
            return StopWordsKorean
        elif language == 'hi':
            return StopWordsHindi
        elif language == 'zh':
            return StopWordsChinese
        # Persian and Arabic Share an alphabet
        # There is a persian parser https://github.com/sobhe/hazm, but nltk is likely sufficient
        elif language == 'ar' or language == 'fa':
            return StopWordsArabic
        elif language == 'ja':
            return StopWordsJapanese
        elif language == 'th':
            return StopWordsThai
        return StopWords

    @staticmethod
    def get_parser():
        return Parser


class ArticleConfiguration(Configuration):
    pass
