import os
import config
from indexing.inverted_index import InvertedIndex
from indexing.lexicon import Lexicon
import concurrent.futures


def main():
	lexicon = Lexicon(config.LEXICON_PATH)

	inverted_index = InvertedIndex(config.INVERTED_INDEX_BARRELS_PATH, config.INVERTED_INDEX_BARRELS_TEMP_PATH, len(lexicon), config.INVERTED_INDEX_BARREL_SIZE)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		batch_1_thread = executor.submit(inverted_index.invert_forward_index, os.path.join(config.FORWARD_INDEX_BARRELS_PATH, 'batch_001'))
		batch_2_thread = executor.submit(inverted_index.invert_forward_index, os.path.join(config.FORWARD_INDEX_BARRELS_PATH, 'batch_002'))

		for f in concurrent.futures.as_completed([batch_1_thread, batch_2_thread]):
			print(f"{f.result()} created.")

		inverted_index.merge_buckets()