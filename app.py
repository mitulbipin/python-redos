from flask import Flask, request, render_template, make_response
import re
import regex
from multiprocessing import Process, Queue

app = Flask(__name__)
@app.route('/index', methods=['GET', 'POST'])
def home():
    message = None
    if request.method == 'POST':
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
    

@app.route('/limit_backtrack', methods=['GET', 'POST'])
def limit_backtrack():
    message = None
    if request.method == 'POST':
        #pattern = regex.compile(r'(A(B|C+)+D){e<=1000}')  # limit backtracking to 1000 steps
        pattern = regex.compile(r'A(B|C+)+D', regex.BESTMATCH, depth=100000000)
        string = request.form.get('string')
        if pattern and string:
            match = pattern.fullmatch(string,partial=True)
            if match:
                response = make_response(render_template('limit_backtrack.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('limit_backtrack.html', message='400 Bad Request'), 400)
            return response
    # if request.method == 'POST':
    #     pattern = r'A(B|C++)+D'
    #     #pattern = r'A(B(*COMMIT)|C+(*PRUNE))+D'  # limit backtracking to 1000 steps
    #     string = request.form.get('string')
    #     if pattern and string:
    #         match = regex.match(pattern, string)
    #         if match:
    #             response = make_response(render_template('limit_backtrack.html', message='200 OK'), 200)
    #         else:
    #             response = make_response(render_template('limit_backtrack.html', message='400 Bad Request'), 400)
    #         return response
    return render_template('limit_backtrack.html', message=message)

def match_pattern(string, queue):
    match = re.findall(r'A(B|C+)+D', string)
    queue.put(match)

def search(r,s):
    SECRET = "this_is_secret"
    return re.match(r,SECRET)

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