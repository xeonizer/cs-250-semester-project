import pickle
import os
import json
import nltk
import re


class Lexicon:
    """
    The lexicon is a dictionary of the form:
    lexicon = {
        cat: 1,
        dog: 2,
        snake: 3,
        .
        .
        .
    }
    """

    def __init__(self, path):
        """
        The constructor gets absolute path to pickle
        storing the dictionary of the lexicon
        """
        self.path = path
        self.lexicon = self.load_lexicon()

    def load_lexicon(self):
        """
        parameters: none
        This method is called by the constructor to
        load any existing dictionary pickle. If no such
        pickle exists create a new one.
        return: dictionary
        """
        lexicon = {}  # Empty Dictionary
        try:
            pickle_file = open(self.path, 'rb')
            lexicon = pickle.load(pickle_file)
            pickle_file.close()
        except IOError:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'wb') as file:
                pickle.dump(lexicon, file)
            file.close()

        return lexicon

    def generate_lexicon(self, doc_paths):
        """
        parameters:
        doc_paths - list of document paths from which
        to generate new lexicon.
        Store this lexicon at self.path. If a lexicon
        already exists there replace it.
        Use NLTK to tokenize and stem words and also
        remove stop words.
        https://www.nltk.org/
        return: void
        """
        lexicon = self.lexicon

        for path in doc_paths:
            with open(path) as json_file:
                document = json.load(json_file)  # reading json in document
            json_file.close()

            title_tokens = nltk.word_tokenize(document['title'])
            text_tokens = nltk.word_tokenize(document['text'])

            # Removing URLs, numbers and punctuations
            text_tokens = [re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in text_tokens]
            text_tokens = [re.sub(r'[^A-Za-z]+', '', x) for x in text_tokens]
            title_tokens = [re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in title_tokens]
            title_tokens = [re.sub(r'[^A-Za-z]+', '', x) for x in title_tokens]

            # Removing stop words
            stop_words = set(nltk.corpus.stopwords.words('english'))
            text_tokens = [x for x in text_tokens if not x in stop_words]
            title_tokens = [x for x in title_tokens if not x in stop_words]

            # Stemming words
            stemmer = nltk.stem.PorterStemmer()
            text_tokens = [stemmer.stem(x) for x in text_tokens]
            title_tokens = [stemmer.stem(x) for x in title_tokens]

            for x in title_tokens:
                if x is not '' and x not in lexicon:
                    lexicon[x] = len(lexicon) + 1

            for x in text_tokens:
                if x is not '' and x not in lexicon:
                    lexicon[x] = len(lexicon) + 1

        # Storing the lexicon
        with open(self.path, 'wb') as file:
            pickle.dump(lexicon, file)
        file.close()


    def get_lexicon_dict(self):
        """
        parameters: none
        return: dictionary
        """
        # Reading lexicon from pickle and returning it
        pickle_file = open(self.path, 'rb')
        lexicon = pickle.load(pickle_file)
        pickle_file.close()
        return lexicon

    def get_word_id(self, word):
        """
        parameters: word
        Search word in self.dictionary and return
        its wordID. If the word does not exist 
        return -1
        return: void
        """
        stemmer = nltk.stem.PorterStemmer()
        stemmed_word = stemmer.stem(word)
        try:
            id = self.lexicon[stemmed_word]
            return id
        except KeyError:
            return -1


    def __len__(self):
        """
        magic method
        return len of lexicon.
        """
        return len(self.lexicon)