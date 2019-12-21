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
    def __init__(self, path, temp_path, lexicon_size, barrel_size):
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
        self.lexicon_size = lexicon_size
        self.barrel_size = barrel_size


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
            inverted_indexes = [{} for i in range(self.lexicon_size // self.barrel_size + 1)]

            for document in forward_index:
                for word_id in forward_index[document]:

                    # Find concerned barrel
                    barrel_index = word_id // self.barrel_size

                    # inverted_indexes[barrel_index][word_id][document] = forward_index[document][word_id]

                    if word_id in inverted_indexes[barrel_index]:
                        inverted_indexes[barrel_index][word_id][document] = forward_index[document][word_id]
                        # inverted_indexes[barrel_index][word_id].append({document: forward_index[document][word_id]})
                    else:
                        inverted_indexes[barrel_index][word_id] = { document: forward_index[document][word_id] }
                        # inverted_indexes[barrel_index][word_id] = [{document: forward_index[document][word_id]}]

            # Saving inverted index barrels which are not empty
            for i, inverted_index_barrel in enumerate(inverted_indexes):
                if not len(inverted_index_barrel) == 0:
                    filename = os.path.join(self.temp_path, f"{i:03}_inverted_{ntpath.basename(forward_index_path)}")
                    with open(filename, 'wb+') as inverted_index_file:
                        pickle.dump(inverted_index_barrel, inverted_index_file)

        return filename

    
    def merge_buckets(self):
        """
        Merge the temporary inverted indexes in self.temp_path with
        the inverted index in self.path and save them.

        This function expects to be called by the main thread.
        """
        temp_inverted_indexes = os.listdir(self.temp_path)

        for i in range(self.lexicon_size // self.barrel_size + 1):
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
                        # TODO: What if temp_index[word_id] i.e. that document and its hit list already exists?? 
                        if word_id in inverted_index:
                            inverted_index[word_id].update(temp_index[word_id])
                        else:
                            inverted_index[word_id] = temp_index[word_id]

                # Delete temp index
                os.remove(os.path.join(self.temp_path, concerned_index))
            
            # Save updated index
            with open (filename, 'wb') as inverted_index_file:
                pickle.dump(inverted_index, inverted_index_file)


    def retrieve(self, word_id):
        """
        parameters: word_id - Word id for which to return inverted_index

        return: list of documents and the hitlists for that word_id
        """

        # Find concerned barrel
        # TODO: What if barrel does not exist
        barrel_index = word_id // self.barrel_size
        filename = os.path.join(self.path, f"{barrel_index:03}_inverted")

        with open(filename, 'rb') as inverted_index_file:
            inverted_index = pickle.load(inverted_index_file)

            if word_id in inverted_index:
                return inverted_index[word_id]

        return None
