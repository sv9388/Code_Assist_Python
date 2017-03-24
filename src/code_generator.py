#import requests
from keywords_extractor import *

class CodeGenerator:
	def __init__(self, stopwords_file = None):
		self.kw_extractor = KeywordsExtractor(stopwords_file)

	def get_code_from_keywords(self, keywords):
		#TODO: Implementation
		return """#TODO: Rename variables in generated code\nop = %s\n#End of generated code""" % keywords 

	def get_code_from_str(self, ip_str, kws_only = False):
		kws = self.kw_extractor.get_keywords(ip_str)
		if kws_only:
			return kws
		code = self.get_code_from_keywords(kws)
		return code		

