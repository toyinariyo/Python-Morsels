from collections import Counter


def count_words(string):
    words = string.lower().split()
    return Counter(words)
