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


def compute_median_view_time(student_data):
    """
     Given a list of student response dicts,
    return the median time (across all users) spent reading the text

    :param student_data: list, student response dicts
    :return: float, median amount of time users spend reading the text
    """
    list_of_times = []
    for row in student_data:
        for view_time in row.get('views'):
            list_of_times.append(view_time)
    list_of_times.sort()
    if len(list_of_times) == 0:
        median_view_time = 0
    else:
        median_view_time = list_of_times[int(len(list_of_times) / 2)]
    return median_view_time


def run_analysis():
    """
    Runs the analytical method on the reading data

    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    median_view_time = compute_median_view_time(student_data)
    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')
    print(f'The median view time of all students was {median_view_time}.')


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

    def test_compute_median_view_time(self):
        median_view_time = compute_median_view_time(self.test_student_data)
        self.assertEqual(median_view_time, 2.319)

        # check we don't crash on the defaults from the model!
        median_view_time = compute_median_view_time(self.default_student_data)
        self.assertEqual(median_view_time, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
