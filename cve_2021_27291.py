################### Pygments ####################
# https://nvd.nist.gov/vuln/detail/CVE-2021-27291
# https://pygments.org/
# Type : Exponential
# Fix Applied : Repaired the regular expression

from flask import Blueprint, request, render_template, make_response
from multiprocessing import Process, Queue
import subprocess
from pygments import highlight
from pygments.lexers import PythonLexer,get_lexer_by_name
from pygments.formatters import HtmlFormatter

cve_2021_27291_blueprint = Blueprint('cve_2021_27291', __name__)

@cve_2021_27291_blueprint.route('/cve_2021_27291/index', methods=['GET','POST'])
def index():
    message = None
    if request.method == 'POST':
        value = request.form.get('string')
        if value:
            lexer = get_lexer_by_name("odin", stripall=True)
            formatter = HtmlFormatter(linenos=True, cssclass="source")
            highlighted_code = highlight(value, lexer, formatter)
            response = make_response(render_template('odin.html', message='200 OK', highlighted_code=highlighted_code), 200)
            return response
    return render_template('odin.html', message=message)

@cve_2021_27291_blueprint.route('/cve_2021_27291/index1', methods=['GET', 'POST'])
def home():
    message = None
    highlighted_code = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            # Write the input string to a temporary file
            with open('temp.odin', 'w') as temp_file:
                temp_file.write(string)
            
            # Run the pygmentize command
            result = subprocess.run(['pygmentize','temp.odin'], capture_output=True, text=True)
            
            # Capture the output
            highlighted_code = result.stdout
            
            response = make_response(highlighted_code, 200)
            return response
    return render_template('index.html', message=message, highlighted_code=highlighted_code)