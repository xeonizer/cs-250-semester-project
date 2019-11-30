import config
from indexing.lexicon import Lexicon


def main():
    lexicon = Lexicon(config.LEXICON_PATH)

    lexicon.generate_lexicon(list(config.dataset_files(1)))
    # lexicon.update_lexicon(list(config.dataset_files()))
    # lexicon_dict = lexicon.get_lexicon_dict()
    # word_id = lexicon.get_word_id("inflation")
    # word_exists = lexicon.check_word_exists("blablabla")