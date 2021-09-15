from flask import Flask, request
from flask_cors import CORS

from assignment import schepers, dhondt, hare_niemeyer


app = Flask(__name__)

# Allows CORS ON ALL ROUTES FOR ALL METHODS
CORS(app)

@app.route('/hello_world')
def hello_world():
    return 'Hello World from the API'


@app.route('/azur', methods=['POST'])
def azur():
    input = request.get_json()

    # Checking if all inputs are there
    try:
        method = input['method']
        votes = input['votes']
        num_of_seats = input['num_of_seats']
    except KeyError as e:
        return f'Value with key {e} is required but wa snot found in the input data', 404
    except Exception as e:
        return 'An unexpected error occured', 500

    # TODO Input validation and sanitization (no too large arrays and so on)


    allowed_methods = ['schepers', 'hare', 'dhondt']

    if method == 'schepers':
        seats, assignment_sequence = schepers(votes, num_of_seats)
    elif method == 'dhondt':
        seats, assignment_sequence = dhondt(votes, num_of_seats)
    elif method == 'hare':
        seats = hare_niemeyer(votes, num_of_seats)
        assignment_sequence = None
    else:
        return f'Unknown method: Expected one of {str(allowed_methods)} but got {method}', 500

    return (
        {
           "seats": seats,
           "assignment_sequence": assignment_sequence
        },
        200
    )