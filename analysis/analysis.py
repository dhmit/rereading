"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
import unittest


def load_data_csv(csv_path: Path):
    """
    Takes the path to a csv file, reads it, and returns its
    content as a list of OrderedDicts
    :param Path csv_path: path to the CSV file
    :return: List[dict]
    """
    out_data = []
    with open(str(csv_path)) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row['views'] = literal_eval(row['views'])
            for header_name in ('id', 'student_id', 'scroll_ups'):
                row[header_name] = int(row[header_name])
            row = dict(row)
            out_data.append(row)
    return out_data


def compute_total_view_time(student_data):
    """
    Given a list of student response dicts,
    return the total time (across all users) spent reading the text
    :param student_data: list, student response dicts
    :return: float, the total time all users spent reading the text
    """
    total_view_time = 0
    for row in student_data:
        for view_time in row.get('views'):
            total_view_time += view_time
    return total_view_time


def run_analysis():
    """
    Takes in no parameters and initializes the analysis of the data
    :return: None
    """
    # csv_path = Path('data', 'test_data.csv')
    # csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    # student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    # total_view_time = compute_total_view_time(student_data)
    # print(f'The total view time of all students was {total_view_time}.')


def average_time(data):
    """
    Takes the data and finds the average time of all the times [views] in the data
    :param data: path to the CSV file
    :return: integer representing the average time overall
    """
    times = 0
    count = 0
    for dictionary in data:
        views = dictionary["views"]
        for view in views:
            times += view
            count += 1
    return times/count


def avg_time_student(data, student_id):
    """
    Takes the data and an id and computes the average time overall of the student
    :param student_id: integer, represents specific id number
    :param data:  path to the CSV file
    :return: integer: represents the average time of this id
    :return: None: when there is no data entries for this specific id
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_id = dictionary["student_id"]
        if dict_id == student_id:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times / count


def avg_time_cxt(data, question, context):
    """
    Takes the data, a question, and context and computes the average time of the
    views of this specific context and question
    :param question: String representing specific question
    :param context: String representing a specific context
    :param data:  path to the CSV file
    :return: integer: represents the average time of this question and context when it exists
    :return: None: when there is no data entries for this specific question and context
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_question = dictionary["question"]
        dict_context = dictionary["context"]
        if dict_question == question and dict_context == context:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times/count


def frequent_responses(freq_dict):
    """
    Takes in a dictionary with values that are frequency dictionaries
    Returns a dictionary showing the most frequent responses
    :param freq_dict: dictionary, A dictionary with tuples as keys and a dictionary as values.
    These values are actually dictionaries with strings as keys and numbers (the frequency) as
    values.
    :return: dictionary, A dictionary with tuples as keys and a dictionary as values.
    The values are dictionaries with different information about the most frequent responses
    such as a list of the most common responses as well as the number of times they occurred
    """
    output = {}
    for key in freq_dict:
        details = {}
        a_freq_dict = freq_dict[key]
        max_occurrences = 0
        max_list = []
        for word in a_freq_dict:
            occurrence = a_freq_dict[word]
            if occurrence > max_occurrences:
                max_occurrences = occurrence
                max_list = [word]
            elif occurrence == max_occurrences:
                max_list.append(word)
        details['most_frequent_words'] = max_list
        details['max_occurrences'] = max_occurrences
        output[key] = details
    return output


def word_freq_all(data):
    """
    :param data: list, A list of all of the data entries from the survey
    :return: dictionary, A dictionary with a tuple of the question and
    context as keys and with values of a dictionary with the words as
    keys and their frequencies as values
    """
    output = {}
    for entry in data:
        the_key = (entry["question"], entry["context"])
        if the_key not in output:
            output[the_key] = {}
        qc_dict = output[the_key]
        response = entry['response'].lower()
        if response not in qc_dict:
            qc_dict[response] = 1
        else:
            qc_dict[response] += 1
    return output


class TestAnalysisMethods(unittest.TestCase):
    def setUp(self):
        test_data_path = Path('data', 'test_data.csv')
        self.test_student_data = load_data_csv(test_data_path)
        self.default_student_data = [  # model default values
            {
                'id': 0,
                'question': '',
                'context': '',
                'response': '',
                'views': [],
                'student_id': 0,
                'scroll_ups': 0,
            }
        ]

    # def test_compute_total_view_time(self):
    #     total_view_time = compute_total_view_time(self.test_student_data)
    #     self.assertEqual(total_view_time, 6.385)
    #
    #     # check we don't crash on the defaults from the model!
    #     total_view_time = compute_total_view_time(self.default_student_data)
    #     self.assertEqual(total_view_time, 0)

    def test_average_time(self):
        average_view_time = average_time(self.test_student_data)
        self.assertAlmostEqual(average_view_time, 2.128333333333)

        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertAlmostEqual(total_view_time, 0)

    def test_word_freq_all(self):
        freq_dict = word_freq_all(self.test_student_data)
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {
            'sad': 1
        }
        self.assertEqual(freq_dict[specific_question_context], answer)

        freq_dict = word_freq_all(self.default_student_data)
        specific_question_context = ("", "")
        answer = {
            '': 1
        }
        self.assertEqual(freq_dict[specific_question_context], answer)

    def test_frequent_responses(self):
        most_frequent_responses = frequent_responses(word_freq_all(self.test_student_data))
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {
            'most_frequent_words': ['sad'],
            'max_occurrences': 1
        }
        self.assertEqual(most_frequent_responses[specific_question_context], answer)

        most_frequent_responses = frequent_responses(word_freq_all(self.default_student_data))
        specific_question_context = ("", "")
        answer = {
            'most_frequent_words': [''],
            'max_occurrences': 1
        }
        self.assertEqual(most_frequent_responses[specific_question_context], answer)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
