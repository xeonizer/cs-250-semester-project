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
		pass


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
		pass


	def update_lexicon(self, doc_paths):
		"""
		parameters:
		
		doc_paths - list of new documents added to
		system. 

		Append new words found in these
		documents to existing lexicon.

		return: void
		"""
		pass


	def get_lexicon_dict(self):
		"""
		parameters: none

		return: dictionary
		"""
		pass

		
	def get_word_id(self, word):
		"""
		parameters: word

		Search word in self.dictionary and return
		its wordID. If the word does not exist 
		return -1

		return: void
		"""
		pass


	def check_word_exists(self, word):
		"""
		parameters: word

		Search word in lexicon.

		return: boolean

		"""


	def __len__(self):
		"""
		magic method

		return len of lexicon.
		"""
		pass