from typing import Mapping, Tuple, Dict, List, Union

from assignment import assign
import os

def compare(params_1: Dict, params_2: Dict, num_seats: int, return_table: bool = True ) -> Dict[str, Union[Dict, List[Dict]]]:

    params_1['num_of_seats'], params_1['return_table'] = num_seats, True
    params_2['num_of_seats'], params_2['return_table'] = num_seats, True
    out_1 = assign(params_1)
    out_2 = assign(params_2)

    comparison = {}

    comparison['distribution'] = compare_instance(out_1['distribution'], out_2['distribution'])

    if return_table:

        comparison['table'] = [compare_instance(out_1['table'][x], out_2['table'][x]) for x in range(num_seats)]
    
    if 'assignment_sequence' in out_1.keys() and 'assignment_sequence' in out_2.keys():
        
        comparison['assignment_sequence'] = [compare_instance(out_1['assignment_sequence'][x],
                                                              out_2['assignment_sequence'][x],
                                                              "assignment_A",
                                                              "assignment_B")
                                             for x in range(num_seats)]

    return comparison

def compare_instance(dist1, dist2, key1 = "dist_A", key2 = "dist_B"):

    is_identical = False

    try:
        if dist1 == dist2:
            is_identical = True
            dist2 = None
    except:
        print('An error occurred.')
        return None

    return {
            key1:  dist1,
            key2:  dist2,
            "is_identical": is_identical
            }

def compare_demo():

    dist_A =  {
        "votes": {
                "SPD": 1,
                "CDU": 1,
                "GRÜNE": 1,
                "LINKE": 1
        },
        "method": "schepers"
    }

    dist_B =  {
        "votes": {
                "SPD": 1,
                "CDU": 1,
                "GRÜNE": 1,
                "LINKE": 2
        },
        "method": "hare"
    }

    seats = 25

    return compare(dist_A, dist_B, seats)