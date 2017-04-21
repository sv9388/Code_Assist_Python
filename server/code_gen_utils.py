import sys
sys.path.append("../src")
from code_generator import *

def update_code(code, tab_width, indent_by):
	lspace = indent_by * tab_width

	clines = code.split("\n")
	modified_code_snippet = ""
	for ln in clines:
		modified_code_snippet += (lspace + ln + '\n')
	return modified_code_snippet

def get_code_output(old_code, full_ip_str,  tab_width, indent_count, access_token = None, app_key = None):
	if not full_ip_str.strip().startswith("###") or not ( full_ip_str.strip()[3:].strip()[0].isalpha() or full_ip_str.strip()[3:].strip()[0] == '"'):
		return old_code, "", [], "Please type the problem statement in the format ###&lt;problem_statement&gt;"

	ip_str = full_ip_str.strip()[3:]
	cg = CodeGenerator()
	code_snippet, answer_link, keywords, errors = cg.get_code_from_str(ip_str, False, access_token, app_key)
	if not errors or errors.strip() != "":
		modified_code_snippet = update_code(code_snippet, tab_width, indent_count)
		new_code = old_code.replace(full_ip_str, modified_code_snippet)
	else:
		new_code = old_code
	return new_code, answer_link, keywords, errors
