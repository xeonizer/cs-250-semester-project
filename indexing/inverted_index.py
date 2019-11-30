import pickle
import os
import ntpath


class InvertedIndex:
    """
    The inverted index is a set of dictionaries of the form:

    ii_dict_1 = {
        wordID1: [docID, docID, docID...]
        wordID2: [docID, docID, docID...]
        .
        .
        .
    }

    The InvertedIndex class handles the storage/inverted_index_barrels folder.
    In the storage/inverted_index_barrels/temp folder the new inverted indexes
    are added. There will be duplicates here as multiple threads will be adding
    inverted indexes here. So the files might look like:
        word_id_1_1000_1
        word_id_1_1000_2
        word_id_1_1000_3
        word_id_1001_2000_1
        word_id_1001_2000_2
        word_id_1001_2000_3
        .
        .
        .

    These will be merged and saved in the main folder where the files will 
    look like:
        word_id_1_1000
        word_id_1001_2000
        .
        .
        .

    """

    LEXICON_SIZE = 100 # TODO: get this value from Lexicon
    INVERTED_INDEX_BARREL_SIZE = 10 # DO NOT CHANGE THIS
    NUM_BARRELS = LEXICON_SIZE // INVERTED_INDEX_BARREL_SIZE


    def __init__(self, path, temp_path):
        """
        The initializer gets the absolute path to the direcotry
        which holds all the barrels for the inverted index.

        The initializer also gets the path to the temp folder where
        it stores inverted indexes when they are first created. This
        is done to cater for multi threaded execution which will lead
        to multiple files storing inverted index for the same range
        of wordIDs which need to be merged later.
        """
        self.path = path
        self.temp_path = temp_path


    def invert_forward_index(self, forward_index_path):
        """
        parameters: forward_index_path - The path to the forward index
        that needs to be inverted.

        Invert this forward index and store it in self.temp_path. If a bucket
        already exists there don't over write it.

        return: void

        This method expects to be called by multiple threads.
        """
        with open(forward_index_path, 'rb') as forward_index_file:
            forward_index = pickle.load(forward_index_file)
            inverted_indexes = [{} for i in range(self.LEXICON_SIZE // self.INVERTED_INDEX_BARREL_SIZE)]

            for document in forward_index:
                for word_id in forward_index[document]:

                    # Find concerned barrel
                    barrel_index = word_id // self.INVERTED_INDEX_BARREL_SIZE

                    if word_id in inverted_indexes[barrel_index]:
                        inverted_indexes[barrel_index][word_id].append(document)
                    else:
                        inverted_indexes[barrel_index][word_id] = [document]

            # Saving inverted index barrels which are not empty
            for i, inverted_index_barrel in enumerate(inverted_indexes):
                if not len(inverted_index_barrel) == 0:
                    filename = f"{i:03}_inverted_{ntpath.basename(forward_index_path)}"
                    with open(os.path.join(self.temp_path, filename), 'wb+') as inverted_index_file:
                        pickle.dump(inverted_index_barrel, inverted_index_file)

    
    def merge_buckets(self):
        """
        Merge the temporary inverted indexes in self.temp_path with
        the inverted index in self.path and save them.

        This function expects to be called by the main thread.
        """
        temp_inverted_indexes = os.listdir(self.temp_path)

        for i in range(self.NUM_BARRELS):
            concerned_indexes = [temp_index for temp_index in temp_inverted_indexes if temp_index.startswith(f"{i:03}_inverted_")]
            
            # If for i'th barrel no temp indexes exist continue
            if not len(concerned_indexes): continue

            # Open barrel
            filename = os.path.join(self.path, f"{i:03}_inverted")
            inverted_index = {}
            if os.path.exists(filename):
                with open(filename, 'rb') as inverted_index_file:
                    inverted_index = pickle.load(inverted_index_file)

            # For each temp index, append its content to main barrel
            for concerned_index in concerned_indexes:
                with open(os.path.join(self.temp_path, concerned_index), 'rb') as temp_index_file:
                    temp_index = pickle.load(temp_index_file)
                    for word_id in temp_index:
                        if word_id in inverted_index:
                            inverted_index[word_id] += temp_index[word_id]
                        else:
                            inverted_index[word_id] = temp_index[word_id]

                # Delete temp index
                os.remove(os.path.join(self.temp_path, concerned_index))
            
            # Save updated index
            with open (filename, 'wb') as inverted_index_file:
                pickle.dump(inverted_index, inverted_index_file)


