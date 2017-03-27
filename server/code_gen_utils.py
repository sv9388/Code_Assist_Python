import sys
sys.path.append("../src")
from code_generator import *

def update_code(code, indent_by):
	lspace = indent_by * ' '

	clines = code.split("\n")
	modified_code_snippet = ""
	for ln in clines:
		modified_code_snippet += (lspace + ln + '\n')
	return modified_code_snippet

def get_code_output(old_code, ip_str, indent_count):
	cg = CodeGenerator()
	code_snippet, keywords, errors = cg.get_code_from_str(ip_str)
	if not errors or errors.strip() != "":
		modified_code_snippet = update_code(code_snippet, indent_count)
		new_code = old_code.replace(ip_str, modified_code_snippet)
	else:
		new_code = old_code
	return new_code, keywords, errors
