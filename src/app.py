#from _typeshed.wsgi import ErrorStream
from flask import Flask, request
from flask_cors import CORS
import json
import os

from assignment import assign
from comparison import compare

app = Flask(__name__)

# Allows CORS ON ALL ROUTES FOR ALL METHODS
CORS(app)

@app.route('/hello_world') #TODO replace with default route and link to API docs
def hello_world():
    return 'Hi Lotsen!'

@app.route('/azur', methods=['POST'])
def azur():
    """
    Main route of the app, accepts an API POST request with assignment parameters and returns distribution,
    possibly assignment sequence, and possibly table depending on inputs
    """
    #TODO docstring

    # Read and parse request JSON
    try:
        request_data = request.get_data()
        input = json.loads(request_data, object_pairs_hook=dict_raise_on_duplicates) # Catch duplicates in input JSON
    
    except Exception as e:
        if type(e) == ValueError: return {'message': str(e)}, 500 # This probably means there's a duplicate key
        return {'message': 'The request JSON could not be parsed.'}, 500 # TODO error codes

    try:
        # Validating input completeness and sanitization
        input_is_valid, error_info, error_code = validate_input(input)
        
        if input_is_valid: return assign(input), 200
        else: return error_info, error_code

    except:
        return {'message': 'An unexpected server error occurred.'}, 500

@app.route('/azur_compare', methods=['POST'])
def azur_compare():

    try:
        request_data = request.get_data()
        input = json.loads(request_data, object_pairs_hook=dict_raise_on_duplicates) # Catch duplicates in input JSON
    
    except Exception as e:
        if type(e) == ValueError: return {'message': str(e)}, 500 # This probably means there's a duplicate key
        return {'message': 'The request JSON could not be parsed.'}, 500 # TODO error codes
    
    #TODO input validation
    
    params_1 = input['dist_A']
    params_2 = input['dist_B']
    num_seats = input['num_of_seats']

    try:
        return compare(params_1, params_2, num_seats), 200
    except:
        return {'message':'An unexpected server error occured.'}, 500


def validate_input(input): #TODO docstring; typing
    """
    Determines whether a given json is a valid input for the API to receive
    :param input: the input JSON received from flask
    :return: 
        (1) a bool with whether or not the input is valid
        (2) if not valid, a dict with error information
        (3) if not valid, an int with the error id
    """

    # Required variables are in request
    try:
        method = input['method']
        votes = input['votes']
        num_of_seats = input['num_of_seats']
    except KeyError as e:
        return False, {'message': f'Value with key {e} is required but was not found in the input data'}, 404

    # Types and dimensions of input are correct
    try:     
        assert type(votes) == dict, f"'votes' parameter must be dict, but got {str(type(votes))}."
        assert all(type(v) == str for v in votes.keys()), "Some or all of of the party names in the votes dictionary are not strings."
        assert all(type(v) == int for v in votes.values()), "Some or all of of the vote values in the votes dictionary are not integers."
        assert all(v >= 0 for v in votes.values()), "Some or all of the vote values in the votes dictionary are negative."
        assert all(v <= 1000000000 for v in votes.values()), "Some or all of the vote values in the votes dictionary are above 1,000,000,000."
        assert all(len(v) in range(1,33) for v in votes.keys()), "Some or all of the party names in the votes dict are not between 1 and 32 characters long."
        assert len(votes) > 0, "The passed votes dictionary is empty."

        assert type(num_of_seats) == int, f"'num_of_seats' parameter must be int, but got {str(type(num_of_seats))}."
        assert type(method) == str, f"'method' parameter must be string, but got {str(type(method))}."

        if 'return_table' in input.keys(): assert type(input['return_table']) == bool, f"'return_table' parameter must be bool, but got {str(type(input['return_table']))}."

    except AssertionError as e:
        return False, {'message': str(e)}, 400

    # All submitted variables are within allowed range
    # TODO turn into asserts
    allowed_methods = ['schepers', 'hare', 'dhondt']
    if method not in allowed_methods: 
        return False, {'message': f"Unknown method: Expected one of {allowed_methods} but got {method}"}, 500
    
    seat_limit = 100000
    if num_of_seats > seat_limit: 
        return False, {'message': f"Num_of_seats ({num_of_seats}) is above accepted limit of {seat_limit}"}, 400
    elif num_of_seats <= 0:
        return False, {'message': f"Num_of_seats ({num_of_seats}) is below 1"}, 400

    parties_limit = 100
    if len(votes) > parties_limit: 
        return False, {'message': f"The votes dictionary contains {len(votes)} parties, above the accepted limit of {parties_limit}"}
    
    return True, None, None

def dict_raise_on_duplicates(ordered_pairs): #TODO docstring; typing
    """Helper function that rejects duplicate keys in dict, passed to json.loads above."""
    d = {}
    for k, v in ordered_pairs:
        if k in d: raise ValueError("Duplicate key: %r" % (k,))
        else: d[k] = v
    return d


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)