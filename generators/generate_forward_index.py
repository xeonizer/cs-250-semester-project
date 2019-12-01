import os
import pickle
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

	print('-'*32)

	PRINT_BARREL = 1
	PRINT_N = 2

	### DEMO PRINTING ###
	print("### DEMO TEST ###")
	print(f"{PRINT_N} entrie(s) from barrel {PRINT_BARREL}:")

	with open(os.path.join(config.FORWARD_INDEX_BARRELS_PATH, f"batch_00{PRINT_BARREL}"), 'rb') as forward_index_file:
		forward_index = pickle.load(forward_index_file)


		for i, doc_id in enumerate(forward_index):

			if i >= PRINT_N: break

			print(f"\t{doc_id}:")
			for word_id in forward_index[doc_id]:
				print(f"\t\t{word_id}: {forward_index[doc_id][word_id]}")

	print('-'*32)