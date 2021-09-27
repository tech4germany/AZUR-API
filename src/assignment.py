import numpy as np
from typing import Mapping, Tuple, Dict, List

def dhondt(votes: Mapping[str, int], seats_available: int, return_table: bool = False) -> Tuple[Dict[str, int], List[str], Dict]: #TODO update output typing
    """ Applies D'Hondt Method for calculating the distribution of all seats available based on the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :param return_table: whether or not the function should also return a table with each distribution up to the given one
    :return: A Tuple containing (1) the final distribution, (2) the sequence in which these seats where distributed, (3) optionally 
    the table of distributions from one seat up to the final one as a dict with (a) the headers and (b) the values of the table
    """
    # TODO update docstring

    return assign_iterative(votes, seats_available, 1, return_table)

def schepers(votes: Mapping[str, int], seats_available: int, return_table: bool) -> Tuple[Dict[str, int], List[str], Dict]: #TODO update output typing
    """ Applies saint-lague/schepers Method for calculating the distribution of all seats available based on
    the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :param return_table: whether or not the function should also return a table with each distribution up to the given one
    :return: A Tuple containing (1) the final distribution, (2) the sequence in which these seats where distributed, (3) optionally 
    the table of distributions from one seat up to the final one as a dict with (a) the headers and (b) the values of the table
    """
    # TODO update docstring 

    return assign_iterative(votes, seats_available, 0.5, return_table)

def assign_iterative(votes: Mapping[str, int], seats_available: int, div_starting_val: int = 1, return_table: bool = False) -> Tuple[Dict[str, int], List[str], Dict]: #TODO update output typing
    """ Performs the recursive assignment loop underlying dhondt and schepers methods
    :param votes: the number of votes each party/faction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :param div_starting_val: the initial value of the divisor which is kept for each faction
    :param return_table: whether or not the function should also return a table with each distribution up to the given one
    :return: A Tuple containing 
    (1) a dict with (a) the final distribution and (b) parties which could get the last seat if there is an ambiguity
    (2) a list with the sequence in which these seats where distributed, where ambiguous elements are themselves a list of possible parties,
    (3) optionally the table of distributions from one seat up to the final one as a dict with 
        (a) the headers of the table in table_headers 
        (b) the values of the table in table_values, with the previous row repeated in cases of ambiguity, 
        (c) a table with all zeroes except 1's for parties which could receive an ambiguous seat in rows with ambiguity
    """


    divs = {key: div_starting_val for (key, val) in votes.items()}
    ambigs = {key: 0 for (key,val) in votes.items()} # Returns ambiguities, if any, in final assignment
    assgs = []
    if return_table: 
        table = np.zeros(shape = (seats_available, len(votes)))
        ambig_table = np.zeros(shape = (seats_available, len(votes)))

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
            if return_table: table[i] = list(divs.values())

        else: # Ambiguity
            
            # Find names of ambiguous parties
            party_keys = [x for i, x in enumerate(divided_vals.keys()) if i in seat_goes_to]

            # Find number of ambig. seats
            n_ambiguous_seats = len(party_keys) - 1

            # Add list of tied parties to assignment order
            #assgs.append(party_keys)
            for p in range(n_ambiguous_seats + 1): assgs.append(party_keys) 
            
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
                
                # Replace as many rows in table with previous one as seats are ambiguous
                # And add ambiguities in ambig table
                for r in range(n_ambiguous_seats): 
                    try:
                        
                        table[i+r] = table[i-1]

                        # TODO should this instead only be in the first ambiguous row?
                        # TODO should number always be 1, or total ambiguous seats?
                        for val in seat_goes_to: ambig_table[i+r,val] = 1 

                    except IndexError:
                        # No worries, was just out of bounds of table, nothing needs updating
                        pass
                        
                # Add row to table where ambiguity is resolved, ie. each ambig. party gets an extra seat
                try:
                    table[i+n_ambiguous_seats] = list(divs.values())
                except IndexError:
                    # No worries, was just out of bounds of table, nothing needs updating
                    pass
                 
    # Format final party seat numbers and ambiguities
    party_names = list(votes.keys())
    seats_final = {key: int(val-div_starting_val) for (key, val) in divs.items()} # convert from divisors to seats
    seats = {'seats': seats_final,
             'ambiguities': ambigs}
    
    if return_table: 

        table = (table-div_starting_val).astype(int).tolist() # vals in table are divisors, not seats, this fixes that
        ambig_table = ambig_table.astype(int).tolist()

        table = {'table_headers': party_names,
                 'table_values': table,
                 'table_ambiguities': ambig_table}

        return seats, assgs, table
    
    return seats, assgs

def hare_niemeyer(votes: Mapping[str, int], seats_available: int) -> Dict[str, int]:
    """ Applies Hare/Niemeyer Method for calculating the distribution of all seats available based on
    the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: The final distribution of seats (Hare/Niemeyer produces no ordering of these seats)
    """

    votes_vals = np.array(list(votes.values()))
    props = seats_available * votes_vals / np.sum(votes_vals)
    # print(props)

    fulls = np.floor(props)
    # print(fulls)
    
    rest = props - fulls
    # print(rest)

    seats_left = seats_available - np.sum(fulls)
    # print(seats_left)
    
    ranks = rest.argsort().argsort()
    # print(ranks)
    
    gets_another_seat = np.where(ranks >= len(ranks) - seats_left, 1, 0)
    # print(gets_another_seat)
    
    seats = fulls + gets_another_seat
    # do not use numpy parse to int32 as that type is not understood by json parse (for api)
    seats = map(int, seats)

    # TODO unsafe die ergebnisse einfach am ende mit den input keys zu zippen?
    seats_labeled = dict(zip(votes.keys(), seats))
    
    return seats_labeled
    
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
    print(str(dhondt(votes, seats)))

    print('Schepers')
    print(str(schepers(votes, seats)))

    print('Hare-Niemeyer')
    print(str(hare_niemeyer(votes, seats)))
