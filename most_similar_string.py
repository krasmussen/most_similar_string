#!/usr/bin/env python


# Lets cheat and dynamically build regex conditionals :P

# (a)(?(1)(b)?)(?(2)(c)?)(?(3)(d)?)
# this should match abcde but not acde
# This allows us to do this:
# [''.join(i) for i in re.findall('(a)(?(1)(b)?)(?(2)(c)?)(?(3)(d)?)', 'abcdadababcd')]
# giving us:
# ['abcd', 'a', 'ab', 'abcd']
# if we don't match we get an empty list

import random
import re


def find_substrings(string1, string2, min_len=1):
    '''
    Finds substrings of string1 that exist in string 2 of length min_len or greater
    '''
    # For each possible different starting character of string1
    # convert string1 starting char to end of string into our regex query
    regex_strings = []
    for gen in [string1[index:] for index in range(0, len(string1))]:
        # First match is formatted different than all the rest so we grab that now
        first_match = gen[:min_len]
        # If our first match is less than our minimum we can stop looking
        if len(first_match) < min_len:
            break
        # Start building our regex string from our first match
        regex_string = '({})'.format(first_match)
        # Future matches are all of the same format and should just be 1 char each
        remainder_substr = gen[min_len:]
        for char_index in range(0, len(remainder_substr)):
            iteration = char_index + 1
            # This should build us (?(1)(b)?)
            # then add (?(2)(c)?) to it and so on from our example above
            regex_string += '(?({})({})?)'.format(iteration, remainder_substr[char_index])
        regex_strings.append(regex_string)
    # Attempt to find substrings
    substrings = []
    for regex_string in regex_strings:
        regex_string_results = []
        skip_these = []
        regex_results = re.findall(regex_string, string2)
        for regex_result in regex_results:
            result = ''.join(regex_result)
            regex_string_results.append(result)
        # Avoid adding overlapping results to the substrings list
        # We have to do this in seperate calls because we can
        # have multiple matches that are substrings of eachother
        for result in regex_string_results:
            for substring in substrings:
                if result in substring:
                    skip_these.append(result)
        for result in regex_string_results:
            if result not in skip_these:
                substrings.append(result)
    return substrings


def most_similar_string(s, canidates, min_len=3):
    weights = dict()
    weights['substr_len_match_multiplier'] = 10
    scores = {}
    for canidate in canidates:
        scores[canidate] = 0
        # score up substrings
        substrings = find_substrings(s, canidate, min_len=min_len)
        for substring in substrings:
            substring_points = len(substring) * weights['substr_len_match_multiplier']
            scores[canidate] += substring_points
    final_scores = sorted(scores.items(), key=lambda tup: tup[1])
    print(final_scores)
    winners = []
    high_score = None
    while final_scores:
        potential_winner, score = final_scores.pop()
        if high_score is None:
            high_score = score
        if score == high_score:
            winners.append(potential_winner)
    if len(winners) > 1:
        return random.choice(winners)
    if len(winners) == 1:
        return winners.pop()


# Test data
# most_similar_string('abc123', ['bc231', 'zaf2131', '123', 'zbc120'])
# This should return 'zbc120'
# find_substrings('abcdefg', 'zabcdabcedefg', min_len=3)
# This should return ['abcd', 'abc', 'defg']
