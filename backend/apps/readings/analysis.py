"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from pathlib import Path

from config.settings.base import PROJECT_ROOT
from .models import StudentResponse


def compare_abs_value(val1, val2):
    """
    Compares the absolute value of the values, returning the larger of the two values

    In the event of a tie, returns 0

    :param val1: int, positive or negative
    :param val2: int, positive or negative
    :return: int, larger of val1 or val2 by absolute value
    """
    abs_1 = abs(val1)
    abs_2 = abs(val2)

    if abs_1 > abs_2:
        return val1
    if abs_2 > abs_1:
        return val2
    else:
        return 0


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
    # as negative values (if there's a tie, the sentiment is 0)
    score = compare_abs_value(positive_score, negative_score)

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
                if compare_abs_value(old_sentiment, score) == old_sentiment:
                    continue

            sentiments[new_word] = score

    return sentiments


class RereadingAnalysis:
    """
    This class loads all student responses from the db,
    and implements analysis methods on these responses.

    We use .serializers.AnalysisSerializer to send these analysis results to the
    frontend for display.
    """

    def __init__(self):
        """ On initialization, we load all of the StudentResponses from the db """
        self.responses = StudentResponse.objects.all()

    def total_view_time(self):
        """
        Queries the db for all StudentResponses,
        and computes total time (across all users) spent reading the text

        :return: float, the total time all users spent reading the text
        """
        total_view_time = 0
        for response in self.responses:
            for view_time in response.get_parsed_views():
                total_view_time += view_time
        return total_view_time

    def question_sentiment_analysis(self):

        """
        Uses database to create a list of sentiment scores for
        :return:
        """

        sentiments = get_sentiments()
        student_data = self.responses
        question_text = 'In one word'

        # Set up data for calculations
        num_scores = 0
        sentiment_sum = 0
        score_list = list()

        for response in student_data:

            if question_text in response.question.text:
                words = response.response.lower().split()

                # Find the sentiment score for each word, and add it to our data
                for word in words:
                    # Ignore the word if it's not in the sentiment dictionary
                    if word in sentiments:
                        sentiment_sum += sentiments[word]
                        num_scores += 1
                        score_list.append(sentiments[word])

        average = sentiment_sum / num_scores
        standard_dev = statistics.stdev(score_list)

        return average, standard_dev

    def compute_median_view_time(self):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in self.responses:
            for view_time in row.get('views'):
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time
