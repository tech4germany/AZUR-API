import pytest
import csv
import ast

from assignment import dhondt, schepers, hare_niemeyer

def read_vals():
    '''
    Get test values for functional tests of methods from csv file
    '''

    test_vals = []

    with open('tests/tests.csv', newline='', encoding = 'utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader: 
            
            row_dict = {'method': row[0],
                        'votes': ast.literal_eval(row[1]),
                        'seats': int(row[2]),
                        'out_dist': ast.literal_eval(row[3]),
                        #'out_order': row[4],
                        #'out_table': row[5] # TODO handle + handle empties
                        }

            test_vals.append(row_dict)
    
    dhondt_tests = [x for x in test_vals if x.pop('method', None) == 'dhondt']
    schepers_tests = [x for x in test_vals if x.pop('method', None) == 'schepers']
    hare_tests = [x for x in test_vals if x.pop('method', None) == 'hare']

    return {'dhondt': dhondt_tests,
            'schepers': schepers_tests,
            'hare': hare_tests}
    
# Get test values
tests = read_vals()

# Begin tests
def test_hello_world():
    '''
    Ensure pytest is running correctly
    '''

    x, y = 1, 1
    assert x == y

sample_votes = {
    "SPD": 1000000,
    "CDU": 300000,
    "GRÜNE": 100000,
    "LINKE": 50000
}

sample_seats = 25

def test_dhondt_import():
    '''
    Ensure import of dhondt method is working
    ie. pytest is running in correct location (/src/)
    '''

    assert type(dhondt(sample_votes, sample_seats)) == dict

def test_schepers_import():

    assert type(schepers(sample_votes, sample_seats)) == dict

def test_hare_import():
    
    assert type(hare_niemeyer(sample_votes, sample_seats)) == dict

def test_dhondt_output_structure():

    output = dhondt(sample_votes, sample_seats, True)

    assert type(output) == dict
    assert len(output) == 3

def test_dhondt_dist_structure():
    
    output = dhondt(sample_votes, sample_seats, True)['distribution']

    assert type(output) == dict
    assert len(output) == 2
    assert type(output['seats']) == dict
    assert len(output['seats']) == len(sample_votes)
    assert type(output['is_ambiguous']) == bool

def test_dhondt_sequence_structure():
    
    output = dhondt(sample_votes, sample_seats, True)['assignment_sequence']

    assert type(output) == list
    assert len(output) == sample_seats
    assert all(type(x) == dict for x in output)
    assert all(type(x['is_ambiguous'] == bool) for x in output)

def test_dhondt_table_structure():
    
    output = dhondt(sample_votes, sample_seats, True)['table']

    assert type(output) == list
    assert len(output) == sample_seats
    assert all(type(x) == dict for x in output)
    assert all(len(x['seats']) == len(sample_votes) for x in output)

@pytest.mark.parametrize('params', tests['dhondt'])    
def test_dhondt_distribution(params):

    output = dhondt(params['votes'], params['seats'], False)

    assert output['distribution']['seats'] == params['out_dist']

# def test_dhondt_order(params):
#     pass

# def test_dhondt_table(params):
#     pass

# def test_schepers_distribution(params):
#     pass

# def test_schepers_order(params):
#     pass

# def test_schepers_table(params):
#     pass

# TODO tests:
# - Länge Tabelle 
# - Gesamtsitzzahl stimmt
# - Letzte Reihe Tabelle = Distribution


# def test_hare(v):
#     assert v + 1 > 100

