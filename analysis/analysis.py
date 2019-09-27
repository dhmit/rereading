"""

Analysis.py - initial analyses for dhmit/rereading

"""
import csv
import unittest
from ast import literal_eval
from pathlib import Path


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


def compute_reread_counts(student_data):
    """"
    Given a list of student response dicts,
    return a matrix containing the number of times students had to reread
    the text based on the context and question.
    :param student_data: list, student response dicts
    :return: matrix, rows being context & question, columns having tallies
    of how many students reread 1 time, 2 times, etc. Returning list of 6 lists. Each individual
    list has 6 elements.
    """

    compilation_of_contexts_and_question = {
        "q1_ad": [],
        "q1_short": [],
        "q2_ad": [],
        "q2_short": [],
        "q3_ad": [],
        "q3_short": []
    }

    # For each row in the student data, the loop sorts the number of reread counts into 6 lists
    # for the six different questions
    for row in student_data:
        # "encountered" signifies the "Have you encountered this text before?" question
        # "one" signifies the "In one word, how does this make you feel?" question
        # "three" signifies the "In three words or fewer, what is this text about?" question
        # "ad" signifies the "This is an ad." context
        # "short" signifies the "This is a short story." context
        view_count = len(row['views'])
        question = row['question']
        context = row['context']
        if "ad" in context:
            if "encountered" in question:
                compilation_of_contexts_and_question["q1_ad"].append(view_count)
            elif "one" in question:
                compilation_of_contexts_and_question["q2_ad"].append(view_count)
            elif "three" in question:
                compilation_of_contexts_and_question["q3_ad"].append(view_count)

        if "short" in context:
            if "encountered" in question:
                compilation_of_contexts_and_question["q1_short"].append(view_count)
            elif "one" in question:
                compilation_of_contexts_and_question["q2_short"].append(view_count)
            elif "three" in question:
                compilation_of_contexts_and_question["q3_short"].append(view_count)

    # Compiles all of the question reread count lists into one single list

    # For each question and context of question, this loop counts the number of responses that
    # had 0, 1, 2, 3, and 5 or above reread counts. This data is added to a list.
    organized_data = {
        "q1_ad": {},
        "q1_short": {},
        "q2_ad": {},
        "q2_short": {},
        "q3_ad": {},
        "q3_short": {}
    }
    for question_and_context in compilation_of_contexts_and_question:
        for entry in compilation_of_contexts_and_question[question_and_context]:
            if entry in organized_data.keys():
                organized_data[question_and_context][entry] += 1
            else:
                organized_data[question_and_context].update({entry: 1})
    print(organized_data)
    return organized_data


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
    reread_counts = compute_reread_counts(student_data)
    print("Number of times students reread text based on question or context:\n")
    print(reread_counts)

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

    def test_compute_reread_count(self):
        """
        Test that the reread count equals the expected values.
        """
        total_reread_count = compute_reread_counts(self.test_student_data)
        self.assertEqual(total_reread_count, {"q1_ad": {0: 1},
                                              "q1_short": {0: 1},
                                              "q2_ad": {1: 1},
                                              "q2_short": {1: 1},
                                              "q3_ad": {1: 1},
                                              "q3_short": {0: 1}})
        total_reread_count = compute_reread_counts(self.default_student_data)
        self.assertEqual(total_reread_count, {"q1_ad": {},
                                              "q1_short": {},
                                              "q2_ad": {},
                                              "q2_short": {},
                                              "q3_ad": {},
                                              "q3_short": {}
                                              })


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
