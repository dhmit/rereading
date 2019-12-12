"""

analysis_helpers.py - helper functions for rereading analyses

"""

import math
from pathlib import Path
from config.settings.base import PROJECT_ROOT


def max_abs(val1, val2):
    """
    Compares the absolute value of the values, returning the larger of the two values

    In the event of a tie, returns the absolute value

    :param val1: int, positive or negative
    :param val2: int, positive or negative
    :return: int, larger of val1 or val2 by absolute value
    """
    abs_1 = abs(val1)
    abs_2 = abs(val2)

    return max(abs_1, abs_2)


def get_sentiments_from_word(word_line):
    """
    Takes a line from the sentiment document and processes it to only return the word and
    sentiment score.

    :param word_line: str, line from the sentiment file
    :return: Tuple in the form (word, sentiment_score)
    """

    # This particular file starts lines with '#' for non-sentiment comments, so skip them
    if word_line[0] == '#' or word_line[0] == '\t':
        return None

    # All words use tabs to define the different parts of the data
    attributes = word_line.split('\t')

    # Pull out the word from the line
    data = attributes[4]
    data = data.split('#')
    new_word = data[0]
    positive_score = float(attributes[2])
    negative_score = -float(attributes[3])

    # Find the largest sentiment score for the word, and define negative sentiments
    # as negative values (if there's a tie, the sentiment is the absolute value)
    score = max_abs(positive_score, negative_score)

    return new_word, score


def get_sentiments() -> dict:
    """
    Returns a dictionary of sentiment scores, with the keys being the word and the values being
    their score

    :return: dict mapping words to their sentiment scores
    """
    sentiment_path = Path(PROJECT_ROOT, 'analysis', 'data', 'sentiments.txt')

    sentiments = dict()
    with open(sentiment_path, 'r') as file:

        for word in file:

            sentiment = get_sentiments_from_word(word)

            # Define the new_word and sentiment score only if it exists
            if not sentiment:
                continue

            new_word, score = sentiment

            # If the word is already defined, skip the current line if the sentiment is lower
            if new_word in sentiments:
                old_sentiment = sentiments[new_word]
                if max_abs(old_sentiment, score) == old_sentiment:
                    continue

            sentiments[new_word] = score

    return sentiments


def remove_outliers(data):
    """
    Given a list of times, calculates and removes outliers, which are the data points that
    are outside the interquartile range of the data
    :param data: list, reading times for a specific question
    :return: list, reading times for a specific question with outliers removed
    """
    data.sort()
    data_no_outliers = []
    quartile_one = data[math.trunc(len(data) * 0.25)]
    quartile_three = data[math.trunc(len(data) * 0.75)]
    interquartile_range = quartile_three - quartile_one
    lower_fence = quartile_one - (1.5 * interquartile_range)
    upper_fence = quartile_three + (1.5 * interquartile_range)

    for time in data:
        if (time >= lower_fence) and (time <= upper_fence):
            data_no_outliers.append(time)

    return data_no_outliers


def string_contains_words(input_string, target_words):
    """ Checks if a given input_string contains any of the words in the list of target_words """
    if not target_words:
        return True

    input_string_lowercase = input_string.lower()

    for word in target_words:
        if word.lower() in input_string_lowercase:
            return True

    return False
