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
    # TODO: do something with student_data that's not just printing it!
    # print(student_data)
    people_with_multiple_views = []
    people_with_one_view = []

    # one word answers for each question separated out by view count (one vs multiple)
    single_view_responses_to_c1 = []
    single_view_responses_to_c2 = []
    multiple_view_responses_to_c1 = []
    multiple_view_responses_to_c2 = []

    for person_response in student_data:
        # filter out responses from people who didn't go back
        # this sorting doesn't work. We need to find a way to sort people with 1, +1 views...
        if len(person_response['views']) == 1:
            people_with_one_view.append(person_response)
        else:
            people_with_multiple_views.append(person_response)

    for person in people_with_one_view:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                single_view_responses_to_c2.append(person['response'].lower())
            else:
                single_view_responses_to_c1.append(person['response'].lower())

    for person in people_with_multiple_views:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                multiple_view_responses_to_c2.append(person['response'].lower())
            else:
                multiple_view_responses_to_c1.append(person['response'].lower())

    for i in (single_view_responses_to_c1, single_view_responses_to_c2,
              multiple_view_responses_to_c1, multiple_view_responses_to_c2):
        print(find_word_frequency(i))
        print("\n")

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')


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

    def test_compute_total_view_time(self):
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
