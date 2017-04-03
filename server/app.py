import requests, urllib
from flask import session, url_for, Flask, request, redirect, render_template, flash, jsonify
from code_gen_utils import *

SECRET_KEY = "e225eef6c3dadd7e1334b3b2c65d29dff60f2db374a7d4d7"
app = Flask(__name__)
app.secret_key = SECRET_KEY
app_key = "9x8YIuDTJmsYEPH2Lr)SFg(("

main_dict =  {"client_id" : 9277, "client_secret" : "8FLwOKpZQ6H0tgr13i8MlQ((",  "redirect_uri" : "http://52.14.132.27:5000/oauth_authorized" }

default_new_code = """#############################################################################################################################
# 1. Enter your python source code here
# 2. When blocked, type the problem statement here, prefixed with ###. Then select the problem statement and press Generate Code button. Eg.: If you want to append a line to an existing file, type " ###Append line to an existing file " (without quotes) and click Generate code.
# 3. If no selection is made, the app assumes that the last line should be inferred for source codes.
# 4. Click Generate code and verify the rename the local variables from the generated code.
#############################################################################################################################
"""

@app.route("/logout")
def logout():
	session.clear() #ss_token')
	#print "LOGOUT: ", session
	return render_template('login.html')

@app.route("/code_gen", methods = ["POST", "GET"])
def code_editor():
	#print session, session.keys()
	if not 'access_token' in session:
		#print "CODE ED: No access token. Redirecting back" 
		return render_template('login.html')
	
	new_code = default_new_code
	errors = ""
	ip_str = ""
	keywords = []

	if "src_code_content" in request.form.keys():
		old_code = request.form["src_code_content"]
		ip_str = request.form["ip_str"] if "ip_str" in request.form and request.form["ip_str"] != u""  else [x for x in old_code.split("\n") if x.strip() != ""][-1] 
		if ip_str == "":
			errors = "No valid selection found. Please select a string that should be replaced with code or type the input string at the end of code"
			print ip_str, request.form, [x for x in old_code.split("\n") if x.strip() != ""],  errors
			return render_template('code_editor.html', full_code = old_code, errors = errors, keywords = keywords, ip_str = ip_str)
		tab_width = request.form["tab_w"]
		indent_count =( len(ip_str) - len(ip_str.lstrip()))/len(tab_width)

		access_token = session.get('access_token', 'not_set')
		if access_token == 'not_set':
			flash('Can\'t authenticate you. Please try in a new session')
			return render_template('login.html')

		new_code, keywords, errors = get_code_output(old_code, ip_str, tab_width, indent_count, access_token, app_key)

		if errors.startswith("KILL TOKEN:"):
			errors = errors[12:]
			flash(errors)
			return redirect(url_for('logout'))
		return jsonify(full_code = new_code, errors = errors, keywords = keywords, ip_str = ip_str)
	print errors, ip_str
	return render_template('code_editor.html', full_code = new_code, errors = errors, keywords = keywords, ip_str = ip_str)

@app.route("/oauth_authorized")
def oauth_authorized():
	secret_key = request.args.get('code')
	#print request.url 
	if not secret_key:
		flash("Sorry! Wasn't authorized with the right credentials")
		return render_template('login.html')

	#print secret_key
	form_data = main_dict.copy()
	form_data["code"] = secret_key
	resp = requests.post("https://stackexchange.com/oauth/access_token", data =  form_data) 
	#print resp
	if resp.status_code != 200:
		flash("You didn't authorize the app!")
		return render_template('login.html')#render_template('login.html')

	tok_str, scope_str = resp.content.split("&")
	toks = tok_str.split("=")
	if not toks[0] == "access_token":
		flash("Something went wrong while authorizing the app. Please try again later")
		return render_template('login.html')#render_template('login.html')

	session["access_token"] = toks[1]

	return  redirect(url_for('code_editor'))#render_template('code_editor.html', full_code = new_code, errors = errors, keywords = keywords, ip_str = ip_str))

@app.route("/")
def index():
	if 'access_token' in session:
		return redirect(url_for('code_editor'))
	return render_template('login.html')

@app.route('/login')
def login():
	if 'access_token' in session:
		#print "LOGIN: Redirecting to code ed"
		return redirect(url_for('code_editor'))
	oauth_q = main_dict.copy()
	oauth_url_fs = "https://stackexchange.com/oauth?%s"
	#print oauth_url_fs % urllib.urlencode(oauth_q)
	return redirect(oauth_url_fs % urllib.urlencode(oauth_q))

def main():
	app.run(host = '0.0.0.0', port = 5000) #, port = 80, threaded = True) #, debug = True)

if __name__ == "__main__":
	main()

