import math


def stableford(
        impacts: int,
        par: int,
        index: int,
        handicap: int,
        hcp: int,
):
    handicap_index = round(handicap * hcp / 100)
    edge_list = [0 for _ in range(18)]
    i = 0
    while i < handicap_index:
        if i < 18:
            edge_list[i] += 1

        else:
            edge_list[i % 18] += 1
        i += 1
    delta: int = impacts - par - edge_list[index - 1]
    rules = {
        2: 0,
        1: 1,
        0: 2,
        -1: 3,
        -2: 4,
        -3: 5,
    }
    if delta > 2:
        points = 0
    elif delta <= -3:
        points = 5
    else:
        points = rules[delta]
    return points


def stroke_play_nett(total_impacts: int, handicap: int, hcp: int):
    return total_impacts - math.ceil(handicap * hcp / 100)
