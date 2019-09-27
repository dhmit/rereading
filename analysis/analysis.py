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
    #print(student_data)


    # csv_path = Path('data', 'test_data.csv')
    # csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    # student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    # total_view_time = compute_total_view_time(student_data)
    # print(f'The total view time of all students was {total_view_time}.')
    # print(average_time(student_data)
    #  print(data))
    average = average_time(student_data)
    print("The standard deviation:", standard_deviation(student_data, average))


def average_time(data):
    """
    Takes the data and finds the average time of all the view times in the data
    :param data: list of responses
    :return: float representing the average view times
    :return: None when there are no entries for viewing time
    """
    times = 0
    count = 0
    for dictionary in data:
        views = dictionary["views"]
        for view in views:
            times += view
            count += 1
    if count == 0:
        return None
    return times/count


def avg_time_student(data, student_id):
    """
    Takes the data and an id and computes the average time overall of the entry with that id
    :param student_id: integer, represents specific id number of student
    :param data: list of responses
    :return: float: represents the average view time of the student with this id
    :return: None: when there is no data entries for this specific id
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_id = dictionary["student_id"]
        if dict_id == student_id:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times / count


def avg_time_cxt(data, question, context):
    """
    Takes the data, a question, and context and computes the average time of the
    views of this specific context and question
    :param question: String representing a specific question
    :param context: String representing a specific context
    :param data: list of responses
    :return: float: represents the average view time spent on this specific question and context
    :return: None: when there is no data entries for this specific question and context
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_question = dictionary["question"]
        dict_context = dictionary["context"]
        if dict_question == question and dict_context == context:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times/count


def frequent_responses(freq_dict):
    """
    Takes in a dictionary with values that are frequency dictionaries
    Returns a dictionary showing the most frequent responses to each specific question/context
    combination
    :param freq_dict: dictionary, A dictionary with tuples as keys and a
    frequency dictionary as values.
    :return: dictionary, A dictionary with tuples as keys and a dictionary as values.
    The values are dictionaries with different information about the most frequent responses
    such as a list of the most common responses as well as the number of times they occurred
    """
    output = {}
    for key in freq_dict:
        details = {}
        a_freq_dict = freq_dict[key]
        max_occurrences = 0
        max_list = []
        for word in a_freq_dict:
            occurrence = a_freq_dict[word]
            if occurrence > max_occurrences:
                max_occurrences = occurrence
                max_list = [word]
            elif occurrence == max_occurrences:
                max_list.append(word)
        details['most_frequent_words'] = max_list
        details['max_occurrences'] = max_occurrences
        output[key] = details
    return output


def word_freq_all(data):
    """
    Takes in the list of responses
    Returns a dictionary linking question/context combinations to a frequency dictionary
    :param data: list, A list of all of the data entries from the survey
    :return: dictionary, A dictionary with a tuple of the question and
    context as keys and with a frequency dictionary as values
    """
    output = {}
    for entry in data:
        the_key = (entry["question"], entry["context"])
        if the_key not in output:
            output[the_key] = {}
        qc_dict = output[the_key]
        response = entry['response'].lower()
        if response not in qc_dict:
            qc_dict[response] = 1
        else:
            qc_dict[response] += 1
    return output


def standard_deviation(data, average):
    """
    Takes the data and finds the standard deviation of the time
    :param data: list of responses
    :param average: float that represents average time of views
    :return: float representing the standard deviation

    """
    result = 0
    elements = 0
    for ele in data:
        for view in ele["views"]:
            elements = elements + 1
            result = result + (view - average) ** 2
    result = result / (elements - 1)
    result = result ** (1/2)
    return result


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
        self.default_student_data_2 = [
            {
                'id': 0,
                'question': 'In one word, how does this text make you feel?',
                'context': 'This is actually a short story.',
                'response': 'Sad',
                'views': [4.231, 1.234, 5.231],
                'student_id': 2,
                'scroll_ups': 0,
            },
            {
                'id': 5,
                'question': 'In one word, how does this text make you feel?',
                'context': 'This is actually a short story.',
                'response': 'saD',
                'views': [2.2, 3.1],
                'student_id': 7,
                'scroll_ups': 2,
            },
            {
                'id': 19,
                'question': 'In one word, how does this text make you feel?',
                'context': 'This is an ad.',
                'response': 'intrigued',
                'views': [1.3],
                'student_id': 7,
                'scroll_ups': 0,
            }
        ]

    def test_avg_time_cxt(self):
        args = [self.test_student_data,
                'In one word, how does this text make you feel?',
                'This is an ad.']
        avg_time = avg_time_cxt(*args)
        self.assertAlmostEqual(avg_time, 2.319)
        
        args = [self.default_student_data_2,
                'In one word, how does this text make you feel?',
                'This is actually a short story.']
        avg_time = avg_time_cxt(*args)
        self.assertAlmostEqual(avg_time, 3.1992)
        args = [self.default_student_data,'In one word, how does this text make you feel?',
                'This is an ad.']
        avg_time = avg_time_cxt(*args)
        self.assertIsNone(avg_time)
        
    def test_compute_total_view_time(self):
        """
        Test that the total view time equals the expected values.
        """
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

    def test_avg_time_student(self):
        avg_time = avg_time_student(self.test_student_data, 15)
        self.assertAlmostEqual(avg_time, 2.128333333333)

        avg_time = avg_time_student(self.default_student_data, 0)
        self.assertIsNone(avg_time)

        avg_time = avg_time_student(self.default_student_data_2, 7)
        self.assertAlmostEqual(avg_time, 2.2)

        avg_time = avg_time_student(self.default_student_data_2, 999)
        self.assertIsNone(avg_time)

    def test_average_time(self):
        avg_time = average_time(self.test_student_data)
        self.assertAlmostEqual(avg_time, 2.128333333333)

        avg_time = average_time(self.default_student_data)
        self.assertIsNone(avg_time)

        avg_time = average_time(self.default_student_data_2)
        self.assertAlmostEqual(avg_time, 2.88266666666)

    def test_word_freq_all(self):
        freq_dict = word_freq_all(self.test_student_data)
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {
            'sad': 1
        }
        self.assertEqual(freq_dict[specific_question_context], answer)

        freq_dict = word_freq_all(self.default_student_data)
        specific_question_context = ("", "")
        answer = {
            '': 1
        }
        self.assertEqual(freq_dict[specific_question_context], answer)

    def test_frequent_responses(self):
        most_frequent_responses = frequent_responses(word_freq_all(self.test_student_data))
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {
            'most_frequent_words': ['sad'],
            'max_occurrences': 1
        }
        self.assertEqual(most_frequent_responses[specific_question_context], answer)

        most_frequent_responses = frequent_responses(word_freq_all(self.default_student_data))
        specific_question_context = ("", "")
        answer = {
            'most_frequent_words': [''],
            'max_occurrences': 1
        }
        self.assertEqual(most_frequent_responses[specific_question_context], answer)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests

