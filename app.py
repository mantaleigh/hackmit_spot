"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os, random, datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

spot_available = False
initTimestamp = None

hasVisitedParked = False

defaultMeterTime = datetime.time(2, 0, 0, 0) # 2 hours

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secret_secret')

@app.route('/')
def search():
    """Render website's search page."""
    global hasVisitedParked
    hasVisitedParked = False
    return render_template('search.html', showSearch=True)

@app.route('/selected/')
def selected():
    """Render the website's selected page."""
    return render_template('selected.html', showBackToMap=True)

@app.route('/parked/')
def parked():
    """Render the website's parked page."""
    global initTimestamp
    global hasVisitedParked

    if not hasVisitedParked:
        initTimestamp = datetime.datetime.time(datetime.datetime.now())
        hasVisitedParked = True

    return render_template('parked.html', showBackToMap=True, time_remaining='2 hr 0 mins', meter_val='$0.00', time_used='0 MINUTES')

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

@app.route('/get_parking_updates')
def get_parking_updates():
    global initTimestamp
    global hasVisitedParked
    global defaultMeterTime


    if initTimestamp:
        currentTime = datetime.datetime.now()

        # print "currentTime----> " + str(currentTime)
        # print "defaultMeterTime----> " + str(defaultMeterTime)
        # print "initTimestamp----> " + str(initTimestamp)

        temp_delta = currentTime - datetime.datetime.combine(datetime.date.today(), initTimestamp)

        # print temp_delta
        # print datetime.datetime.combine(datetime.date.today(), defaultMeterTime) - temp_delta

        timeString = '2 hr 0 mins'
        

        # timeString = delta.strftime('%I hr %M mins')

        # datetime.combine(temp_delta, )



    else: 
        timeString = '2 hr 0 mins'





    return jsonify({'time_left': timeString})

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
