import config
from indexing.lexicon import Lexicon


def main(batch_start, batch_end, demo=False):
	lexicon = Lexicon(config.LEXICON_PATH)

	lexicon.generate_lexicon(config.dataset_files(batch_start, batch_end))

	print(f"Lexicon created with {len(lexicon)} words.")
	print('-'*32)

	if not demo: return

	### DEMO PRINTING ### 

	PRINT_N = 10
	print("### DEMO TEST ###")
	print(f"{PRINT_N} words from the lexicon are: ")

	lexicon_dict = lexicon.get_lexicon_dict()

	for i, word in enumerate(lexicon_dict):
		if i >= PRINT_N: break
		print(f"\t{word}: {lexicon_dict[word]}")

	print('-'*32)