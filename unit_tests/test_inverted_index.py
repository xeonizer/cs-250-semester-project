import unittest
import os
import pickle
import config
from indexing.inverted_index import InvertedIndex
from indexing.lexicon import Lexicon


class TestInverteIndex(unittest.TestCase):

	def setUp(self):
		self.inverted_index = InvertedIndex(config.INVERTED_INDEX_BARRELS_PATH, config.INVERTED_INDEX_BARRELS_TEMP_PATH)

		test_forward_index_1 = {
			"blog_0000001": [1, 47, 32, 18],
			"blog_0000002": [47, 18, 4, 79],
			"blog_0000003": [47, 18, 92, 3],
			"blog_0000004": [52, 9, 32, 47],
		}

		test_forward_index_2 = {
			"blog_0000005": [2, 74, 23, 18],
			"blog_0000006": [47, 8, 41, 79],
			"blog_0000007": [4, 18, 92, 32],
			"blog_0000008": [52, 9, 32, 47],
		}
		
		self.test_forward_index_path_1 = os.path.join(config.FORWARD_INDEX_BARRELS_PATH, "test_forward_index_1")
		self.test_forward_index_path_2 = os.path.join(config.FORWARD_INDEX_BARRELS_PATH, "test_forward_index_2")

		with open(self.test_forward_index_path_1, 'wb+') as test_forward_index_file:
			pickle.dump(test_forward_index_1, test_forward_index_file)

		with open(self.test_forward_index_path_2, 'wb+') as test_forward_index_file:
			pickle.dump(test_forward_index_2, test_forward_index_file)


	def test_create_forward_index(self):
		self.inverted_index.invert_forward_index(self.test_forward_index_path_1)
		self.inverted_index.invert_forward_index(self.test_forward_index_path_2)
		self.inverted_index.merge_buckets()

		"""
	

		"""