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
    response_groups_freq_dicts = get_response_groups_frequencies(student_data)
    show_response_groups(response_groups_freq_dicts)
    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')

    
def run_our_analysis(student_data):
    """
    Runs the analysis on the data loaded from the CSV file by looking at the average
    reread time for each question and the context that the question was given in and
    prints it in a nice readable format.
    :return: None
    """
    question_one = "In one word, how does this text make you feel?"
    question_two = "In three words or fewer, what is this text about?"
    question_three = "Have you encountered this text before?"

    mean_rereading_time_results_data = [
        mean_rereading_time_for_a_question(student_data, question_one, "ad"),
        mean_rereading_time_for_a_question(student_data, question_two, "ad"),
        mean_rereading_time_for_a_question(student_data, question_three, "ad"),
        mean_rereading_time_for_a_question(student_data, question_one, "short story"),
        mean_rereading_time_for_a_question(student_data, question_two, "short story"),
        mean_rereading_time_for_a_question(student_data, question_three, "short story")
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
        print("")


def mean_rereading_time_for_a_question(student_data, question, context):
    """
    Given the student response dicts, computes the mean reread time for a
    specific question (given by its keyword) and the context in which it was asked.
    Returns the question, context, mean reread time, and number of people who reread.
    :param student_data: list, student response dicts
    :param question: string, to determine which question was being asked
    :param context: string, what the reader thought the reading was
    :return: tuple, in order of the question asked (full question), the context, the mean reread
             time, and the number of people who reread it
    """
    mean_time = 0
    number_of_rereaders = 0
    question_count = 0
    rereading_time = []
    total_question_view_time = 0

    for student_data_dictionary in student_data:
        if question != student_data_dictionary['question'] or\
                context != student_data_dictionary['context']:
            continue
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

    return question, context, mean_time, number_of_rereaders


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
    return times / count


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


def avg_time_context(data, question, context):
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
    return times / count


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
    result = result ** (1 / 2)
    return result

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
        test_data_2_path = Path('data', 'test_data_2.csv')
        self.default_student_data_2 = load_data_csv(test_data_2_path)
        sample_csv_path = Path('data', 'rereading_data_2019-09-13.csv')
        self.student_data = load_data_csv(sample_csv_path)

    def test_mean_rereading_time_for_a_question(self):
        # check we don't crash on the defaults from the model!
        mean_rereading_data = mean_rereading_time_for_a_question(self.default_student_data, "", "")

        empty_comparison_tuple = ("", "", 0, 0)
        self.assertEqual(mean_rereading_data, empty_comparison_tuple)

        feel = "In one word, how does this text make you feel?"
        about = "In three words or fewer, what is this text about?"
        encountered = "Have you encountered this text before?"
        ad = "This is an ad."
        short_story = "This is actually a short story."

        mean_rereading_time_results_data = [
            mean_rereading_time_for_a_question(self.test_student_data, feel, ad),
            mean_rereading_time_for_a_question(self.test_student_data, about, ad),
            mean_rereading_time_for_a_question(self.test_student_data, encountered, ad),
            mean_rereading_time_for_a_question(self.test_student_data, feel, short_story),
            mean_rereading_time_for_a_question(self.test_student_data, about, short_story),
            mean_rereading_time_for_a_question(self.test_student_data, encountered, short_story)
        ]

        # The expected result times are rounded to 2 decimals here due to Python rounding errors
        # not matching actual rounding.
        mean_comparison_results = [
            (feel, ad, round(2.319, 2), 1),
            (about, ad, round(2.945, 2), 1),
            (encountered, ad, 0, 0),
            (feel, short_story, round(1.121, 2), 1),
            (about, short_story, 0, 0),
            (encountered, short_story, 0, 0)
        ]
        self.assertEqual(mean_rereading_time_results_data, mean_comparison_results)

    def test_mean_rereading_time_for_a_question_two(self):
        mean_rereading_time = mean_rereading_time_for_a_question(self.test_student_data,
                                                                 "Have you encountered this text "
                                                                 "before?",
                                                                 "This is an ad.")

        self.assertEqual(mean_rereading_time[0], "Have you encountered this text before?")

    def test_mean_rereading_time_for_a_question_reversed(self):
        mean_rereading_time = mean_rereading_time_for_a_question(reversed(self.test_student_data),
                                                                 "Have you encountered this text "
                                                                 "before?",
                                                                 "This is an ad.")

        self.assertEqual(mean_rereading_time[0], "Have you encountered this text before?")

    def test_remove_outliers(self):
        outliers_data_1 = [-100, -50, 1, 2, 3, 4, 5, 100]
        outliers_data_2 = [1, 2, 3, 4, 5]

        remove_outliers(outliers_data_1)
        self.assertEqual(outliers_data_1, outliers_data_2)


    def test_compute_total_view_time(self):
        """
        Test that the total view time equals the expected values.
        """
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)

    def test_avg_time_context(self):
        args = [self.test_student_data,
                'In one word, how does this text make you feel?',
                'This is an ad.']
        avg_time = avg_time_context(*args)
        self.assertAlmostEqual(avg_time, 2.319)

        args = [self.default_student_data_2,
                'In one word, how does this text make you feel?',
                'This is actually a short story.']
        avg_time = avg_time_context(*args)
        self.assertAlmostEqual(avg_time, 3.1992)
        args = [self.default_student_data, 'In one word, how does this text make you feel?',
                'This is an ad.']
        avg_time = avg_time_context(*args)
        self.assertIsNone(avg_time)

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
