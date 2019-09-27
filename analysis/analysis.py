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


def compile_response(student_data, question):
    """
    Returns answers as a dictionary with context as the keys and another dictionary containing each
    response and their frequency as the value.
    :param student_data: list of OrderedDicts, set of responses
    :param question: string, question
    :return: dictionary mapping strings to integers
    """
    data = {}
    for elem in student_data:
        student_question = elem['question']
        student_response = elem['response'].lower()
        question_context = elem['context']
        if student_question == question:
            if question_context not in data:
                data[question_context] = {student_response: 1}
            else:
                if student_response in data[question_context]:
                    data[question_context][student_response] += 1
                else:
                    data[question_context][student_response] = 1
    return data


def common_response(student_data, question, context):
    """
    Returns a list of the most common response(s) given a set of data, a question, and a context.
    :param student_data: list of OrderedDicts, student response data
    :param question: string, question
    :param context: string, context
    :return: list of strings
    """
    max_response = []
    response_dict = compile_response(student_data, question)
    responses_by_context = response_dict[context]
    for response in responses_by_context:
        if responses_by_context[response] == max(responses_by_context.values()):
            max_response.append(response)
    return max_response


def run_analysis():
    """
    Runs the analytical method on the reading data

    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')
    print(compile_response(student_data, "In one word, how does this text make you feel?"))
    print(common_response(student_data, "In one word, how does this text make you feel?",
                                        "This is an ad."))


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

    def test_common_response(self):
        """
        Tests to make sure the function runs properly by checking against known data sets.
        :return: None
        """
        most_common_response = common_response(self.test_student_data,
                                               "In one word, how does this text make you feel?",
                                               "This is an ad.")
        self.assertEqual(most_common_response, ['sad'])

        # check we don't crash on the defaults from the model!
        most_common_response = common_response(self.default_student_data, '', '')
        self.assertEqual(most_common_response, [''])


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
