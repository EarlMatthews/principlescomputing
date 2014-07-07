"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = [item * hand.count(item) for item in hand]
    return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    if num_free_dice == 0:
        return score(held_dice)
    outcomes = list(range(1, num_die_sides+1))
    all_sequences = gen_all_sequences(outcomes, num_free_dice)
    length = len(all_sequences)
    total = 0.0
    for item in all_sequences:
        total += score(tuple(list(held_dice) + list(item)))
    return total / length


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    result = [[]]
    length = len(hand)
    for idx in range(length):
        ans = result
        result = []
        for item in ans:
            result.append(item)
            temp_list = list(item)
            temp_list.append(hand[idx])
            result.append(temp_list)
    result = [tuple(item) for item in result]
    return set(result)

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_subsets = gen_all_holds(list(set(hand)))
    max_value = None
    max_set = None
    for subset in all_subsets:
        held = _set_only_save(hand, subset)
        expection = expected_value(held, num_die_sides, len(hand) - len(held))
        if max_value is None:
            max_value = expection
            max_set = tuple(held)
        elif max_value < expection:
            max_value = expection
            max_set = tuple(held)
    return (max_value, max_set)

def _set_only_save(hand, subset):
    """
        get the complete list for subset
    """
    result = []
    for item in subset:
        result.extend([item] * hand.count(item))
    return result

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
