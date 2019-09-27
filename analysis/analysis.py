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




def compute_mean_reading_times(student_data):

    '''
    Analyze answer response times by computing a ratio of the response
    time of the first question to the response time of the second question;
    if multiple responses are recorded for the same question, add
    response times first.
    :param student_data: list, student response dicts
    :return: list, total number of participants, mean of first reading time, mean of second reading time
    '''
    # TODO: do something with student_data that's not just printing it!
    # print(student_data)

    total_first_response = 0
    total_second_response = 0
    total_participants = 0
    last_student_id = -1  # value not present in the data
    for line in student_data:
        context = line["context"]
        question = line["question"]
        student_id = line["student_id"]
        if question == "In one word, how does this text make you feel?":
            if context == 'This is an ad.':
                for duration in line["views"]:
                    total_first_response += duration
            elif context == "This is actually a short story.":
                for duration in line["views"]:
                    total_second_response += duration
        if student_id != last_student_id:
            total_participants += 1
            last_student_id = student_id

    mean_first_response = total_first_response / total_participants
    mean_second_response = total_second_response / total_participants
    return [total_participants, mean_first_response, mean_second_response]


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
    mean_data = compute_mean_reading_times(student_data)
    print(mean_data)


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


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
