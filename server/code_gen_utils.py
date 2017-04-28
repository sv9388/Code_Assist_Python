import sys
sys.path.append("../src")
from code_generator import *

def update_code(title, code, link,  indent_by):
	lspace = ' ' * indent_by

	clines = code.split("\n")
	modified_code_snippet = "## %s at  %s \n"%(title, link)
	for ln in clines:
		modified_code_snippet += (lspace + ln + '\n')
	modified_code_snippet += '\n'
	return modified_code_snippet

def update_all(code_snippets, indent_by, full_ip_str):
	new_snips = []
	answer_links = []
	errors = ''

	if len(code_snippets) == 1:
		err =  code_snippets[0][-1]
		if err.strip() != '':
			return [full_ip_str.strip()], answer_links, err
 
	for code_snippet in code_snippets:
            if code_snippet[-1].strip() != '':
                #print code_snippet
                continue
            modified_code_snippet = update_code(code_snippet[0],  code_snippet[1], code_snippet[2], indent_by)
            new_snips.append(modified_code_snippet)
            answer_links.append(code_snippet[2])

	if len(new_snips) == 0:
		new_snips, errors = [full_ip_str.strip()],  'No valid solutions found. Break the question into subproblems and retry'
	return new_snips, list(set(answer_links)), errors

def get_code_output(old_code, full_ip_str,  indent_by, access_token = None, app_key = None):
	if not full_ip_str.strip().startswith("###") or not ( full_ip_str.strip()[3:].strip()[0].isalpha() or full_ip_str.strip()[3:].strip()[0] == '"'):
		return old_code, "", [], "Please type the problem statement in the format ###&lt;problem_statement&gt;"

	ip_str = full_ip_str.strip()[3:]
	cg = CodeGenerator()
	code_snippets, keywords = cg.get_code_from_str(ip_str, False, access_token, app_key)
	new_code_snippets, answer_links, errors = update_all(code_snippets, indent_by, full_ip_str)
	return new_code_snippets, answer_links, errors, keywords #ywords, errors
