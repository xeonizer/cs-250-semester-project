import config
from indexing.lexicon import Lexicon


def main():
	lexicon = Lexicon(config.LEXICON_PATH)

	lexicon.generate_lexicon(config.dataset_files())

	print(f"Lexicon created with {len(lexicon)} words.")