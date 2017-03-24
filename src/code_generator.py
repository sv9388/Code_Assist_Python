import requests
import urllib, json
from keywords_extractor import *
from bs4 import BeautifulSoup as bs

server_url_fs = "http://api.stackexchange.com/2.2/search/advanced?%s"
#TODO: Fill Client key after oayth impl
params = { "page" : 1 , "pagesize" : 100, "order" : "desc" , "sort" : "relevance" , "q" : "" , "tagged" : "python;python-2.7" , "site" : "stackoverflow", "accepted" : "True" }
answer_url_fs = "http://stackoverflow.com/a/%d"
def get_all_answers(keywords, page = 1):
	if len(keywords) == 0:
		return []
	params["q"] = ' '.join(keywords)
	params["page"] = page
	query_str = urllib.urlencode(params)
	r = requests.get(server_url_fs % query_str)
	js_data = json.loads(r.text)
	
	items = js_data['items']
	if js_data['has_more']:
		items += get_all_answers(keywords, page + 1)

	return items 

#Code is compatible with https://github.com/google/code-prettify html
def get_code_in_answer_id(answer_id):
	url = answer_url_fs % answer_id
	r = requests.get(url)
	soup = bs(r.text, "html.parser")
	answer_div = soup.find("div", attrs = {'data-answerid' : str(answer_id)})
	#TODO: Multiple code snippets in accepted answer. So rewrite this aprt. 
	code_div = answer_div.find("code")

	code = None
	if not code_div:
		code = u"#No valid code snippets found. Break the query into subproblems or refer to the details in %s\n" %url
	else:
		code = code_div.text
	start_line = u"####CODE ASSIST: TODO: Rename variables in generated code ###\n"
	end_line = u"###CODE ASSIST: End of generated code"

	return start_line + code + end_line
	

def get_code(keywords):
	answers = get_all_answers(keywords)
	if not answers or len(answers) == 0:
		return ""

	#TODO: Figure out the more relevant answer
	code = get_code_in_answer_id(answers[0]['accepted_answer_id'])
	return code

class CodeGenerator:
	def __init__(self, stopwords_file = None):
		self.kw_extractor = KeywordsExtractor(stopwords_file)

	def get_code_from_keywords(self, keywords, delimiter):
		code = get_code(keywords)
		return code

	def get_code_from_str(self, ip_str, kws_only = False, delimiter = None):
		kws = self.kw_extractor.get_keywords(ip_str)
		if kws_only:
			return kws
		code = self.get_code_from_keywords(kws, delimiter)
		return code		

