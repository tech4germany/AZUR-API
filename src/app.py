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
    """
    Main route of the app, accepts an API POST request with assignment parameters and returns distribution,
    possibly assignment sequence, and possibly table depending on inputs
    """
    input = request.get_json()

    try:
        # Validating input completeness and sanitization
        input_is_valid, error_info, error_code = validate_input(input)
        
        if input_is_valid:
            return assign(input), 200
        else: 
            return error_info, error_code

    except:
        return {'message': 'An unexpected server error occurred.'}, 500

def validate_input(input): #TODO docstring; typing
    """
    Determines whether a given json is a valid input for the API to receive
    :param input: the input JSON received from flask
    :return: 
        (1) a bool with whether or not the input is valid or not
        (2) if not valid, a dict with error information
        (3) if not valid, an int with the error id
    """

    try:
        method = input['method']
        votes = input['votes']
        num_of_seats = input['num_of_seats']
    except KeyError as e:
        return False, {'message': f'Value with key {e} is required but was not found in the input data'}, 404

    if method not in ['schepers', 'hare', 'dhondt']: 
        return False, {'message': f"Unknown method: Expected one of ['dhondt', 'schepers', 'hare'] but got {method}"}, 500

    seat_limit = 100000
    if num_of_seats > seat_limit: 
        return False, {'message': f"Num_of_seats ({num_of_seats}) is above accepted limit of {seat_limit}"}, 400
    return True, None, None

def assign(input): #TODO docstring; typing
    """
    Calls the assignment method required by an assignment input JSON and returns the output the method produces. Assumes
    the input is validated.
    """
    votes = input['votes']
    method = input['method']
    num_seats = input['num_of_seats']

    # Handling return_table
    return_table = False
    if 'return_table' in input.keys(): return_table = input['return_table']

    if method == 'schepers':
        output = schepers(votes, num_seats, return_table)
    elif method == 'dhondt':
        output = dhondt(votes, num_seats, return_table)
    elif method == 'hare':
        output = hare_niemeyer(votes, num_seats)
    
    return output