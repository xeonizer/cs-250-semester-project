class ForwardIndex:
	"""
	The forward index is a set of dictionaries of the form:

	fi_dict_1 = {
		blog_0000001: wordID <HitList>,
		blog_0000001: wordID <HitList>,
		blog_0000001: wordID <HitList>,
		.
		.
		.
		blog_0000002: wordID <HitList>,
		blog_0000002: wordID <HitList>,
		blog_0000002: wordID <HitList>,
		.
		.
		.
	}

	The set of these dictionaries is stored in a directory
	as pickles of which the path is given to the constructor.

	"""

	def __init__(self, path, lexicon_dict):
		"""
		The constructor gets the absolute path to the directory 
		which holds all the pickles of the forward index.

		The constuctor also gets the lexicon dictionary which is
		used by methods inside it.
		"""
		self.path = path
		self.lexicon = lexicon


	def add_to_forward_index(self, doc_paths):
		"""
		parameters: doc_paths - list of document paths. These need
		to be parsed and their words need to be added to a new dictionary
		with the hit list.

		Everytime this method is called a new pickle file is added to
		the forward index directory

		return: void
		"""
		pass


	def get_forward_index_files(self):
		"""
		parameters: none
		return: Return the list of files(pickles) in forward index
		directors a.k.a the barrels
		"""
		pass


	def traverse_forward_index(self, path):
		"""
		parameters: path to the pickle
		GENERATOR FUNCTION - yeilds tuple of the form:
		("docID", "word", "<HitList>")
		"""
		pass