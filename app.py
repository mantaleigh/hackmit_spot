"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

spot_available = False

total_avail_spots = 5

import os, random
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_secret')

@app.route('/')
def search():
    """Render website's search page."""
    return render_template('search.html', total_avail_spots=total_avail_spots)


@app.route('/selected/')
def selected():
    """Render the website's selected page."""
    return render_template('selected.html')

@app.route('/parked/')
def parked():
    """Render the website's parked page."""
    return render_template('parked.html')

@app.route('/availability_data', methods=['GET', 'POST'])
def availability_data():
    global spot_available # gross, but whatever it's a hackathon #fuckitshipit
    if request.method == 'POST' and 'availability' in request.form.keys():
        spot_available = bool(int(request.form['availability']))
        response = jsonify(request.form) # echo the received info back
        return response

@app.route('/get_availability')
def get_availability():
    global spot_available
    return jsonify(spot_available)



###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
