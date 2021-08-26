import numpy as np
from typing import Mapping, Tuple


def dhondt(votes: Mapping[str, int], seats_available: int) -> Tuple[dict, list]:
    """ Applies D'Hondt Method for calculating the distirbution of all seats available based on the proportions of votes
    :param votes: the number of votes that each party/fraction received
    :param seats_available: the total number of seats (or minutes, or rooms...) available for distribution
    :return: A Tuple containing (1) the final distribution and (2) the sequence in which these seats where distributed
    """
    
    divs = {key: 1 for (key, val) in votes.items()}  # copy dict keys but init all divisors with 1
    seats =  {key: 0 for (key, val) in votes.items()}  # copy dict keys but init all seat counters with 0

    assgs = []
    
    for i in range(seats_available):
        # TODO werden diese Zwischenergebnisse nicht irgendwie gerundet?
        vals = {key: val/divs[key] for (key, val) in votes.items()}

        # TODO how do we deal with multiple max values?!
        seat_goes_to = max(vals, key=vals.get) # get key for party that gets the seat

        assgs.append(seat_goes_to)
        seats[seat_goes_to] += 1
        divs[seat_goes_to] += 1

    return seats, assgs


def schepers(votes, seats_available):
    
    divs = np.array([0.5] * len(votes))
    seats = np.array([0] * len(votes))
    assgs = []
    
    for i in range(seats_available):
        
        vals = votes / divs
        seat_goes_to = np.argmax(vals)
        
        assgs.append(seat_goes_to + 1)
        seats[seat_goes_to] += 1
        divs[seat_goes_to] += 1
        
    return seats, assgs


def hare_niemeyer(votes, seats_available):
    
    props = seats_available * votes / np.sum(votes)
    # print(props)
    
    fulls = np.floor(props)
    # print(fulls)
    
    rest = props - fulls
    
    seats_left = seats_available - np.sum(fulls)
    # print(seats_left)
    
    ranks = rest.argsort().argsort()
    # print(ranks)
    
    gets_another_seat = np.where(ranks >= len(ranks) - seats_left, 1, 0)
    # print(gets_another_seat)
    
    seats = fulls + gets_another_seat
    seats = seats.astype(int)
    
    return seats


def demo():
    votes = np.array([1000000, 300000, 100000, 50000])
    seats = 25

    print('Votes: {}, Seats: {}'.format(votes, seats))
    print("D'hondt")
    print(str(dhondt(votes, seats)))

    print('Schepers')
    print(str(schepers(votes, seats)))

    print('Hare-Niemeyer')
    print(str(hare_niemeyer(votes, seats)))


if __name__ == "__main__":
    print(dhondt(
        {
            "cdu": 1000000,
            "grüne": 300000,
            "spd": 100000,
            "dielinke": 50000
         },
        25
    ))