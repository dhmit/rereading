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
    Runs the analytical method on the reading data

    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')
    print(count_revists(student_data))


def count_revists(data):
    """
    Returns the average number of revisits per question

    :param data: list, student response dict
    :return: dict, Key = question, string. Value = average number of revisits, float.
    """

    results = {}

    for entry in data:
        if results.get(entry['question']):
            results[entry['question']][0] += 1
            results[entry['question']][1] += len(entry['views'])
        else:  # create a key with starting values
            results[entry['question']] = [1, len(entry['views'])]

    for question in results:
        results[question] = round(results[question][1] / results[question][0], 2)

    return results


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

    def test_count_revisits(self):
        """
        Test that the average number of revisits equals the expected values.
        """
        revisits_per_question = count_revists(self.test_student_data)
        self.assertEqual(revisits_per_question['In one word, how does this text make you feel?'], 1)
        self.assertEqual(revisits_per_question['In three words or fewer, what is this text '
                                               'about?'], 0.5)
        self.assertEqual(revisits_per_question['Have you encountered this text before?'], 0)

        # check we don't crash on the defaults
        revisits_per_question = count_revists(self.default_student_data)
        self.assertEqual(revisits_per_question[''], 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
