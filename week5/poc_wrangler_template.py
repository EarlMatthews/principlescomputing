"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) == 1 or len(list1) == 0:
        return list1
    previous = list1[0]
    result = [previous]
    for each_element in list1[1:]:
        if each_element == previous:
            continue
        else:
            previous = each_element
            result.append(previous)
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    index1 = 0
    index2 = 0
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] == list2[index2]:
            result.append(list1[index1])
            index1 += 1
            index2 += 1
        elif list1[index1] < list2[index2]:
            index1 += 1
        else:
            index2 += 1
    result = remove_duplicates(result)
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    result = []
    index1 = index2 = 0
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] <= list2[index2]:
            result.append(list1[index1])
            index1 += 1
        else:
            result.append(list2[index2])
            index2 += 1
    if index1 < len(list1):
        result.extend(list1[index1:])
    if index2 < len(list2):
        result.extend(list2[index2:])
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    length = len(list1)
    if length == 1 or length == 0:
        return list1
    half = length / 2
    left_part = merge_sort(list1[:half])
    right_part = merge_sort(list1[half:])
    result = merge(left_part, right_part)
    return result

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [word]
    if len(word) == 1:
        return ["", word]
    rest_result = gen_all_strings(word[1:])
    first_char = word[0]
    result = []
    for each_word in rest_result:
        result.extend(__insert_char_into_word(first_char, each_word))
    result.extend(rest_result)
    return result

def __insert_char_into_word(input_char, word):
    """
        set the input_char into each position 
        of the word.
        This function return a list of all the possible word.
    """
    if len(word) == 0:
        return [input_char]
    result = []
    # range paraments should be length plus 1
    for index in range(len(word)+1):
        combined = word[:index] + input_char + word[index:]
        result.append(combined)
    return result

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    dict_file = urllib2.urlopen(url)
    result = []
    for each_line in dict_file.readlines():
        result.append(each_line[:-1])
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game

run()
    
    
