import os


PROJECT_PATH = os.getcwd()

DATASET_PATH = os.path.join(PROJECT_PATH, "dataset")

STORAGE_PATH = os.path.join(PROJECT_PATH, "storage")
LEXICON_PATH = os.path.join(PROJECT_PATH, "storage/lexicon/lexicon")
FORWARD_INDEX_BARRELS_PATH = os.path.join(PROJECT_PATH, "storage/forward_index_barrels")
INVERTED_INDEX_BARRELS_TEMP_PATH = os.path.join(PROJECT_PATH, "storage/inverted_index_barrels/temp")
INVERTED_INDEX_BARRELS_PATH = os.path.join(PROJECT_PATH, "storage/inverted_index_barrels")


def dataset_files(batches_start=None, batches_end=None):
    for batch in os.listdir(DATASET_PATH)[batches_start:batches_end]:
        for file_path in os.listdir(os.path.join(DATASET_PATH, batch)):
            yield os.path.join(DATASET_PATH, batch, file_path)
