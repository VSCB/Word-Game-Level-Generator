import itertools
import random
import pandas as pd
from nltk.corpus import words, brown
from nltk import FreqDist

def filter_common_words(nltk_word_list, word_candidates, freq_dist):
    """Filter words that are common based on nltk dataset and sort them by frequency."""
    valid_words = [word for word in word_candidates if word in nltk_word_list and is_alphabetic(word)]
    valid_words.sort(key=lambda w: -freq_dist[w])  # Sort by decreasing frequency
    return valid_words

def is_alphabetic(word):
    """Return True if the word consists only of alphabetic characters."""
    return word.isalpha()

# Generate word frequency distribution from Brown corpus
word_freq = brown.words()
freq_dist = FreqDist(word_freq)

# Load nltk words
word_list = set(filter(is_alphabetic, words.words()))
five_letter_words_nltk = [word for word in word_list if len(word) == 5]
five_letter_words_nltk.sort(key=lambda w: -freq_dist[w])  # Sort by decreasing frequency

def generate_word_list():
    if not five_letter_words_nltk:
        return None

    base_word = five_letter_words_nltk.pop(0)  # Get and remove the most common word from the list

    three_letter_combinations = set([''.join(comb) for comb in itertools.permutations(base_word, 3)])
    four_letter_combinations = set([''.join(comb) for comb in itertools.permutations(base_word, 4)])
    five_letter_combinations = set([''.join(comb) for comb in itertools.permutations(base_word, 5)])

    three_letter_words = filter_common_words(word_list, three_letter_combinations, freq_dist)
    four_letter_words = filter_common_words(word_list, four_letter_combinations, freq_dist)
    five_letter_words = filter_common_words(word_list, five_letter_combinations, freq_dist)

    return {
        "base_word": base_word,
        "3-letter words": ', '.join(three_letter_words),
        "4-letter words": ', '.join(four_letter_words),
        "5-letter words": ', '.join(five_letter_words)
    }

def main():
    data = []
    for _ in range(2000):
        row = generate_word_list()
        if row:
            data.append(row)
    df = pd.DataFrame(data)
    df.to_excel("five_letter_word_lists.xlsx", index=False)

if __name__ == "__main__":
    main()
