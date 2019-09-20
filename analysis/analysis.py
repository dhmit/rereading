"""

Analysis.py - initial analyses for dhmit/rereading

"""
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
            row['views'] = eval(row['views'])  # eval the list
            out_data.append(row)
    return out_data


def compile_response(student_data, question):
    """
    Returns answers as a dictionary with context as the keys and another dictionary containing each
    response and their frequency as the value.
    :param student_data: list of OrderedDicts, set of responses
    :param question: string, question
    :return: dictionary
    """
    data = {}
    for elem in student_data:
        student_question = elem['question']
        student_response = elem['response']
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
    Returns the most common response
    :param student_data:
    :param question:
    :param context:
    :return:
    """
    max_freq = 0
    max_response = ''
    response_dict = compile_response(student_data, question)
    for response in response_dict[context]:
        if response_dict[context][response] > max_freq:
            max_freq = response_dict[context][response]
            max_response = response
    return max_response


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    print(common_response(student_data, "In one word, how does this text make you feel?", "This is an ad."))


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


def test_common_response(self):
    most_common_response = common_response(self.test_student_data, "In one word, how does this text make you feel?", "This is an ad.")
    self.assertEqual(most_common_response, "Happy")

    # check we don't crash on the defaults from the model!
    most_common_response = common_response(self.default_student_data, "In one word, how does this text make you feel?", "This is an ad.")
    self.assertEqual(most_common_response, '')


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests