# TODO: Write tests using python's unittest module


import config
from indexing.lexicon import Lexicon


def main():
	lexicon = Lexicon(config.LEXICON_PATH)

	lexicon.generate_lexicon(list(config.dataset_files(1)))
	lexicon.generate_lexicon(list(config.dataset_files()))
	lexicon_dict = lexicon.get_lexicon_dict()
	print(len(lexicon_dict))
	word_id = lexicon.get_word_id("Dear")
	print(word_id)
	word_exists = lexicon.get_word_id("blablabla")
	print(word_exists)
