import numpy as np


def dhondt(votes, seats_available):
    
    divs = np.array([1] * len(votes))
    seats = np.array([0] * len(votes))
    assgs = []
    
    for i in range(seats_available):
        
        vals = votes / divs
        seat_goes_to = np.argmax(vals)
        
        assgs.append(seat_goes_to + 1)
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
