"""
    test as a shell
"""
from Yahtzee import gen_all_sequences


outcomes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

all_set = gen_all_sequences(outcomes, 5)

def filter_set(seq):
    pass

def is_des(seq):
    for idx in range(1, len(seq)):
        if seq[idx] <= seq[idx-1]:
            continue
        else:
            return False
    return True

def is_asc(seq):
    for idx in range(1, len(seq)):
        if seq[idx] >= seq[idx-1]:
            continue
        else:
            return False
    return True

size = len(all_set)
total = 0.0
for seq in all_set:
    if is_asc(seq) or is_des(seq):
        total += 1
print total / size


print "sb"