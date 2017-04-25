#!/usr/bin/python3

"""
freqy.py

Calculates the frequency of ascii characters in a string, and compares it to
the frequency of characters in an English sentence.

https://en.wikipedia.org/wiki/Letter_frequency

According to Lewand, arranged from most to least common in appearance,
the letters are: 

    etaoinshrdlcumwfgypbvkjxqz 

Lewand's ordering differs slightly from others, such as Cornell University 
Math Explorer's Project, which produced a table after measuring 40,000 words.

In English, the space is slightly more frequent than the top letter (e) and 
the non-alphabetic characters (digits, punctuation, etc.) collectively occupy 
the fourth position (having already included the space) between t and a.
"""

##############################
# IMPORTS
##############################

from collections import Counter
from string import ascii_lowercase

##############################
# DEFINES
##############################

english_letter_freq = {'e': 12.70,
                       't': 9.06,
                       'a': 8.17,
                       'o': 7.51,
                       'i': 6.97,
                       'n': 6.75,
                       's': 6.33,
                       'h': 6.09,
                       'r': 5.99,
                       'd': 4.25,
                       'l': 4.03,
                       'c': 2.78,
                       'u': 2.76,
                       'm': 2.41,
                       'w': 2.36,
                       'f': 2.23,
                       'g': 2.02,
                       'y': 1.97,
                       'p': 1.93,
                       'b': 1.29,
                       'v': 0.98,
                       'k': 0.77,
                       'j': 0.15,
                       'x': 0.15,
                       'q': 0.10,
                       'z': 0.07}


##############################
# FUNCTIONS
##############################

def english_score(message):
    """Score a phrase based on frequency of English letters.
    
    Return the number of matches that the string in the message 
    parameter has when its letter frequency is compared to English 
    letter frequency. A "match" is how many of its six most frequency 
    and six least frequent letters is among the six most frequent and 
    six least frequent letters for English. 

    This function works better with the more input it has.
    """
    etaoin = 'etaoinshrdlcumwfgypbvkjxqz'
    letters = ascii_lowercase
    letter_count = Counter(x for x in message.lower() if x in letters)
    freq_order = ''.join(letter for letter, _ in letter_count.most_common())
    if freq_order:
        top = sum(1 for x in etaoin[:6] if x in freq_order[:6])
        bottom = sum(1 for x in etaoin[-6:] if x in freq_order[-6:])
    return top + bottom

def chi_squared(message):
    """Calculate the Chi-Squared statistic value.
    
    If the two distributions are identical, the chi-squared statistic is 0.
    If the two distributions are quite different, expect a higher number.

    X^2(C,E) = sum of (Ci - Ei)^2 / Ei, where i = A -> Z
    """
    c = Counter(message.lower())
    # Normalize the expected probabilities into counts
    e = { k: v * len(message) for k, v in english_letter_freq.items() }
    return sum(((c[i] - e[i])**2 / e[i]) for i in c if i in e)


##############################
# MAIN
##############################

if __name__ == "__main__":
    """Test the score of a block of English text."""

    test_string = """
    I want to start with a story from the Onion. Because really, 
    shouldn’t every talk start with a story from the Onion? 
    This is from earlier this year.
    
    The headline reads: “Nation Shudders At Large Block Of Uninterrupted Text.”
    
    “Unable to rest their eyes on a colorful photograph or boldface heading 
    that could be easily skimmed and forgotten, Americans collectively 
    recoiled Monday when confronted with a solid block of uninterrupted text.
    
    “Dumbfounded citizens from Maine to California gazed helplessly at the 
    frightening chunk of print, unsure of what to do next.
    
    “Without an illustration, chart, or embedded YouTube video to ease 
    them in, millions were frozen in place, terrified by the sight of one 
    long, unbroken string of English words.
    """

    score = english_score(test_string)
    print('For message:\n{}\nScore: {} (out of possible 12)'.format(test_string,
                                                                    score))
    chi_score = chi_squared(test_string)
    print('Chi Score: {}'.format(chi_score))
