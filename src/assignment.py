import numpy as np
from typing import Mapping, Tuple, Dict, List, Union

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
        output = hare_niemeyer(votes, num_seats, return_table)
    
    return output

def dhondt(votes: Mapping[str, int], seats_available: int, return_table: bool = False) -> Dict[str, Union[Dict, List[Dict]]]:
    """
    Applies the d'Hondt Method for calculating the distribution of all seats available based on
    the proportions of votes. See assign_iterative docstring for parameter and return documentation.
    """
    # TODO update docstring for new output

    return assign_iterative(votes, seats_available, 1, return_table)

def schepers(votes: Mapping[str, int], seats_available: int, return_table: bool = False) -> Dict[str, Union[Dict, List[Dict]]]:
    """ 
    Applies the Saint-Lague/Schepers Method for calculating the distribution of all seats available based on
    the proportions of votes. See assign_iterative docstring for parameter and return documentation.
    """

    return assign_iterative(votes, seats_available, 0.5, return_table)

def assign_iterative(votes: Mapping[str, int], seats_available: int, div_starting_val: int = 1, return_table: bool = False) -> Dict[str, Union[Dict, List[Dict]]]:
    """ 
    Performs the recursive assignment loop underlying dhondt and schepers methods
    :param votes: the number of votes each party/faction received in a mapping of format {party_name: seats}
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :param div_starting_val: the initial value of the divisor which is kept for each faction (1 for d'Hondt, 0.5 for Schepers)
    :param return_table: whether or not the function should also return a table with each distribution up to the given one
    :return: A dict containing
        (1) 'distribution', a dict containing
            (a) 'seats', a dict of format {party_name: n_seats}, where n_seats is an int if unambiguous and a list of possible values if ambiguous
            (b) 'is_ambiguous', a bool signalling if there are ambiguities 
        (2) 'assignment_sequence', a list of dicts which each contain
            (a) 'seat_goes_to', the party (as str) or list of parties (if ambiguous) the seat goes to
            (b) 'is_ambiguous', a bool signalling if there are ambiguities
        (3) optionally 'table', a list containing dicts, each of the same format as (1), from 1 up to seats_available seats
    """

    # Initialize required tracking vars
    divs = {key: div_starting_val for (key, val) in votes.items()}
    ambigs = {key: 0 for (key,val) in votes.items()}
    assgs = []
    if return_table: table, ambig_table = [], []
    skip_iter = 0 # An n-way ambiguity handles n rows at once. This variable tracks how many iters are then skipped 

    for i in range(seats_available):
        
        if skip_iter > 0: # Iteration handled by previous one bc of ambiguity; skip iteration
            skip_iter -= 1
            continue 

        divided_vals = {key: val/divs[key] for (key, val) in votes.items()}

        # Find party/parties that get next seat
        seat_goes_to = [i for i, x in enumerate(divided_vals.values()) if x == max(divided_vals.values())]
        
        if len(seat_goes_to) == 1: # No ambiguity

            party_key = max(divided_vals, key=divided_vals.get)  # get key for party that gets the seat
            assgs.append(party_key)
            divs[party_key] += 1
            if return_table: 
                table.append(divs.copy())
                ambig_table.append({key: 0 for key in votes})

        else: # Ambiguity
            
            # Find names of ambiguous parties
            party_keys = [x for i, x in enumerate(divided_vals.keys()) if i in seat_goes_to]

            # Find number of ambig. seats
            n_ambiguous_seats = len(party_keys) - 1

            # Add list of tied parties to assignment order
            #assgs.append(party_keys)
            for p in range(n_ambiguous_seats + 1): 
                if len(assgs) < seats_available:
                    assgs.append(party_keys) 
            
            # Skip the next n iterations of the loop
            skip_iter = n_ambiguous_seats

            # Skipping those iterations may end the loop, in that case add ambiguity to seats output
            # TODO This is screaming off-by-one-error? Test
            if i + skip_iter >= seats_available: 
                for party in party_keys: ambigs[party] = 1
            else:
                # Otherwise increase all ambiguous parties' divisors by 1
                for party in party_keys: divs[party] += 1 
            
            if return_table:
                
                # TODO mem errors through too much appending possible?
                # Add as many rows in table as previous one as seats are ambiguous
                # And add ambiguities in ambig table
                for r in range(n_ambiguous_seats): 
                    if len(table) <= seats_available:
                        
                        if len(table) > 0: table.append(table[-1].copy())
                        else: table.append({key: div_starting_val for key in votes}) # Case where first row is ambiguous

                        # TODO should this instead only be in the first ambiguous row?
                        # TODO should number always be 1, or total ambiguous seats?
                        ambig_table.append({key: 1 if key in party_keys else 0 for key in votes})
                    
                # Add row to table where ambiguity is resolved, ie. each ambig. party gets an extra seat
                if len(table) <= seats_available: 
                    table.append(divs.copy())
                    ambig_table.append({key: 0 for key in votes})

    ### Format Output
    out = {}

    # Format final distribution
    seats_corrected = {key: int(divs[key]-div_starting_val) for key in divs} # convert from divisors to seats
    seats_with_ambigs, is_ambiguous = add_ambiguity(seats_corrected, ambigs) # add ambiguities to seats dict if relevant
    out['distribution'] = {'seats': seats_with_ambigs, 'is_ambiguous': is_ambiguous}
    
    # Format assignment sequence
    assgs_final = [{'seat_goes_to': x, 'is_ambiguous': (type(x) == list)} for x in assgs]
    out['assignment_sequence'] = assgs_final

    # Format table
    if return_table: 

        final_table = []
        table = [{key: int(row[key] - div_starting_val) for key in row} for row in table] # convert divisors to seats

        for row in range(seats_available):
            row_seats, row_ambiguity = add_ambiguity(table[row], ambig_table[row])
            final_table.append({'seats': row_seats, 'is_ambiguous': row_ambiguity})
        
        out['table'] = final_table
    
    return out

