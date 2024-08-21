################### URL-LIB ####################
# https://nvd.nist.gov/vuln/detail/CVE-2022-36087
# Type : Exponential
# Fix Applied : Repaired the regular expression

from flask import Blueprint, request, render_template, make_response
import re
from multiprocessing import Process, Queue
#import re2
from oauthlib import uri_validate

cve_2022_36087_blueprint = Blueprint('cve_2022_36087', __name__)

def is_valid_uri(uri):
    # Check if the URI starts with http:// or https://
    if not (uri.startswith('http://') or uri.startswith('https://')):
        return False
    
    # Extract the domain part by removing the protocol
    domain_part = uri.split("://")[1].split("/")[0]
    
    # Check if there is at least one "." in the domain, indicating a domain name
    if '.' not in domain_part:
        return False
    
    # Split the domain part into subdomains and a TLD
    domain_sections = domain_part.split('.')
    
    # Ensure each section of the domain contains only letters or digits
    for section in domain_sections:
        if not section.isalnum():
            return False
    
    return True

@cve_2022_36087_blueprint.route('/cve_2022_36087/index', methods=['GET','POST'])
def index():
    message = None
    if request.method == 'POST':
        uri = request.form.get('string')
        if uri:
            if uri_validate.is_uri(uri,2):
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)

@cve_2022_36087_blueprint.route('/cve_2022_36087/repair', methods=['GET','POST'])
def repair():
    message = None
    if request.method == 'POST':
        uri = request.form.get('string')
        if uri:
            if uri_validate.is_uri(uri,2):
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)

@cve_2022_36087_blueprint.route('/cve_2022_36087/diff_regex_engine', methods=['GET','POST'])
def diff_regex_engine():
    message = None
    if request.method == 'POST':
        uri = request.form.get('string')
        if uri:
            if uri_validate.is_uri(uri,1):# 1 indicates re2 is used as regex engine
                response = make_response(render_template('uri_validation.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('uri_validation.html', message='400 Bad Request'), 400)
            return response
    return render_template('uri_validation.html', message=message)

@cve_2022_36087_blueprint.route('/cve_2022_36087/alternate_logic', methods=['GET','POST'])
def alternate_logic():
    message = None
    if request.method == 'POST':
        uri = request.form.get('string')
        if uri:
            if is_valid_uri(uri):# 1 indicates re2 is used as regex engine
                response = make_response(render_template('uri_validation.html', message='200 OK'), 200)
            else:
                response = make_response(render_template('uri_validation.html', message='400 Bad Request'), 400)
            return response
    return render_template('uri_validation.html', message=message)

def match_pattern_uri(string, queue):
    match = uri_validate.is_uri(string,2)
    #print(match)
    queue.put(match)

@cve_2022_36087_blueprint.route('/cve_2022_36087/timeout', methods=['GET', 'POST'])
def timeout_cve():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            queue = Queue()
            p = Process(target=match_pattern_uri, args=(string, queue))
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

@cve_2022_36087_blueprint.route('/cve_2022_36087/modified_timeout', methods=['GET', 'POST'])
def modified_timeout_cve():
    message = None
    if request.method == 'POST':
        string = request.form.get('string')
        if string:
            queue = Queue()
            p = Process(target=match_pattern_uri, args=(string, queue))
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