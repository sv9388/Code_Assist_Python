from code_gen_utils import *
from flask import Flask, render_template, request, session, flash, jsonify

#https://stackapps.com/apps/oauth/view/9277
SECRET_KEY = "e225eef6c3dadd7e1334b3b2c65d29dff60f2db374a7d4d7"
app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods = ["POST", "GET"])
@app.route("/code_gen", methods = ["POST", "GET"])
def code_editor():
	new_code = """#######################################################################################################
# 1. Enter your python source code here
# 2. When blocked, type the problem statement here, SELECT the problem statement and press enter.
# 3. If no selection is made, the app assumes that the last line should be inferred for source codes.
# 4. Click Generate code and verify the rename the local variables from the generated code.
#######################################################################################################

"""
	errors = ""
	keywords = []
	ip_str = ""

	if "src_code_content" in request.form.keys() and request.form["ip_str"] != "":
		old_code = request.form["src_code_content"]
		ip_str = request.form["ip_str"]
		delimiter = request.form["delim"]
		indent_count = len(ip_str) - len(ip_str.lstrip())
		new_code, keywords, errors = get_code_output(old_code, ip_str, indent_count)
		return jsonify(full_code = new_code, errors = errors, keywords = keywords, ip_str = ip_str)
	return render_template('code_editor.html', full_code = new_code, errors = errors, keywords = keywords, ip_str = ip_str) 

@app.route("/login")
def login():
	pass

if __name__ == '__main__':
	app.run(threaded = True, debug = True)
