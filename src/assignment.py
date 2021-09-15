import numpy as np
from typing import Mapping, Tuple, Dict, List

def dhondt(votes: Mapping[str, int], seats_available: int, return_table: bool) -> Tuple[Dict[str, int], List[str], List[List[int]]]: #TODO list of lists typing? 
    """ Applies D'Hondt Method for calculating the distribution of all seats available based on the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: A Tuple containing (1) the final distribution and (2) the sequence in which these seats where distributed
    """
    
    return assign_iterative(votes, seats_available, 1, return_table)


def schepers(votes: Mapping[str, int], seats_available: int, return_table: bool) -> Tuple[Dict[str, int], List[str]]:
    """ Applies saint-lague/schepers Method for calculating the distribution of all seats available based on
    the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: A Tuple containing (1) the final distribution and (2) the sequence in which these seats where distributed
    """

    return assign_iterative(votes, seats_available, 0.5, return_table)

def assign_iterative(votes, seats_available, div_starting_val = 1, return_table = False): #TODO typing
    """ Performs the recursive assignment loop underlying dhondt and schepers methods
    :param votes: the number of votes each party/faction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :param div_starting_val: the initial value of the divisor which is kept for each faction
    """

    divs = {key: div_starting_val for (key, val) in votes.items()}
    assgs = []
    if return_table: table = np.zeros(shape = (seats_available, len(votes)))

    for i in range(seats_available):
        
        # TODO werden diese Zwischenergebnisse nicht irgendwie gerundet?
        vals = {key: val/divs[key] for (key, val) in votes.items()}

        # TODO how do we deal with multiple max values?!
        seat_goes_to = max(vals, key=vals.get)  # get key for party that gets the seat
        
        assgs.append(seat_goes_to)
        divs[seat_goes_to] += 1
        
        if return_table: table[i] = list(divs.values())
    
    seats = {key: int(val-div_starting_val) for (key, val) in divs.items()} # convert from divisors to seats
    
    if return_table: 
        table = (table-div_starting_val).astype(int).tolist()# vals in table are divisors, not seats, this fixes that
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