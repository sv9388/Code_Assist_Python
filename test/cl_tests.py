import argparse, traceback, sys
sys.path.insert(0, '/home/ubuntu/code_assist_python/src')
from code_generator import *

debug = False
def get_code_snippet(ip_str, kws_only):
	cg = CodeGenerator()
	code, keywords, errors =  cg.get_code_from_str(ip_str, kws_only  = kws_only)
	return code, keywords, errors 

def main():
	parser = argparse.ArgumentParser(description='Extracts keywords and/or code snippets from a given input string. By default, the command retrieves the corresponding code snippet')
	parser.add_argument('test_str', metavar = 'test_str',  default = 'help', type = str, nargs = '+', help = 'The free form string from which the required code snippet will be pulled.')
	parser.add_argument('--keywords', action='store_true', required = False, help='Extracts only the relevant keywords instead of code snippets')
	try:
		args = parser.parse_args()
		ip_str = ' '.join(args.test_str)
		code, keywords, errors = get_code_snippet(ip_str, args.keywords)
		if len(errors) == 0 and not args.keywords:
			print code
		else:
			print 'Keywords: \n\t', keywords, '\nErrors: \n\t', "None" if len(errors) == 0 else errors
	except:
		if debug:
			traceback.print_exc()
		"""
		print "Incorrect usage"
		parser.print_help()"""
		sys.exit(0)

if __name__ == "__main__":
	main()
