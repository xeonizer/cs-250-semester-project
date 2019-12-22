import sys
import argparse
import config
from generators import generate_lexicon, generate_forward_index, generate_inverted_index
from indexing.lexicon import Lexicon
from indexing.inverted_index import InvertedIndex
from search.search import Search


def main():
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='subparser')

	lexicon_argparser = subparser.add_parser("generate_lexicon")
	lexicon_argparser.add_argument('--b_range', type=str, help="Batches numbers range start and end creating/updating lexicon from. For example 1,3")
	lexicon_argparser.add_argument('--d', type=int, default=0, help="Print demo results.")

	forward_index_argparser = subparser.add_parser("generate_forward_index")
	forward_index_argparser.add_argument('--b_range', type=str, help="Batches numbers range start and end creating/updating forward index from. For example 1,3")
	forward_index_argparser.add_argument('--d', type=int, default=0, help="Print demo results.")

	inverted_index_argparser = subparser.add_parser("generate_inverted_index")
	inverted_index_argparser.add_argument('--b', type=str, help="Forward Index Batches to create inverted_index from. Comma Separated.")
	inverted_index_argparser.add_argument('--d', type=int, default=0, help="Print demo results.")

	search = subparser.add_parser("search")
	search.add_argument("--q", type=str, help="Search Query.")

	args = parser.parse_args()

	if args.subparser == 'generate_lexicon':
		batche_range = list(map(int, args.b_range.split(",")))
		generate_lexicon.main(*batche_range, demo=args.d)
	elif args.subparser == 'generate_forward_index':
		batche_range = list(map(int, args.b_range.split(",")))
		generate_forward_index.main(*batche_range, demo=args.d)
	elif args.subparser == 'generate_inverted_index':
		batches = args.b.split(',')
		generate_inverted_index.main(batches, demo=args.d)
	elif args.subparser == 'search':
		lexicon = Lexicon(config.LEXICON_PATH)
		inverted_index = InvertedIndex(config.INVERTED_INDEX_BARRELS_PATH, config.INVERTED_INDEX_BARRELS_TEMP_PATH, len(lexicon), config.INVERTED_INDEX_BARREL_SIZE)
		search = Search(lexicon, inverted_index)
		print(search.search(args.q))


if __name__ == '__main__':
	main()
