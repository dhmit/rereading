"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from collections import Counter

from .analysis_helpers import (
    get_sentiments,
)

from .models import StudentReadingData, StudentSegmentData, SegmentQuestionResponse


def get_responses_for_question(all_responses, question):
    """
    For a certain question, returns the set of responses as a dictionary with keys
    being the response and values being the frequency.
    :param all_responses: QuerySet of all student responses
    :param question: string, question
    :return: dictionary mapping strings to integers
    """
    responses_frequency = Counter()
    response_list = []
    for student_response in all_responses:
        student_question = student_response.question.text
        student_answer = student_response.response.lower()
        if student_question == question:
            response_list.append(student_answer)
    for answer in response_list:
        responses_frequency[answer] += 1
    return responses_frequency


def most_common_response_by_question(all_responses, question):
    """
    Returns a list of the most common response(s) given a set of data, and question.
    :param all_responses: student response object
    :param question: string, question
    :return: list of strings
    """
    max_response = []
    response_dict = get_responses_for_question(all_responses, question)
    max_response_frequency = max(response_dict.values())
    for response in response_dict:
        if response_dict[response] == max_response_frequency:
            max_response.append(response)
    return max_response


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()
        self.segments = StudentSegmentData.objects.all()
        self.question_response = SegmentQuestionResponse.objects.all()

    def all_responses(self):
        """
        Given a list of student response dicts, returns the most common responses for each
        question.
        :return: list of dictionaries storing each question and most common answers
        """
        questions = []

        all_responses = []
        for reading in self.readings:
            if reading.question.text not in questions:
                questions.append(reading.question.text)

        return all_responses

    def total_and_median_view_time(self):
        """
        This function totals the overall view times and calculates the median view time per student
        :return: a tuple containing (total view time, median view time per student)
        """
        total_time = 0  # track the total reading time while looking at segment times
        ret_dict = {}
        in_dict = []  # prevent calling ret_dict.keys() repeatedly
        for segment in self.segments:
            # prime two variable to reduce calls to database
            view_time = segment.view_time
            reading_data = segment.reading_data
            # add the segment view times to a dictionary entry for each student reading session
            if reading_data not in in_dict:
                ret_dict[reading_data] = [view_time]
                in_dict.append(reading_data)
            else:
                ret_dict[reading_data].append(view_time)
            total_time += view_time
        student_total_view_time = []
        # do not cycle through something that doesn't exist
        if not ret_dict.values():
            median_view_time = 0
        else:
            for item in ret_dict.values():
                # total the segment view times for each student
                student_total_view_time.append(sum(item))
            # find the mean of the total reading time for each student
            median_view_time = statistics.median(student_total_view_time)
        ret_tuple = (round(total_time), round(median_view_time))
        return ret_tuple

    def get_number_of_unique_students(self):
        """
        This function finds the number of unique students who have participated in the study
        :return: an integer value
        """
        student_names = set()

        # go through all data in readings to get name of each user and add to set student_names
        for reading in self.readings:
            name = reading.student.name
            # convert to lower just in case some students forget to capitalize
            name = name.lower()
            # add name to set
            student_names.add(name)
        # return length of set (represents unique number of students)
        return len(student_names)

    def question_sentiment_analysis(self):
        """
        Uses database to create a list of sentiment scores for
        :return:
        """
        sentiments = get_sentiments()
        student_data = self.readings
        question_text = 'In one word'

        # Set up data for calculations
        num_scores = 0
        sentiment_sum = 0
        score_list = list()

        for reading in student_data:

            if question_text in reading.question.text:
                words = reading.response.lower().split()

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

    @staticmethod
    def transform_nested_dict_to_list(nested_dict):
        """
        Transforms a nested dictionary data structure into a flat array of tuples in the form
        (key1, key2, value).
        :param nested_dict: the map generated by
        students_using_relevant_words_by_c_question
        :return a list of tuples in the form (question, data)
        """
        flattened_list = []
        for key1, inner_keys in nested_dict.items():
            for key2, value in inner_keys.items():
                flattened_list.append((key1, key2, value))
        return flattened_list

    def students_using_relevant_words_by_question(self):
        """
        Return a list of tuples of the form (question, count), where count is
        the number of students who used relevant words in that question. This list
        is sorted by question.
        :return the return type explained in the function description
        """
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]

        question_count_map = {}

        for reading in self.readings:
            question = reading.question.text
            if question not in question_count_map:
                question_count_map[question] = {}

            if RereadingAnalysis.description_has_relevant_words(
                    reading.response,
                    relevant_words):
                question_count_map[question] += 1

        flattened_data = \
            RereadingAnalysis.transform_nested_dict_to_list(question_count_map)

        flattened_data.sort()
        return flattened_data

    def run_compute_reread_counts(self):
        """
        Runs the analysis on the data loaded from the CSV file by looking at the reread count for
        each question that the question was given in and
        prints it in a nice readable format.
        :return: the info wed like to put on js
        """
        questions = []
        student_data = self.responses[:]
        for response in student_data:
            if response.question.text not in questions:
                questions.append(response.question.text)

        compute_reread_counts_data = []

        for question in questions:
            compute_reread_counts_data.append(self.compute_reread_counts(
                question))

        return compute_reread_counts_data

    def compute_reread_counts(self, question):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :param question: string, question for which reread counts is collected
        :return: dictionary, each key in dictionary is the number of times the text was reread
        and value is the number of students who reread that many times
        """

        # Collects the reread count for every student id of the provided question
        raw_reread_counts = []
        for reading in self.readings:
            table_question = reading.question.text
            view_count = len(reading.get_parsed_views())

        # Tallies the raw reread counts into the dictionary to be returned
        organized_data = {}
        sum_of_views = 0
        student_count = 0

        for entry in raw_reread_counts:
            if entry in organized_data.keys():
                organized_data[entry] += 1
            elif len(raw_reread_counts) != 0:
                organized_data.update({entry: 1})
        keys_of_dictionary = organized_data.keys()
        for entry in keys_of_dictionary:
            sum_of_views += entry * organized_data[entry]
            student_count += organized_data[entry]

        if student_count == 0:
            return 0
        else:
            mean_reread_count = round((sum_of_views / student_count), 2)
            sum_of_views = 0
            final_student_count = student_count
            student_count = 0

    def frequency_words(self, question, minimum=1):
        """
        Compute the frequencies of words among all the responses. Not sensitive to case.
        Specifically for questions that ask the reader to give a list of words, or ask for one
        specific word (e.g. black or white.)

        Param: question is a string in exactly the same format as how it appears on the page
                minumum is the minimum frequency above which we include a word, default being any
                word that occurs more than once

        :return a list of tuples of words that appear more than once, and how often they occur,
        in order of their frequency
        """

        words_dict = {}

        for response in self.question_response:
            if response.question == question:
                lower_case_response = response.lower()
                wordlist = lower_case_response.split()
                for word in wordlist:
                    if words_dict.get(word, 0) == 0:
                        words_dict[word] = 1
                    else:
                        words_dict[word] += 1

        frequent_words = []  # list of tuples in the format (word, frequency)
        for word in words_dict:
            if words_dict[word] > minimum:
                frequent_words.append((word, words_dict[word]))
        frequent_words.sort(key=lambda x: x[1], reverse=True)
        return frequent_words
