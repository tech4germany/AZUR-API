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

    # Checking if all mandatory inputs are there
    try:
        method = input['method']
        votes = input['votes']
        num_of_seats = input['num_of_seats']
    except KeyError as e:
        return f'Value with key {e} is required but was not found in the input data', 404
    except Exception as e:
        return 'An unexpected error occured', 500

    # Handling return_table
    return_table = False
    if 'return_table' in input.keys(): return_table = input['return_table']

    # TODO Input validation and sanitization (no too large arrays and so on)

    allowed_methods = ['schepers', 'hare', 'dhondt']

    if method == 'schepers':
        outputs = schepers(votes, num_of_seats, return_table)
    elif method == 'dhondt':
        outputs = dhondt(votes, num_of_seats, return_table)
    elif method == 'hare':
        seats = hare_niemeyer(votes, num_of_seats)
        outputs = (seats, None)
    else:
        return f'Unknown method: Expected one of {str(allowed_methods)} but got {method}', 500
    
    seats = outputs[0]
    
    if method != 'hare':
        assignment_sequence = outputs[1]
        if return_table: 
            table = outputs[2]
            return (
                {
                "seats": seats,
                "assignment_sequence": assignment_sequence,
                "table": table,
                },
                200
            )  
        return (
            {
            "seats": seats,
            "assignment_sequence": assignment_sequence
            },
            200
        )
    return (
    {
    "seats": seats,
    },
    200
)