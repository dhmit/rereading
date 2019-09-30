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


def word_time_relations(student_data: list) -> dict:
    """
    Takes a list of dicts representing student data and aggregates case-insensitive responses
    into a dictionary, with the response as the key and the average time (across all similar
    responses) viewing the story as the value.

    :param student_data: list of dicts obtained from load_data_csv
    :return: dict, responses as keys and values as average view times for that response
    """

    # First gather all responses in an easy-to-handle format of dict(response: times)
    responses = dict()
    for response_data in student_data:

        # Find total time spent looking at story
        total_time = 0
        for view in response_data['views']:
            total_time += view

        # Add this time to the response dictionary (case-insensitive)
        response = response_data['response'].lower()
        if response not in responses:
            responses[response] = [total_time]
        else:
            responses[response].append(total_time)

    # Now compute the average time for each response and add them to a new dictionary
    averages = dict()
    for response in responses:
        times = responses[response]
        total = sum(times)
        average = total / len(times)
        averages[response] = average

    return averages


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

    response_groups_freq_dicts = get_response_groups_frequencies(student_data)
    show_response_groups(response_groups_freq_dicts)

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')


def show_response_groups(response_groups_freq_dicts):
    """
    Given response_groups_freq_dicts list of dictionaries, prints the dicts in readable format

    :param response_groups_freq_dicts, lists of 4 dicts (one for each response
    group)
    mapping words to frequencies within that response group
    :return None
    """
    print(f'Word frequencies for Single view responses to ad context: ',
          response_groups_freq_dicts[0])
    print(f'Word frequencies for Single view responses to short story context: ',
          response_groups_freq_dicts[1])
    print(f'Word frequencies for Multiple view responses to ad context: ',
          response_groups_freq_dicts[2])
    print(f'Word frequencies for Multiple view responses to short story context: ',
          response_groups_freq_dicts[3])


def get_response_groups_frequencies(student_data: list):
    """"
    Given student_data,
    Returns lists of 4 frequency dicts, one for each response group,
     that map response words to frequencies for each response group.
    Response groups are based on single vs. multiple views and ad vs. short story
    context to the "In one word, how does this text make you feel?" question
    :param student_data, list of dicts
    :return: list of four dicts (one for each response group) mapping words
    to frequencies within that response group
    """
    people_with_multiple_views = []
    people_with_one_view = []

    for person_response in student_data:
        if len(person_response['views']) == 1:
            people_with_one_view.append(person_response)
        else:
            people_with_multiple_views.append(person_response)

    single_view_short_story_group, single_view_ad_group = \
        get_groups_by_context(people_with_one_view)
    multiple_view_short_story_group, multiple_view_ad_group = \
        get_groups_by_context(people_with_multiple_views)

    response_groups = [
        single_view_ad_group,
        single_view_short_story_group,
        multiple_view_ad_group,
        multiple_view_short_story_group,
    ]

    response_groups_freq_dicts = []
    for group_name in response_groups:
        freq_dict = find_word_frequency(group_name)
        response_groups_freq_dicts.append(freq_dict)
    return response_groups_freq_dicts


def get_groups_by_context(people_with_view_number):
    """
    :param people_with_view_number: list of responses for people with certain number of views
    :return: two lists, one for responses to short story context and one for ad context
    """
    short_story_context_group = []
    ad_context_group = []
    for person in people_with_view_number:
        if person['question'] == "In one word, how does this text make you feel?":
            response = person['response'].lower()
            if person['context'] == "This is actually a short story.":
                short_story_context_group.append(response)
            else:
                ad_context_group.append(response)
    return short_story_context_group, ad_context_group


def find_word_frequency(response_list):
    """
    :param response_list: list of single-word str
    :return: freq, dict mapping each unique word in response_list to number of appearances in
    response_list
    """
    freq = {}
    for word in response_list:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


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
        sample_csv_path = Path('data', 'rereading_data_2019-09-13.csv')
        self.student_data = load_data_csv(sample_csv_path)

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

    def test_response_group_frequencies(self):
        """
        Tests get_response_groups_frequencies returns correct freq dictionaries when passed
        certain student data set
        """
        response_groups = get_response_groups_frequencies(self.student_data)
        expected = [
            {'sad': 2, 'bored': 1, 'annoyed': 2, 'fine': 1, 'melancholic': 1, 'suspicious': 1,
             'speculative': 1, 'depressed': 1, 'confused': 1},
            {'sad': 8, 'enticed': 1, 'ok': 1, 'inyrigu': 1, 'interested': 2, 'surprised': 1,
             'concerned': 1, 'helped': 1, 'depressed': 2, 'sad/curious': 1, 'intrigued': 1,
             'confused': 1, 'puzzled': 1},
            {'targeted': 1, 'confused': 3, 'informed': 2, 'weird': 1, 'comfortable': 1,
             'melancholy': 2, 'sad': 2, 'concerned': 1, 'uncomfortable': 1, 'curious': 1,
             'disappointed': 1, 'indifferent': 1, 'fine': 1, 'neutral': 1},
            {'somber': 1, 'mysterious': 1, 'curious': 1, 'sad': 1, 'interested': 1,
             'underwhelmed': 1, 'melancholy': 1, 'sadder': 1},
        ]
        self.assertEqual(expected, response_groups)

    def test_word_time_relations(self):
        """
        Test the word_time_relations function against the test data and an empty dataset
        """

        # Expected values for test_data.csv
        expected = {
            'sad': 1.72,
            'miscarriage': 1.4725,
            'no': 0,
            'yes': 0
        }
        test_result = word_time_relations(self.test_student_data)
        self.assertEqual(test_result, expected)

        # Expected dictionary for empty default data
        default_expected = {
            '': 0,
        }
        default_result = word_time_relations(self.default_student_data)
        self.assertEqual(default_result, default_expected)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
