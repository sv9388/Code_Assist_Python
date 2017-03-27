import requests
import urllib, json
from keywords_extractor import *
from bs4 import BeautifulSoup as bs

server_url_fs = "http://api.stackexchange.com/2.2/search/advanced?%s"

#TODO: Fill Client key after oayth impl
params = { "page" : 1 , "pagesize" : 100, "order" : "desc" , "sort" : "relevance" , "q" : "" , "tagged" : "python;python-2.7" , "site" : "stackoverflow", "accepted" : "True" }

answer_url_fs = "http://stackoverflow.com/a/%d"

def get_all_answers(keywords, page = 1):
	items = []
	errors = ''

	if len(keywords) == 0:
		errors = 'No valid keywords detected. Please post a specific question'
		return [], errors 

	params["q"] = ' '.join(keywords)
	params["page"] = page
	query_str = urllib.urlencode(params)
	r = requests.get(server_url_fs % query_str)
	if r.status_code != 200:
		errors = 'Unable to make API Request. Please try again after sometime'
		return items, errors

	js_data = json.loads(r.text)
	items = js_data['items']
	if js_data['has_more']:
		next_items, new_errors = get_all_answers(keywords, page + 1)
		items += next_items
		errors += ' ' + new_errors

	return items, errors 

#Code is compatible with https://github.com/google/code-prettify html
def get_code_in_answer_id(answer_id):
	start_line = u"####CODE ASSIST: TODO: Rename variables in generated code ###\n"
	end_line = u"###CODE ASSIST: End of generated code"

	url = answer_url_fs % answer_id
	r = requests.get(url)
	if r.status_code != 200:
		errors = "Invalid URL at %s" % url 
		return "", errors
 
	soup = bs(r.text, "html.parser")
	answer_div = soup.find("div", attrs = {'data-answerid' : str(answer_id)})
	#TODO: Multiple code snippets in accepted answer. So rewrite this aprt. 
	code_div = answer_div.find("code")

	code = ''  
	errors = ''  
	if not code_div:
		errors = u"#No valid code snippets found. Break the query into subproblems or refer to the details in %s" %url
	else:
		code = code_div.text

	return start_line + code + end_line, errors
	

def get_code(keywords):
	code = ''
	errors = ''
	answers, errors = get_all_answers(keywords)
	if len(answers) == 0:
		if len(errors) == 0:
			errors = "No answers retrieved. Break it into subproblems and retry  per problem or rephrase the existing question"
		return code, errors

	#TODO: Figure out the more relevant answer
	code, errors = get_code_in_answer_id(answers[0]['accepted_answer_id'])
	return code, errors

class CodeGenerator:
	def __init__(self, stopwords_file = None):
		self.kw_extractor = KeywordsExtractor(stopwords_file)

	def get_code_from_keywords(self, keywords):
		code, errors = get_code(keywords)
		return code, errors

	def get_code_from_str(self, ip_str, kws_only = False):
		kws = self.kw_extractor.get_keywords(ip_str)
		if kws_only:
			return '', kws, ''
		code, errors = self.get_code_from_keywords(kws)
		return code, kws, errors

