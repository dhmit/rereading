"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
import unittest
import math


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
    Runs the analysis on the data loaded from the CSV file by looking at the average
    reread time for each question and the context that the question was given in and
    prints it in a nice readable format.
    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)

    mean_rereading_time_results_data = [
        mean_rereading_time_for_a_question(student_data, "feel", "ad"),
        mean_rereading_time_for_a_question(student_data, "about", "ad"),
        mean_rereading_time_for_a_question(student_data, "encountered", "ad"),
        mean_rereading_time_for_a_question(student_data, "feel", "short story"),
        mean_rereading_time_for_a_question(student_data, "about", "short story"),
        mean_rereading_time_for_a_question(student_data, "encountered", "short story")
    ]

    for rereading_result in mean_rereading_time_results_data:
        if rereading_result[3] != 0:
            print(f"Out of those who thought the reading was a(n) {rereading_result[1]}"
                  f"and were asked {rereading_result[0]}\"")
            print(
                f"{rereading_result[3]} subject(s) reread the text for an average of "
                f"{round(rereading_result[2], 3)} seconds.")
        else:
            print(f"No one who thought the reading was a(n) {rereading_result[1]} and were asked "
                  f"\"{rereading_result[0]}\" reread the text.")
        print()


def mean_rereading_time_for_a_question(student_data, question_keyword, context):
    """
    Given the student response dicts, computes the mean reread time for a
    specific question (given by its keyword) and the context in which it was asked.
    Returns the question, context, mean reread time, and number of people who reread.
    :param student_data: list, student response dicts
    :param question_keyword: string, keyword to determine which question was being asked
    :param context: string, what the reader thought the reading was
    :return: tuple, in order of the question asked (full question), the context, the mean reread
             time, and the number of people who reread it
    """
    mean_time = 0
    number_of_rereaders = 0
    question_asked = ""
    question_count = 0
    rereading_time = []
    total_question_view_time = 0

    for student_data_dictionary in student_data:
        if student_data_dictionary['question'].find(question_keyword) != -1:
            question_asked = student_data_dictionary['question']
            if student_data_dictionary['context'].find(context) != -1:
                if len(student_data_dictionary['views']) != 0:
                    number_of_rereaders += 1
                for view_time in student_data_dictionary['views']:
                    rereading_time.append(view_time)

    if len(rereading_time) != 0:
        remove_outliers(rereading_time)

    view_time = 0
    while view_time < len(rereading_time):
        question_count += 1
        total_question_view_time += rereading_time[view_time]
        view_time += 1

    if len(rereading_time) != 0:
        mean_time = round(total_question_view_time / len(rereading_time), 2)

    return question_asked, context, mean_time, number_of_rereaders


def remove_outliers(rereading_time):
    """
    Given a list of times, calculates and removes outliers.
    :param rereading_time: list, rereading times for a specific question
    :return: list, rereading times for a specific question with outliers removed
    """
    rereading_time.sort()
    quartile_one = rereading_time[math.trunc(len(rereading_time) * 0.25)]
    quartile_three = rereading_time[math.trunc(len(rereading_time) * 0.75)]
    interquartile_range = quartile_three - quartile_one
    lower_fence = quartile_one - (1.5 * interquartile_range)
    upper_fence = quartile_three + (1.5 * interquartile_range)

    view_time_two = 0
    while view_time_two < len(rereading_time):
        if (rereading_time[view_time_two] < lower_fence) \
                or (rereading_time[view_time_two] > upper_fence):
            rereading_time.remove(rereading_time[view_time_two])
            view_time_two -= 1
        else:
            view_time_two += 1

    return rereading_time


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

    def test_mean_rereading_time_for_a_question(self):
        # check we don't crash on the defaults from the model!
        mean_rereading_data = mean_rereading_time_for_a_question(self.default_student_data, "", "")

        empty_comparison_tuple = ("", "", 0, 0)
        self.assertEqual(mean_rereading_data, empty_comparison_tuple)

        mean_rereading_time_results_data = [
            mean_rereading_time_for_a_question(self.test_student_data, "feel", "ad"),
            mean_rereading_time_for_a_question(self.test_student_data, "about", "ad"),
            mean_rereading_time_for_a_question(self.test_student_data, "encountered", "ad"),
            mean_rereading_time_for_a_question(self.test_student_data, "feel", "short story"),
            mean_rereading_time_for_a_question(self.test_student_data, "about", "short story"),
            mean_rereading_time_for_a_question(self.test_student_data, "encountered", "short story")
        ]

        # The expected result times are rounded to 2 decimals here due to Python rounding errors
        # not matching actual rounding.
        mean_comparison_results = [
            ("In one word, how does this text make you feel?", "ad", round(2.319, 2), 1),
            ("In three words or fewer, what is this text about?", "ad", round(2.945, 2), 1),
            ("Have you encountered this text before?", "ad", 0, 0),
            ("In one word, how does this text make you feel?", "short story", round(1.121, 2), 1),
            ("In three words or fewer, what is this text about?", "short story", 0, 0),
            ("Have you encountered this text before?", "short story", 0, 0)
        ]
        self.assertEqual(mean_rereading_time_results_data, mean_comparison_results)

    def test_compute_total_view_time(self):
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
