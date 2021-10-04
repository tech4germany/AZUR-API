import pytest
import csv
import ast

from assignment import dhondt, schepers, hare_niemeyer

def read_vals():
    '''
    Get test values for functional tests of methods from csv file
    '''

    test_vals = []

    with open('tests/tests.csv', encoding = 'utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter = '|')
        for row in reader: 
            
            row_dict = {}
            lit_eval_rows = {'votes': 1,
                             'out_distribution': 3,
                             'out_sequence': 4,
                             'out_table': 5}

            for var_name, input_pos in lit_eval_rows.items():
                try:
                    row_dict[var_name] = ast.literal_eval(row[input_pos])
                except:
                    row_dict[var_name] = None

            row_dict['method'] = row[0]
            row_dict['num_of_seats'] = int(row[2])

            test_vals.append(row_dict)

    dhondt_tests = [x for x in test_vals if x['method'] == 'dhondt']
    schepers_tests = [x for x in test_vals if x['method'] == 'schepers']
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

@pytest.mark.parametrize('params', tests['dhondt'])   
def test_dhondt_output_structure(params):

    output = dhondt(params['votes'], params['num_of_seats'], True)

    assert type(output) == dict
    assert len(output) == 3

@pytest.mark.parametrize('params', tests['dhondt'])    
def test_dhondt_dist_structure(params):
    
    output = dhondt(params['votes'], params['num_of_seats'])['distribution']

    assert type(output) == dict
    assert len(output) == 2
    assert type(output['seats']) == dict
    assert len(output['seats']) == len(params['votes'])
    assert type(output['is_ambiguous']) == bool

@pytest.mark.parametrize('params', tests['dhondt'])    
def test_dhondt_sequence_structure(params):
    
    output = dhondt(params['votes'], params['num_of_seats'])['assignment_sequence']

    assert type(output) == list
    assert len(output) == params['num_of_seats']
    assert all(type(x) == dict for x in output)
    assert all(type(x['is_ambiguous'] == bool) for x in output)

@pytest.mark.parametrize('params', tests['dhondt'])    
def test_dhondt_table_structure(params):
    
    output = dhondt(params['votes'], params['num_of_seats'], True)['table']

    assert type(output) == list
    assert len(output) == params['num_of_seats']
    assert all(type(x) == dict for x in output)
    assert all(len(x['seats']) == len(params['votes']) for x in output)

@pytest.mark.parametrize('params', tests['dhondt'])    
def test_dhondt_distribution_values(params):

    if params['out_distribution'] is not None:
        output = dhondt(params['votes'], params['num_of_seats'])
        assert output['distribution'] == params['out_distribution']
    
    assert True

@pytest.mark.parametrize('params', tests['dhondt'])  
def test_dhondt_sequence_values(params):
    
    if params['out_sequence'] is not None:
        output = dhondt(params['votes'], params['num_of_seats'])
        assert output['assignment_sequence'] == params['out_sequence']

    assert True

@pytest.mark.parametrize('params', tests['dhondt'])  
def test_dhondt_table_values(params):

    if params['out_table'] is not None:
        output = dhondt(params['votes'], params['num_of_seats'], True)
        
        for item_to_check in params['out_table']:
            assert output['table'][item_to_check['row'] - 1] == item_to_check['distribution']
    
        assert output['distribution'] == output['table'][-1]

    assert True

@pytest.mark.parametrize('params', tests['schepers'])   
def test_schepers_output_structure(params):

    output = schepers(params['votes'], params['num_of_seats'], True)

    assert type(output) == dict
    assert len(output) == 3

@pytest.mark.parametrize('params', tests['schepers'])    
def test_schepers_dist_structure(params):
    
    output = schepers(params['votes'], params['num_of_seats'])['distribution']

    assert type(output) == dict
    assert len(output) == 2
    assert type(output['seats']) == dict
    assert len(output['seats']) == len(params['votes'])
    assert type(output['is_ambiguous']) == bool

@pytest.mark.parametrize('params', tests['schepers'])    
def test_schepers_sequence_structure(params):
    
    output = schepers(params['votes'], params['num_of_seats'])['assignment_sequence']

    assert type(output) == list
    assert len(output) == params['num_of_seats']
    assert all(type(x) == dict for x in output)
    assert all(type(x['is_ambiguous'] == bool) for x in output)

@pytest.mark.parametrize('params', tests['schepers'])    
def test_schepers_table_structure(params):
    
    output = schepers(params['votes'], params['num_of_seats'], True)['table']

    assert type(output) == list 
    assert len(output) == params['num_of_seats']
    assert all(type(x) == dict for x in output)
    assert all(len(x['seats']) == len(params['votes']) for x in output)

@pytest.mark.parametrize('params', tests['schepers'])    
def test_schepers_distribution_values(params):

    if params['out_distribution'] is not None:
        output = schepers(params['votes'], params['num_of_seats'])
        assert output['distribution'] == params['out_distribution']
    
    assert True

@pytest.mark.parametrize('params', tests['schepers'])  
def test_schepers_sequence_values(params):
    
    if params['out_sequence'] is not None:
        output = schepers(params['votes'], params['num_of_seats'])
        assert output['assignment_sequence'] == params['out_sequence']

    assert True

@pytest.mark.parametrize('params', tests['schepers'])  
def test_schepers_table_values(params):

    if params['out_table'] is not None:
        output = schepers(params['votes'], params['num_of_seats'], True)
        
        for item_to_check in params['out_table']:
            assert output['table'][item_to_check['row'] - 1] == item_to_check['distribution']
    
        assert output['distribution'] == output['table'][-1]
    
    assert True

@pytest.mark.parametrize('params', tests['hare'])
def test_hare_structure(params):

    output = hare_niemeyer(params['votes'], params['num_of_seats'])

    assert type(output) == dict
    assert len(output) == 1
    assert len(output['distribution']) == len(params['votes'])

@pytest.mark.parametrize('params', tests['hare'])
def test_hare_distribution_values(params):

    output = hare_niemeyer(params['votes'], params['num_of_seats'])

    assert output['distribution'] == params['out_distribution']

# TODO tests:
# - Länge Tabelle 
# - Gesamtsitzzahl stimmt
# - Letzte Reihe Tabelle = Distribution


# def test_hare(v):
#     assert v + 1 > 100