def add_ambiguity(seats: Dict[str, int], ambigs: Dict[str, int]) -> Dict[str, Union[int, list]]:
    """
    A helper function that takes a seat distribution and a number of ambiguous seats (each as dict) and returns 
    a dict of the seats per party, as int if no ambig, else as a list of possible seat nr options
    :param seats: a dict of format {party_name: n_seats}
    :param ambigs: a dict of format {party_name: n_ambig_seats}
    :return: a dict of format {party_name: Union[n_seats, [seats_opt_1, seats_opt_2]]}
    """

    party_names = seats.keys()
    ambig_dict = {x: seats[x] if ambigs[x] == 0 else [seats[x], seats[x]+ambigs[x]] for x in party_names}
    is_ambiguous = sum(ambigs.values()) > 0

    return ambig_dict, is_ambiguous

def hare_niemeyer(votes: Mapping[str, int], seats_available: int, return_table: bool = False) -> Dict[str, Union[Dict, List[Dict]]]:

    out = {}

    if return_table:
        out['table'] = [single_distribution_hare_niemeyer(votes, x) for x in range(1,seats_available+1)]
        out['distribution'] = out['table'][-1]
    else:
        out['distribution'] = single_distribution_hare_niemeyer(votes, seats_available)

    return out

def single_distribution_hare_niemeyer(votes: Mapping[str, int], seats_available: int) -> Dict[str, int]:
    """ 
    Applies the Hare/Niemeyer Method for calculating the distribution of all seats available based on
    the proportions of votes
    :param votes: the number of votes that each party/fraction received in a mapping of format {party_name: seats}
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: The final distribution of seats (Hare/Niemeyer produces no ordering of these seats) in the format
    {'distribution': 'seats': {...}, is_ambiguous: bool}
    """

    votes_vals = np.array(list(votes.values()))
    props = seats_available * votes_vals / np.sum(votes_vals)
    fulls = np.floor(props)
    rest = props - fulls
    seats_left = seats_available - np.sum(fulls)

    # Get ranks
    _, v = np.unique(rest, return_inverse=True)
    ranks = (np.cumsum(np.bincount(v)) - 1)[v]

    gets_another_seat = np.where(ranks >= len(ranks) - seats_left, 1, 0)

    if sum(gets_another_seat) <= seats_left: # No Ambiguity
        
        is_ambiguous = False
        seats = fulls + gets_another_seat

        seats_labeled = dict(zip(votes.keys(), seats))
        seats_labeled = {key: int(val) for key, val in seats_labeled.items()}

    else: # Ambiguity

        is_ambiguous = True

        # Find rank which is ambiguous
        ambig_rank = min(np.where(ranks >= len(ranks) - seats_left, ranks, np.inf))

        # Find seats that are definitely assigned despite ambiguity
        safe_gets_another_seat = np.where(ranks > ambig_rank, 1, 0)

        # Find parties that may get another seat
        ambigs = np.where(ranks == ambig_rank, 1, 0)

        seats = dict(zip(votes.keys(), fulls + safe_gets_another_seat))
        ambigs = dict(zip(votes.keys(), ambigs))

        seats = {key: int(val) for key, val in seats.items()}
        ambigs = {key: int(val) for key, val in ambigs.items()}

        seats_labeled, _ = add_ambiguity(seats,ambigs)
    
    return {'seats': seats_labeled, 'is_ambiguous': is_ambiguous}
 
def demo():

    votes = {
        "SPD": 1000000,
        "CDU": 300000,
        "GRÜNE": 100000,
        "LINKE": 50000
    }
    seats = 25

    print(f'Votes: {votes}, Seats: {seats}')
    print("D'hondt")
    print(str(dhondt(votes, seats, True)))

    print('Schepers')
    print(str(schepers(votes, seats, True)))

    print('Hare-Niemeyer')
    print(hare_niemeyer(votes, seats, True))
