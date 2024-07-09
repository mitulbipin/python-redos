################### Pillow ######################
# https://nvd.nist.gov/vuln/detail/CVE-2021-23437
# https://pillow.readthedocs.io/en/stable/index.html
# Type : Polynomial
# Fix Applied : Input Size Limit

from flask import Blueprint, request, render_template, make_response
from multiprocessing import Process, Queue
from PIL import ImageColor

cve_2021_23437_blueprint = Blueprint('cve_2021_23437', __name__)

@cve_2021_23437_blueprint.route('/cve_2021_23437/index', methods=['GET','POST'])
def index():
    message = None
    if request.method == 'POST':
        value = request.form.get('string')
        if value:
            if ImageColor.getrgb(value):
                response = make_response( '200 OK', 200)
            else:
                response = make_response( '400 Bad Request', 400)
            return response
    return render_template('uri_validation.html', message=message)