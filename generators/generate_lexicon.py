import config
from indexing.lexicon import Lexicon


def main():
	lexicon = Lexicon(config.LEXICON_PATH)

	lexicon.generate_lexicon(config.dataset_files())

	print(f"Lexicon created with {len(lexicon)} words.")
	print('-'*32)

	PRINT_N = 10

	### DEMO PRINTING ###
	print("### DEMO TEST ###")
	print(f"{PRINT_N} words from the lexicon are: ")

	lexicon_dict = lexicon.get_lexicon_dict()

	for i, word in enumerate(lexicon_dict):
		if i >= PRINT_N: break
		print(f"\t{word}: {lexicon_dict[word]}")

	print('-'*32)