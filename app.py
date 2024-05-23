from flask import Flask, request, render_template, make_response
import re
import regex
from multiprocessing import Process, Queue
from email_validator import validate_email, EmailNotValidError
import re2
from oauthlib import uri_validate

app = Flask(__name__)
@app.route('/index', methods=['GET', 'POST'])
def home():
    message = None
    if request.method == 'POST':
        #pattern = r'^([a-zA-Z0-9._]+)+@gmail\.com$' # fixed - ((?:(?:[a-zA-Z0-9._])+))@gmail.com
        pattern = r'A(B|C+)+D'
        string = request.form.get('string')
        if pattern and string:
            match = re.findall(pattern, string)
            if match:
                response = make_response(render_template('index.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('index.html', message='400 Bad Request'), 400)
            return response
    return render_template('index.html', message=message)
    
@app.route('/repair', methods=['GET', 'POST'])
def repair():
    message = None
    if request.method == 'POST':
        #pattern = r'A((?:(?:(?!.).)|(?:(?:[BC])+)))D'
        pattern = r'^((?:(?:[a-zA-Z0-9._])+))@gmail.com$'
        string = request.form.get('string')
        if pattern and string:
            match = re.findall(pattern, string)
            if match:
                response = make_response(render_template('repair.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('repair.html', message='400 Bad Request'), 400)
            return response
    return render_template('repair.html', message=message)

# fuction used for /timeout 
def match_pattern(string, queue):
    match = re.findall(r'^([a-zA-Z0-9._]+)+@gmail\.com$', string)
    queue.put(match)

@app.route('/timeout', methods=['GET', 'POST'])
def timeout():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            queue = Queue()
            p = Process(target=match_pattern, args=(string, queue))
            p.start()
            p.join(1)  # Wait for 1 second
            if p.is_alive():
                p.terminate()
                p.join()
                response = make_response(render_template('timeout.html', message='500 Internal Server Error'), 500)
            else:
                result = queue.get()
                if result:
                    response = make_response(render_template('timeout.html', message='200 OK'), 200)
                else:
                    response = make_response(render_template('timeout.html', message='400 Bad Request'), 400)
            return response
    return render_template('timeout.html', message=message)

@app.route('/diff_regex_engine', methods=['GET', 'POST'])
def diff_regex_engine():
    message = None
    if request.method == 'POST':
        pattern = r'^((?:(?:[a-zA-Z0-9._])+))@gmail.com$'
        string = request.form.get('string')
        try:
            if pattern and string:
                match = re2.match(pattern, string)
                if match:
                    response = make_response(render_template('diff_regex_engine.html', message='200 OK'), 200)
                else:
                    response = make_response(render_template('diff_regex_engine.html', message=re2.error), 400)
        except re2.error:
            response = make_response(render_template('diff_regex_engine.html', message='Error in regex pattern'), 500)

        return response
    return render_template('diff_regex_engine.html', message=message)

@app.route('/alternate_logic', methods=['GET', 'POST'])
def alternate_logic():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            if validate_email(string):
                response = make_response(render_template('alternate_logic.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('alternate_logic.html', message='400 Bad Request'), 400)
            return response
    return render_template('alternate_logic.html', message=message)

@app.route('/limit_input', methods=['GET', 'POST'])
def limit_input():
    message = None
    if request.method == 'POST':
        #pattern = r'^([a-zA-Z0-9._]+)+@gmail\.com$' # fixed - ((?:(?:[a-zA-Z0-9._])+))@gmail.com
        pattern = r'A(B|C+)+D'
        string = request.form.get('string')
        if pattern and string:
            if len(string) > 100: # Enter the value decided by the developers
                response = make_response(render_template('limit_input.html', message='413 Request Entity Too Large'), 413)
            else:
                match = re.findall(pattern, string)
                if match:
                    response = make_response(render_template('limit_input.html', message='200 OK'), 200)
                else:
                    response = make_response(render_template('limit_input.html', message='400 Bad Request'), 400)
            return response
    return render_template('limit_input.html', message=message)

@app.route('/uri_validation', methods=['GET', 'POST'])
def uri_validation():
    message = None
    if request.method == 'POST':
        uri = request.form.get('string')
        if uri:
            if uri_validate.is_uri(uri):
                response = make_response(render_template('uri_validation.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('uri_validation.html', message='400 Bad Request'), 400)
            return response
    return render_template('uri_validation.html', message=message)

def search(r,s):
    SECRET = "this_is_secret"
    return re.match(r,SECRET)

@app.route('/regex_injection', methods=['GET', 'POST'])
def regex_injection():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            queue = Queue()
            p = Process(target=search, args=(string, queue))
            p.start()
            p.join(2)  # Wait for 1 second
            if p.is_alive():
                p.terminate()
                p.join()
                response = make_response(render_template('timeout.html', message='500 Internal Server Error'), 500)
            else:
                result = queue.get()
                if result:
                    response = make_response(render_template('timeout.html', message='200 OK'), 200)
                else:
                    response = make_response(render_template('timeout.html', message='400 Bad Request'), 400)
            return response
    return render_template('timeout.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)