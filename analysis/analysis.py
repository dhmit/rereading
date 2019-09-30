"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from builtins import dict
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
    middle_index = int(len(list_of_times) / 2)
    return list_of_times[middle_index]


def run_time_analysis_functions(student_data):
    median_view_time = compute_median_view_time(student_data)
    total_view_time = compute_total_view_time(student_data)

    print(f'The total view time of all students was {total_view_time}.')
    print(f'The median view time of all students was {median_view_time}.')


def description_has_relevant_words(story_meaning_description, relevant_words):
    """
    Determine if the user's description contains a word relevant to the story's meaning
    :param story_meaning_description: The three word description of the story that the user supplied
    :param relevant_words: a list of words which show an understanding of the story's meaning
    :return True if the description contains one of the relevant words. False otherwise
    """
    words_used_in_description = story_meaning_description.split(' ')
    for word in relevant_words:
        if word in words_used_in_description:
            return True
    return False


RELEVANT_WORDS_FILE_PATH = 'data/words_related_to_story.txt'


def percent_students_using_relevant_words(student_data, target_context, relevant_words):
    """
    Find the percentage of students that used relevant words in their responses
    :param student_data: the data to analyze
    :param target_context: the context (e.g. "This is an ad") to take responses from
    :param relevant_words: a list of words which show an understanding of the story's meaning
    :return: The percentage of students that used relevant words in their responses
    """
    number_of_students_using_relevant_words = 0
    total_students = 0
    for row in student_data:
        if (row.get('context') == target_context and
                row.get('question') == 'In three words or fewer, what is this text about?'):
            total_students += 1
            if description_has_relevant_words(row.get('response'), relevant_words):
                number_of_students_using_relevant_words += 1
    percentage_of_all_students = number_of_students_using_relevant_words / total_students
    return percentage_of_all_students


def read_words_from_txt_file(file):
    lines = []
    for line in file:
        lines.append(line.strip())
    return lines


def run_relevant_word_analysis(student_data):
    target_context = 'This is actually a short story.'

    relevant_words_file = open(RELEVANT_WORDS_FILE_PATH, 'r')
    relevant_words = read_words_from_txt_file(relevant_words_file)

    relevant_words_used_percent = percent_students_using_relevant_words(
        student_data, target_context, relevant_words)
    print(f'{relevant_words_used_percent * 100}% of students used words related to '
          f'the story\'s intended meaning.')


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    run_time_analysis_functions(student_data)
    run_relevant_word_analysis(student_data)


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
