"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import itertools
import statistics
import math
from collections import Counter
from pathlib import Path

from config.settings.base import PROJECT_ROOT
from .models import StudentResponsePrototype, ContextPrototype, QuestionPrototype


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


def get_responses_for_question(all_responses, question, context):
    """
    For a certain question and context, returns the set of responses as a dictionary with keys
    being the response and values being the frequency.
    :param all_responses: QuerySet of all student responses
    :param question: string, question
    :param context: string, context
    :return: dictionary mapping strings to integers
    """
    responses_frequency = Counter()
    response_list = []
    for student_response in all_responses:
        student_question = student_response.question.text
        student_context = student_response.context.text
        student_answer = student_response.response.lower()
        if student_question == question and student_context == context:
            response_list.append(student_answer)
    for answer in response_list:
        responses_frequency[answer] += 1
    return responses_frequency


def most_common_response_by_question_and_context(all_responses, question, context):
    """
    Returns a list of the most common response(s) given a set of data, a question,
    and a context.
    :param all_responses: student response object
    :param question: string, question
    :param context: string, context
    :return: list of strings
    """
    max_response = []
    response_dict = get_responses_for_question(all_responses, question, context)
    max_response_frequency = max(response_dict.values())
    for response in response_dict:
        if response_dict[response] == max_response_frequency:
            max_response.append(response)
    return max_response


