# TODO: Write tests using python's unittest module


import os
import config
from indexing.forward_index import ForwardIndex
from indexing.lexicon import Lexicon

# THESE TESTS CAN ONLY RUN AFTER LEXICON HAS BEEN IMPLEMENTED

def main():
    lexicon = Lexicon(config.LEXICON_PATH)
    forward_index = ForwardIndex(config.FORWARD_INDEX_BARRELS_PATH, lexicon)
    
    forward_index.add_to_forward_index(list(config.dataset_files(0,1)), 'aftab_test_forward_1')
    # forward_index.add_to_forward_index(list(config.dataset_files(1,2)))

    # forward_index_files = forward_index.get_forward_index_files()
    # for file in forward_index_files:
    #   for fi_entry in forward_index.traverse_forward_index(os.path.join(FORWARD_INDEX_BARRELS_PATH, file)):
    #       print(fi_entry)