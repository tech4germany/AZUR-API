import numpy as np
from typing import Mapping, Tuple, Dict, List


def dhondt(votes: Mapping[str, int], seats_available: int) -> Tuple[Dict[str, int], List[str]]:
    """ Applies D'Hondt Method for calculating the distribution of all seats available based on the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: A Tuple containing (1) the final distribution and (2) the sequence in which these seats where distributed
    """
    
    divs = {key: 1 for (key, val) in votes.items()}  # copy dict keys but init all divisors with 1
    seats = {key: 0 for (key, val) in votes.items()}  # copy dict keys but init all seat counters with 0

    assgs = []
    
    for i in range(seats_available):
        # TODO werden diese Zwischenergebnisse nicht irgendwie gerundet?
        vals = {key: val/divs[key] for (key, val) in votes.items()}

        # TODO how do we deal with multiple max values?!
        seat_goes_to = max(vals, key=vals.get)  # get key for party that gets the seat

        assgs.append(seat_goes_to)
        seats[seat_goes_to] += 1
        divs[seat_goes_to] += 1

    return seats, assgs


def schepers(votes: Mapping[str, int], seats_available: int) -> Tuple[Dict[str, int], List[str]]:
    """ Applies saint-lague/schepers Method for calculating the distribution of all seats available based on
    the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: A Tuple containing (1) the final distribution and (2) the sequence in which these seats where distributed
    """

    divs = {key: 0.5 for (key, val) in votes.items()}
    seats = {key: 0 for (key, val) in votes.items()}
    assgs = []

    # TODO remove code duplication between schepers and d'hondt in that loop
    for i in range(seats_available):
        
        vals = {key: val/divs[key] for (key, val) in votes.items()}

        # TODO how do we deal with multiple max values?!
        seat_goes_to = max(vals, key=vals.get)  # get key for party that gets the seat

        assgs.append(seat_goes_to)
        seats[seat_goes_to] += 1
        divs[seat_goes_to] += 1
        
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
    seats = seats.astype(int)

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