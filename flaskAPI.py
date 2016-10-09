from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/coordinate/<lat1>,<long1>;<lat2>,<long2>')
def get_route(lat1, long1, lat2, long2, time):
    # Validate all parameters are valid latitudes and longitudes
    if not is_latitude(lat1):
        return invalid('Latitude 1 not valid')
    elif not is_latitude(lat2):
        return invalid('Latitude 2 not valid')
    elif not is_longitude(long1):
        return invalid('Longitude 1 not valid')
    elif not is_longitude(long2):
        return invalid('Longitude 2 not valid')
    elif not is_time(time):
        return invalid('Time is not valid')

    # add all params to a dict to be converted to a json array
    newDict = {'lat1': lat1, 'long1': long1, 'lat2': lat2, 'long2': long2, 'time': time}

    #wants, year, month, day, time
    return jsonify(**newDict)


# check if a latitude is valid
def is_latitude(s):
    try:
        f = float(s)
        if not 90 > f > -90:
            return False
        return True
    except ValueError:
        return False


# check if a longitude is valid
def is_longitude(s):
    try:
        f = float(s)
        if not 180 > f > -180:
            return False
        return True
    except ValueError:
        return False

def is_time(time):
    if time < 0 || time > 24:
        return False


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer

    return 'Post %d' % post_id


# handle any 404 errors
@app.errorhandler(404)
def not_found(error=None):

    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


# handle any invalid requests
@app.errorhandler(400)
def invalid(error=None):
    error_message = 'Bad Request'

    if error is not None:
        error_message = 'Bad Request: ' + error

    message = {
        'status': 400,
        'message': error_message,
    }

    resp = jsonify(message)
    resp.status_code = 400

    return resp
