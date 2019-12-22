import os
import pickle
import config
from indexing.forward_index import ForwardIndex
from indexing.lexicon import Lexicon
import concurrent.futures


def main(batch_start, batch_end, demo=False):

	lexicon = Lexicon(config.LEXICON_PATH)

	forward_index = ForwardIndex(config.FORWARD_INDEX_BARRELS_PATH, lexicon)

	with concurrent.futures.ThreadPoolExecutor() as executor:

		threads = []

		if batch_start == batch_end:
			batch_1_thread = executor.submit(forward_index.add_to_forward_index, config.dataset_files(batch_start, batch_start + 1), f"batch_00{batch_start}")
			threads.append(batch_1_thread)
		else:
			mid = int((batch_end + batch_start) / 2)
			batch_1_thread = executor.submit(forward_index.add_to_forward_index, config.dataset_files(batch_start, mid), f"batch_00{batch_start}")
			batch_2_thread = executor.submit(forward_index.add_to_forward_index, config.dataset_files(mid, batch_end), f"batch_00{mid}")
			threads.append(batch_1_thread)
			threads.append(batch_2_thread)

		for f in concurrent.futures.as_completed(threads):
			print(f"{f.result()} forward_index created.")

	if not demo: return
	
	### DEMO PRINTING ###

	print('-'*32)

	PRINT_BARREL = 0
	PRINT_N = 2

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