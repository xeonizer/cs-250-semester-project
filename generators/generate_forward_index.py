import config
from indexing.forward_index import ForwardIndex
from indexing.lexicon import Lexicon
import concurrent.futures


def main():

	lexicon_dict = Lexicon(config.LEXICON_PATH).get_lexicon_dict()

	forward_index = ForwardIndex(config.FORWARD_INDEX_BARRELS_PATH, lexicon_dict)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		batch_1_thread = executor.submit(forward_index.add_to_forward_index, config.dataset_files(0,1), 'batch_001')
		batch_2_thread = executor.submit(forward_index.add_to_forward_index, config.dataset_files(1,2), 'batch_002')

		for f in concurrent.futures.as_completed([batch_1_thread, batch_2_thread]):
			print(f"{f.result()} forward_index created.")

