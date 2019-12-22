import os
import pickle
import config
from indexing.inverted_index import InvertedIndex
from indexing.lexicon import Lexicon
import concurrent.futures


def main(forward_index_batches, demo=False):
	lexicon = Lexicon(config.LEXICON_PATH)

	inverted_index = InvertedIndex(config.INVERTED_INDEX_BARRELS_PATH, config.INVERTED_INDEX_BARRELS_TEMP_PATH, len(lexicon), config.INVERTED_INDEX_BARREL_SIZE)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		threads = []
		for fib in forward_index_batches:
			thread = executor.submit(inverted_index.invert_forward_index, os.path.join(config.FORWARD_INDEX_BARRELS_PATH, fib))

		for f in concurrent.futures.as_completed(threads):
			print(f"{f.result()} created.")

	inverted_index.merge_buckets()


	if not demo: return

	### DEMO PRINTING ###

	print('-'*32)

	PRINT_BARREL = 3
	PRINT_N = 30

	print("### DEMO TEST ###")
	print(f"{PRINT_N} entries from barrel {PRINT_BARREL}:")

	with open(os.path.join(config.INVERTED_INDEX_BARRELS_PATH, f"{PRINT_BARREL:03}_inverted"), 'rb') as inverted_index_file:
		inverted_index = pickle.load(inverted_index_file)

		for i, word_id in enumerate(inverted_index):
			if i >= PRINT_N: break

			print(f"\t{word_id}:")

			for doc in inverted_index[word_id]:
				print(f"\t\t{doc}: {inverted_index[word_id][doc]}")