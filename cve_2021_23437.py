################### Pillow ######################
# https://nvd.nist.gov/vuln/detail/CVE-2021-23437
# https://pillow.readthedocs.io/en/stable/index.html
# Type : Polynomial
# Fix Applied : Input Size Limit

from flask import Blueprint, request, render_template, make_response
from multiprocessing import Process, Queue
from PIL import ImageColor

cve_2021_23437_blueprint = Blueprint('cve_2021_23437', __name__)

###################################### Functional
@cve_2021_23437_blueprint.route('/cve_2021_23437/index', methods=['GET','POST'])
def index():
    message = None
    if request.method == 'POST':
        value = request.form.get('string')
        if value:
            if ImageColor.getrgb(value,1):
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)

###### Nicht Funktionierte
@cve_2021_23437_blueprint.route('/cve_2021_23437/repair', methods=['GET','POST'])
def repair():
    message = None
    if request.method == 'POST':
        value = request.form.get('string')
        if value:
            if ImageColor.getrgb(value,3): # 3 indicates the repaired version
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)

def match_pattern(string, queue):
    match = ImageColor.getrgb(string,1)
    #print(match)
    queue.put(match)

###################################### Functional
@cve_2021_23437_blueprint.route('/cve_2021_23437/timeout', methods=['GET', 'POST'])
def timeout_cve():
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
                response = make_response('500 Internal Server Error', 500)
            else:
                result = queue.get()
                if result:
                    response = make_response( '200 OK', 200)
                else:
                    response = make_response( '400 Bad Request', 400)
            return response
    return render_template('timeout.html', message=message)

@cve_2021_23437_blueprint.route('/cve_2021_23437/modified_timeout', methods=['GET', 'POST'])
def modified_timeout_cve():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            queue = Queue()
            p = Process(target=match_pattern, args=(string, queue))
            p.start()
            p.join(0.5) 
            if p.is_alive():
                p.terminate()
                p.join()
                response = make_response('500 Internal Server Error', 500)
            else:
                result = queue.get()
                if result:
                    response = make_response( '200 OK', 200)
                else:
                    response = make_response( '400 Bad Request', 400)
            return response
    return render_template('timeout.html', message=message)

def custom_getrgb(color_name):
    color_dict = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        # Add more color names and their RGB values as needed
    }
    return color_dict.get(color_name.lower(), (0, 0, 0))  # Default to black if color not found


@cve_2021_23437_blueprint.route('/cve_2021_23437/alternate_logic', methods=['GET', 'POST'])
def alternate_logic():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            if custom_getrgb(string):
                response = make_response('200 OK', 200)
            else:
                response = make_response('400 Bad Request', 400)
            return response
    return render_template('alternate_logic.html', message=message)

###################################### Functional
@cve_2021_23437_blueprint.route('/cve_2021_23437/diff_regex_engine', methods=['GET','POST'])
def diff_regex_engine():
    message = None
    if request.method == 'POST':
        value = request.form.get('string')
        if value:
            if ImageColor.getrgb(value,2): # 2 indicates re2 is used as the regex
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)