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
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    response_groups = get_response_groups_frequencies(student_data)
    show_response_groups(response_groups)
    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')

#     My thought is that we can compare the word frequencies we return for each response group to
#     find the similarities and differences between contexts (not enough data atm for this to be
#     significant, but the insights would become more interesting as response # increases)

def show_response_groups(response_groups):
    """
    Given response_group dictionary, prints/shows the dictionaries so that they
    can be compared in the terminal

    Input: response groups, keys are four dicts (one for each response group) mapping words
    to frequencies within that response group
    Returns: None
    """
    for group_name in response_groups:
        print("Word frequencies for", group_name, ":", response_groups[group_name], "\n")


def get_response_groups_frequencies(student_data: list):
    """"
    Given student_data,
    Returns dict mapping response groups to frequency dicts, which themselves
    map response words to frequencies for that response group
    Response groups based on single vs. multiple views and ad vs. short story
    context to the "In one word, how does this text make you feel?" question
    :param student_data
    :return: dict, keys are four dicts (one for each response group) mapping words
    to frequencies within that response group
    """
    people_with_multiple_views = []
    people_with_one_view = []

    response_groups = {
        "Single view responses to ad context": [],
        "Single view responses to short story context": [],
        "Multiple view responses to ad context": [],
        "Multiple view responses to short story context": []
    }

    for person_response in student_data:
        if len(person_response['views']) == 1:
            people_with_one_view.append(person_response)
        else:
            people_with_multiple_views.append(person_response)

    for person in people_with_one_view:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                response_groups["Single view responses to short story context"].append\
                    (person['response'].lower())
            else:
                response_groups["Single view responses to ad context"].append\
                    (person['response'].lower())

    for person in people_with_multiple_views:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                response_groups["Multiple view responses to short story context"].append\
                    (person['response'].lower())
            else:
                response_groups["Multiple view responses to ad context"].\
                    append(person['response'].lower())

    for group_name in response_groups:
        freq_dict = find_word_frequency(response_groups[group_name])
        response_groups[group_name] = freq_dict
    return response_groups


def find_word_frequency(response_list):
    freq = {}
    for word in response_list:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


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
        sample_csv_path = Path('data', 'rereading_data_2019-09-13.csv')
        self.student_data = load_data_csv(sample_csv_path)

    def test_compute_total_view_time(self):
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)

    def test_get_response_group_frequencies(self):
        response_groups = get_response_groups_frequencies(self.student_data)
        expected = {
                    'Single view responses to ad context': {'sad': 2, 'bored': 1,
                                                            'annoyed': 2, 'fine': 1,
                                                            'melancholic': 1, 'suspicious': 1,
                                                            'speculative': 1, 'depressed': 1,
                                                            'confused': 1},
                    'Single view responses to short story context': {
                                                                        'sad': 8, 'enticed': 1,
                                                                        'ok': 1,'inyrigu': 1,
                                                                        'interested': 2,
                                                                        'surprised': 1,
                                                                        'concerned': 1, 'helped': 1,
                                                                        'depressed': 2,
                                                                        'sad/curious': 1,
                                                                        'intrigued': 1,
                                                                        'confused': 1,
                                                                        'puzzled': 1},
                    'Multiple view responses to ad context': {'targeted': 1, 'confused': 3,
                                                              'informed': 2, 'weird': 1,
                                                              'comfortable': 1, 'melancholy': 2,
                                                              'sad': 2, 'concerned': 1,
                                                              'uncomfortable': 1, 'curious': 1,
                                                              'disappointed': 1, 'indifferent': 1,
                                                              'fine': 1, 'neutral': 1},
                    'Multiple view responses to short story context': {'somber': 1,
                                                                       'mysterious': 1,
                                                                       'curious': 1, 'sad': 1,
                                                                       'interested': 1,
                                                                       'underwhelmed': 1,
                                                                       'melancholy': 1,
                                                                       'sadder': 1}
                    }
        self.assertEqual(expected, response_groups)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests

