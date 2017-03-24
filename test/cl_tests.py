import argparse
import sys
sys.path.insert(0, '/home/ubuntu/code_assist_python/src')
from code_generator import *


def get_code_snippet(ip_str, kws_only):
	cg = CodeGenerator()
	return cg.get_code_from_str(ip_str, kws_only)

def main():
	parser = argparse.ArgumentParser(description='Extracts keywords and/or code snippets from a given input string. By default, the command retrieves the corresponding code snippet')
	parser.add_argument('test_str', metavar = 'test_str',  default = 'help', type = str, nargs = '+', help = 'The free form string from which the required code snippet will be pulled.')
	parser.add_argument('--keywords', action='store_true', required = False, help='(Optional) Argument to extract only the relevant keywords')

	try:
		args = parser.parse_args()

		ip_str = ' '.join(args.test_str)
		op = get_code_snippet(ip_str, args.keywords)
		print op
	except:
		parser.print_help()
		sys.exit(0)

if __name__ == "__main__":
	main()