class RereadingAnalysis:
    """
    This class loads all student responses from the db,
    and implements analysis methods on these responses.

    We use .serializers.AnalysisSerializer to send these analysis results to the
    frontend for display.
    """

    def __init__(self):
        """ On initialization, we load all of the StudentResponses from the db """
        self.responses = StudentResponsePrototype.objects.all()

        """ Retrieve all possible questions and turn it into a list """
        list_of_dict_of_questions = QuestionPrototype.objects.values('text')
        merged_dicts = {}
        for key in list_of_dict_of_questions[0].keys():
            merged_dicts[key] = list(dict[key] for dict in list_of_dict_of_questions)
        self.questions = merged_dicts.get('text')

        """ Retrieve all possible contexts, and turn it into a list"""
        list_of_dict_of_contexts = ContextPrototype.objects.values('text')
        merged_dicts = {}
        for key in list_of_dict_of_contexts[0].keys():
            merged_dicts[key] = list(dict[key] for dict in list_of_dict_of_contexts)
        self.contexts = merged_dicts.get('text')

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
        return round(total_view_time)

    def all_responses(self):
        """
        Given a list of student response dicts, returns the most common responses for each
        question and in each context.
        :return: list of dictionaries storing each question, context, and most common answers
        """
        questions = []
        contexts = []
        all_responses = []
        for response in self.responses:
            if response.question.text not in questions:
                questions.append(response.question.text)
            if response.context.text not in contexts:
                contexts.append(response.context.text)
        for question in questions:
            for context in contexts:
                answers = most_common_response_by_question_and_context(
                    self.responses,
                    question,
                    context,
                )
                response_by_question_and_context = {
                    'question': question,
                    'context': context,
                    'answers': answers
                }
                all_responses.append(response_by_question_and_context)

        return all_responses

    def frequency_feelings(self):
        """
        Compute the frequencies of all the responses. Not sensitive to case.
        :return a list of tuples of words that appear more than once, and how often they occur,
        in order of their frequency
        """
        feelings = {}
        for response in self.responses:
            if response.question.text == "In one word, how does this text make you feel?":
                lower_case_word = response.response.lower()
                if feelings.get(lower_case_word, 0) == 0:
                    feelings[lower_case_word] = 1
                else:
                    feelings[lower_case_word] += 1

        frequent_words = []  # list of tuples in the format (frequency, word)
        for word in feelings:
            if feelings[word] > 1:
                frequent_words.append((word, feelings[word]))
        frequent_words.sort(key=lambda x: x[1], reverse=True)
        return frequent_words

    def context_vs_read_time(self):
        """
        Compares mean view times of all contexts
        :return a dictionary where the context is the key and the mean view time for that context
        is the value
        """
        all_contexts = ContextPrototype.objects.all()
        total_contexts_view_times = {context.text: {
            "total_view_time": 0,
            "count": 0
            }
                                     for context in all_contexts}

        for response in self.responses:
            context = response.context.text
            total_contexts_view_times[context]["total_view_time"] += \
                sum(response.get_parsed_views())
            total_contexts_view_times[context]["count"] += 1

        # For each context in total_contexts_view_time, calculate the average view time
        average_context_view_times = {context:
                                      total_contexts_view_times[context]["total_view_time"] /
                                      total_contexts_view_times[context]["count"]
                                      for context in total_contexts_view_times}
        return average_context_view_times

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

    @property
    def run_mean_reading_analysis_for_questions(self):
        """
        Runs the analysis on the data loaded from the CSV file by looking at the average
        read time for each question and the context that the question was given in and
        prints it in a nice readable format.
        :return: the info wed like to put on js
        """

        questions = []
        contexts = []
        student_data = self.responses[:]
        for response in student_data:
            if response.question.text not in questions:
                questions.append(response.question.text)
            if response.context.text not in contexts:
                contexts.append(response.context.text)

        mean_reading_time_results_data = []

        for question in questions:
            for context in contexts:
                mean_reading_time_results_data.append(self.mean_reading_time_for_a_question(
                    question, context))

        return mean_reading_time_results_data

    def mean_reading_time_for_a_question(self, question, context):
        """
        Given the student response dicts, computes the mean read time for a
        specific question (given by its keyword) and the context in which it was asked.
        Returns the question, context, mean read time, and number of people who read.
        :param question: string, to determine which question was being asked
        :param context: string, what the reader thought the reading was
        :return: tuple, in order of the question asked (full question), the context,
        the mean read time, and the number of people who read it
        """
        mean_time = 0
        number_of_readers = 0
        question_count = 0
        reading_time = []
        total_question_view_time = 0
        student_data = self.responses[:]
        for response in student_data:
            if question != response.question.text or context != response.context.text:
                continue
            if response.get_parsed_views():
                number_of_readers += 1
            for view_time in response.get_parsed_views():
                reading_time.append(view_time)

        if reading_time:
            reading_time = remove_outliers(reading_time)

        view_time = 0
        while view_time < len(reading_time):
            question_count += 1
            total_question_view_time += reading_time[view_time]
            view_time += 1

        if reading_time:
            mean_time = round(total_question_view_time / len(reading_time), 2)

        return [question, context, mean_time, number_of_readers]

    def compute_median_view_time(self):
        """
        Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in self.responses:
            for view_time in row.get_parsed_views():
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time

    def compute_reread_counts(self, question, context):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :param question: string, question for which reread counts is collected
        :param context: string, context for which reread counts is collected
        :return: dictionary, each key in dictionary is the number of times the text was reread
        and value is the number of students who reread that many times
        """

        # Checks that the question and context are not blank
        if question == '' or context == '':
            return {}

        # Collects the reread count for every student id of the provided context and question
        raw_reread_counts = []
        for response in self.responses:
            table_context = response.context.text
            table_question = response.question.text
            view_count = len(response.get_parsed_views())
            if context in table_context:
                if question in table_question:
                    raw_reread_counts.append(view_count)

        # Tallies the raw reread counts into the dictionary to be returned
        organized_data = {}
        for entry in raw_reread_counts:
            if entry in organized_data.keys():
                organized_data[entry] += 1
            elif len(raw_reread_counts) != 0:
                organized_data.update({entry: 1})

        return organized_data

    @property
    def reread_counts(self):
        questions_and_contexts = [self.questions, self.contexts]

        question_context_combinations = []
        for element in itertools.product(*questions_and_contexts):
            question_context_combinations.append(element)

        counter = 0
        results = {}
        for question_context_combination in question_context_combinations:
            question, context = question_context_combination
            if results.get(question):
                results[question][context] = self.compute_reread_counts(question, context)
            else:  # Initialize question with a dictionary
                results[question] = {}
                results[question][context] = self.compute_reread_counts(question, context)

            counter += 1

        # return self.compute_reread_counts(questions[0], context)
        return results
