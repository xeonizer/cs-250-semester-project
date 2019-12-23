import json
import ntpath
import os
import nltk
import re
import pickle
from tqdm import tqdm

class ForwardIndex:
    """
    The forward index is a set of dictionaries of the form:

    fi_dict_1 = {
        blog_0000001: [wordID <HitList>, wordID <HitList>, wordID <HitList>]
        blog_0000002: [wordID <HitList>, wordID <HitList>, wordID <HitList>]
        blog_0000003: [wordID <HitList>, wordID <HitList>, wordID <HitList>]
        .
        .
        .
    }

    The set of these dictionaries is stored in a directory
    as pickles of which the path is given to the initializer.

    """

    stop_words = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.stem.PorterStemmer()

    def __init__(self, path, lexicon):
        """
        The initializer gets the absolute path to the directory 
        which holds all the pickles of the forward index.

        The initializer also gets the lexicon dictionary which is
        used by methods inside it.
        """
        self.path = path
        self.lexicon = lexicon


    def add_to_forward_index(self, doc_paths, file_name):
        """
        parameters: doc_paths - list of document paths. These need
        to be parsed and their words need to be added to a new dictionary
        with the hit list.

        Everytime this method is called a new pickle file is added to
        the forward index directory

        return: void
        """
        fi_dict = {}
        for path in tqdm(doc_paths):
            with open(path, encoding="utf8") as json_file:
                document = json.load(json_file)  # reading json in document

            # Extracting doc_id
            document_id = os.path.splitext(ntpath.basename(path))[0]

            text_tokens = nltk.word_tokenize(document['text'])
            title_tokens = nltk.word_tokenize(document['title'])
            text_tokens += title_tokens

            # Removing URLs, numbers and punctuations
            text_tokens = [re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in text_tokens]
            text_tokens = [re.sub(r'[^A-Za-z]+', '', x) for x in text_tokens]


            # Removing stop words
            text_tokens = [x for x in text_tokens if not x in self.stop_words]


            # Stemming words
            text_tokens = [self.stemmer.stem(x) for x in text_tokens]


            word_id = {}

            # Getting word_id and appearances
            position = 1
            for word in text_tokens:
                if word != '' and self.lexicon.exists(word):
                    key = self.lexicon.get_word_id(word)
                    if key in word_id:
                        word_id[key].append(position)
                    else:
                        word_id[key] = [position]
                    position = position + 1

            # TODO: Assign a better document id
            fi_dict[document_id] = word_id

        # Saving the forward_index barrel as pickle
        pickle_path = os.path.join(self.path, file_name)
        with open(pickle_path, 'wb') as file:
            pickle.dump(fi_dict, file)

        return pickle_path