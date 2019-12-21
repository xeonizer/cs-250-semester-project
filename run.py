# from generators import generate_lexicon, generate_forward_index, generate_inverted_index


# generate_lexicon.main()
# generate_forward_index.main()
# generate_inverted_index.main()


import config
from indexing.lexicon import Lexicon
from indexing.inverted_index import InvertedIndex
from search.search import Search

lexicon = Lexicon(config.LEXICON_PATH)
inverted_index = InvertedIndex(config.INVERTED_INDEX_BARRELS_PATH, config.INVERTED_INDEX_BARRELS_TEMP_PATH, len(lexicon), config.INVERTED_INDEX_BARREL_SIZE)

search = Search(lexicon, inverted_index)
# search.search("Rayn Gosling")
search.search("Paul Ryan")
