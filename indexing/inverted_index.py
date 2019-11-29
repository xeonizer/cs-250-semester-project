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




	"""

	def __init__(self, path, temp_path):
		"""
		The constructor gets the absolute path to the direcotry
		which holds all the barrels for the inverted index.

		The constructor also gets the path to the temp folder where
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
		pass

	
	@classmethod
	def merge_buckets(cls):
		"""
		Merge the temporary inverted indexes in self.temp_path and save
		them in self.path.

		This function expects to be called by the main thread.
		"""
		pass


