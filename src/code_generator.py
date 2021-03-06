import requests
import urllib, json
from keywords_extractor import *
from bs4 import BeautifulSoup as bs

MAX_SNIPPETS = 5
server_url_fs = "https://api.stackexchange.com/2.2/search/advanced?%s"

#TODO: Fill Client key after oayth impl
params = { "page" : 1 , "pagesize" : 100, "order" : "desc" , "sort" : "relevance" , "q" : "" , "tagged" : "python" , "site" : "stackoverflow", "accepted" : "True" }

answer_url_fs = "https://stackoverflow.com/a/%d"

def get_all_answers(ip_str, keywords, page = 1, access_token = None, app_key = None):
	items = []
	errors = ''

	if len(keywords) == 0:
		errors = 'No valid keywords detected. Please post a specific question'
		return [], errors 

	params["q"] = ip_str #' '.join(keywords)
	params["page"] = page
	if access_token and app_key:
		#print access_token, app_key
		params['access_token'] = access_token
		params['key'] = app_key.strip()
	query_str = urllib.urlencode(params)
	#print server_url_fs % query_str

	r = requests.get(server_url_fs % query_str)

	js_data = json.loads(r.text)
	if r.status_code != 200:
		if js_data["error_id"] in [ 406, 403 ]:
			errors = "KILL TOKEN: Internal error. Please login again"
		else:
			errors = 'Unable to make API Request. Please try again after sometime'
		return items, errors

	items = js_data['items']
	if False: #js_data['has_more']:
		next_items, new_errors = get_all_answers(ip_str, keywords, page + 1, access_token, app_key)
		items += next_items
		errors += ' ' + new_errors
	else:
		print "Request count : ", js_data['quota_remaining'], " Page = ", page
	return items, errors 

#Code is compatible with https://github.com/google/code-prettify html
def get_code_in_answer_id(answer_id):
	start_line = u"# CODE ASSIST: TODO: Rename variables in generated code\n"
	end_line = u"\n# CODE ASSIST: End of generated code"

	url = answer_url_fs % answer_id
	r = requests.get(url)
	if r.status_code != 200:
		errors = "Invalid URL at %s" % url 
		return [], url,  errors
 
	soup = bs(r.text, "html.parser")
	answer_div = soup.find("div", attrs = {'data-answerid' : str(answer_id)})
	pre_divs = answer_div.find_all("pre")

	code_snippets = []
	errors = ''  
	if  len(pre_divs) == 0:
		pre_divs = answer_div.find_all('code')

	if len(pre_divs) == 0:
		errors = u"WARN: No valid code snippets found. Break the query into subproblems. The closest match to your query is at %s" %url
	else:
		for div in pre_divs:
			cd = div.find('code')
			if cd:
				code_snippets.append(cd.text.strip())

	return code_snippets, url, errors

def get_code_snippets(answers):
	code_snippets = []
	for answer in answers:
		if 'accepted_answer_id' in answer.keys():
			cs_op = get_code_in_answer_id(answer['accepted_answer_id'])
			arr = [[answer['title'], x, cs_op[1], cs_op[2]] for x in cs_op[0]]
			code_snippets = code_snippets + arr
			if len(code_snippets) >= MAX_SNIPPETS:
				break

	if len(code_snippets) == 0:
		return [['', '', '', 'No answers at all']]
	return code_snippets

def get_code(ip_str, keywords, access_token = None, app_key = None):
	code = []
	errors = ''
	answers, errors = get_all_answers(ip_str, keywords, 1, access_token, app_key)
	if len(answers) == 0:
		if len(errors) == 0:
			errors = "No answers retrieved. Break it into subproblems and retry  per problem or rephrase the existing question"
		return [['', code, '', errors]]

	repls = get_code_snippets(answers)
	return repls

class CodeGenerator:
	def __init__(self, stopwords_file = None):
		self.kw_extractor = KeywordsExtractor(stopwords_file)

	def get_code_from_keywords(self, ip_str, keywords, access_token = None, app_key = None):
		code_snippets = get_code(ip_str, keywords, access_token, app_key)
		return code_snippets

	def get_code_from_str(self, ip_str, kws_only = False, access_token = None, app_key = None):
		kws = self.kw_extractor.get_keywords(ip_str)
		if kws_only:
			return [], kws
		code_snippets = self.get_code_from_keywords(ip_str, kws, access_token, app_key)
		return code_snippets, kws

