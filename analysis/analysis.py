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
    """compares average viewtimes, given different context (ad vs story)"""
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    average_times = context_vs_read_time(student_data)

    #print(student_data)

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')

def context_vs_read_time(student_data):
    ad_sum = 0
    ad_count = 0
    story_sum = 0
    story_count = 0


    for dict in student_data:
        if dict['context'] == "This is an ad.":
            if not len(dict["views"])  == 0:
                for view in dict["views"]:
                    ad_sum = ad_sum + view
            ad_count += 1
        elif dict["context"] == "This is actually a short story.":
            if not len(dict["views"])  == 0:
                for view in dict["views"]:
                    story_sum = story_sum + view
            story_count += 1

    average_ad_view = ad_sum / ad_count
    average_story_view = story_sum / story_count

    return average_ad_view, average_story_view


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

    def test_compute_total_view_time(self):
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
