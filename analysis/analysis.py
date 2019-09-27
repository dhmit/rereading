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


def get_word_frequency_differences(student_data):
    """
    Looks over the data and compares responses from people who have read the text vs.
    people who have not read the text before this exercise
    :return: a list of word frequency differences, by increasing order of frequency differences
    """

    # Iterate through all data, and separate ids of students who have vs. have not read the text
    yes_id = []
    no_id = []

    for response in student_data:
        if 'Have you encountered this text before' in response['question'] \
                and 'This is an ad.' in response['context']:
            if 'yes' not in response['response'].lower():
                no_id.append(response['student_id'])
            else:
                yes_id.append(response['student_id'])

    # Iterate through all responses, store words and word frequencies of yes vs. no responses as
    # keys and values in 2 dictionaries

    yes_responses = dict()
    no_responses = dict()

    for element in student_data:
        if 'In one word' in element['question'] and 'This is an ad' in element['context']:
            response = element['response'].lower()
            if element['student_id'] in yes_id:
                if response in yes_responses:
                    yes_responses[response] += 1
                else:
                    yes_responses[response] = 1
            else:
                if response in no_responses:
                    no_responses[response] += 1
                else:
                    no_responses[response] = 1

    # Iterate through yes_responses and no_responses, store words and frequency differences as keys
    # and values of a dictionary
    diff_responses = dict()

    for word in yes_responses:
        if word in no_responses:
            diff_responses[word] = yes_responses[word] - no_responses[word]
        else:
            diff_responses[word] = yes_responses[word]
    for word in no_responses:
        if word not in yes_responses:
            diff_responses[word] = - no_responses[word]

    # Convert diff_responses from a dictionary to a list of tuples
    diff_responses_list = []
    for word in diff_responses:
        diff_responses_list.append((word, diff_responses[word]))

    # Order diff_responses and return ordered list
    ordered_responses = sorted(diff_responses_list, key=lambda x: x[1])
    return ordered_responses


def run_analysis():
    """
    Runs the analytical method on the reading data

    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    print(student_data[0]['question'])

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')


class TestAnalysisMethods(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """
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

    def test_compute_total_view_time(self):
        """
        Test that the total view time equals the expected values.
        """
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)

    def test_word_frequency_differences(self):
        """
        Test the word_frequency_differences function
        """

        word_frequency_differences = get_word_frequency_differences(self.test_student_data)
        expected = [('sad', -1)]
        self.assertEqual(word_frequency_differences, expected)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
