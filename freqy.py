#!/usr/bin/python3

"""
char_freq.py

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

etaoin = 'etaoinshrdlcumwfgypbvkjxqz'
letters = 'abcdefghijklmnopqrstuvwxyz'

def get_letter_count(message):
    """ Returns a dictionary with keys of single letters and values of 
        the count on how many times they appear in the message parameter.
    """
    letter_count = {letter:0 for letter in letters}
    for letter in message.lower():
        if letter in letters:
            letter_count[letter] += 1
    return letter_count

def get_freq_order(message):
    """ Returns a string of the alphabet letters arranged in order of 
        most frequently occuring in the message parameter. 
    """
    # First, get a dictionary of each letter and its frequency count
    letter_to_freq = get_letter_count(message)

    # Second, make a dictionary of each frequency count to each letter(s) 
    # with that frequency
    freq_to_letter = {}
    for letter in letters:
        if letter_to_freq[letter] not in freq_to_letter:
            freq_to_letter[letter_to_freq[letter]] = [letter]
        else:
            freq_to_letter[letter_to_freq[letter]].append(letter)

    # Third, put each list of letter sin reverse "ETAOIN" order, and 
    # then conver it to a string
    for freq in freq_to_letter:
        freq_to_letter[freq].sort(key=etaoin.find, reverse=True)
        freq_to_letter[freq] = ''.join(freq_to_letter[freq])

    # Fourth, convert the freq_to_letter dictionary to a list of tuple 
    # pairs (key, value) then sort
    freq_pairs = list(freq_to_letter.items())
    freq_pairs.sort(key=lambda char: char[0], reverse=True)

    # Fifth, now that the letters are ordered by frequency, extra all 
    # the letters for final string
    return ''.join(char for freq, char in freq_pairs)

def english_freq_match_score(message):
    """ Return the number of matches that the string in the message 
        parameter has when its letter frequency is compared to English 
        letter frequency. A "match" is how many of its six most frequency 
        and six least frequent letters is among the six most frequent and 
        six least frequent letters for English. 
    """
    freq_order = get_freq_order(message)
    match_score = 0
    if freq_order is not None:
        # Find matches for top six
        for common_letter in etaoin[:6]:
            if common_letter in freq_order[:6]:
                match_score += 1
        # Find matches for least common six
        for uncommon_letter in etaoin[-6:]:
            if uncommon_letter in freq_order [-6:]:
                match_score += 1

    return match_score

if __name__ == "__main__":
    " Test the score of a random string "
    test_string = """This is a random test string for the ages """
    score = english_freq_match_score(test_string)
    print('The score for message:\n{}\nis: {}'.format(test_string, score))
