#!/usr/bin/python3

"""
isenglish.py

Determine if a word or phrase is English.
"""

class IsEnglish():
    """IsEnglish class with English word and phrase matching."""

    def __init__(self, threshold=3, filename='./english-words/words.txt'):
        """Create wordset and a suitable phrase threshold."""
        with open(filename) as word_file:
            self.wordset = set(word.strip().lower() for word in word_file)
        self.threshold = threshold

    def is_english_word(self, word):
        """Determine if a word is a known English word."""
        return word.lower() in self.wordset

    def is_english_phrase(self, phrase):
        """If string has more than 3 English words, likely a phrase."""
        english_word_count = 0
        for word in phrase.lower().split(' '):
            if self.is_english_word(word):
                english_word_count += 1
        return english_word_count >= self.threshold
