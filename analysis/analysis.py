"""

Analysis.py - creates multiple dictionaries to analyze rereading data

Creates:


"""
from ast import literal_eval
import csv
from pathlib import Path
import unittest
from collections import defaultdict


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

    def test_compute_view_time_per_response(self):
        """
        Test that average view times per response equals the expected values.
        """
        average_view_time_per_response = compute_view_time_per_response(
            self.test_student_data)
        self.assertEqual(average_view_time_per_response, {'This is an ad.': {'sad': [2.319]},
                                                          'This is actually a short story.': {
                                                              'sad': [1.121]}})

        average_view_time_per_response = compute_view_time_per_response(
            self.default_student_data)
        self.assertEqual(average_view_time_per_response, {'This is an ad.': {},
                                                          'This is actually a short story.': {}})

    def test_reread_time_difference(self):
        """
        Test average and difference modules with expected values
        """
        view_times_per_response = compute_view_time_per_response(
            self.test_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually a short'
                                                                        ' story.'])
        difference = reread_time_difference(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(difference, {'sad': ['ad', 1.198]})

        view_times_per_response = compute_view_time_per_response(
            self.default_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually a short'
                                                                        ' story.'])
        difference = reread_time_difference(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(difference, {})

    def test_get_common_elements(self):
        """
        test that common elements returns the common key:value pairs between two dictionaries
        with the values averaged together
        """
        view_times_per_response = compute_view_time_per_response(
            self.test_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually '
                                                                        'a short story.'])
        common_dict = get_common_elements(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(common_dict, {'sad': 1.72})

        view_times_per_response = compute_view_time_per_response(
            self.default_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually '
                                                                        'a short story.'])
        common_dict = get_common_elements(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(common_dict, {})

    def test_total_rereading_time_exclusive(self):
        """
        test that a dictionary of the elements exclusive to two dictionaries is what is expected
        """
        view_times_per_response = compute_view_time_per_response(
            self.test_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually '
                                                                        'a short story.'])
        exclusive_responses = total_reading_time_exclusive(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(exclusive_responses, {'This is an ad.': {},
                                               'This is actually a short story.': {}})

        view_times_per_response = compute_view_time_per_response(
            self.default_student_data)
        wanted_dict_ad_avg = build_average_dict(view_times_per_response['This is an ad.'])
        wanted_dict_ss_avg = build_average_dict(view_times_per_response['This is actually '
                                                                        'a short story.'])
        exclusive_responses = total_reading_time_exclusive(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(exclusive_responses, {'This is an ad.': {},
                                               'This is actually a short story.': {}})


def compute_view_time_per_response(student_data):
    """
    Compute the total reread times for each response
    :param student_data: list, student response dicts
    :return:
    wanted_dict_ad - Dictionary ('ad context response in lowercase': [total reading times for
        each user])
    wanted_dict_ss - Dictionary ('short story context response in lowercase': [total reading
        times for each user])
    """

    wanted_dict_ad = defaultdict(list)
    wanted_dict_ss = defaultdict(list)

    for entry in student_data:
        if entry['question'] == 'In one word, how does this text make you feel?':
            response = entry['response'].lower()
            views = sum(entry['views'])

            if entry['context'] == 'This is an ad.':
                wanted_dict_ad[response].append(views)

            elif entry['context'] == 'This is actually a short story.':
                wanted_dict_ss[response].append(views)

    return {'This is an ad.': wanted_dict_ad, 'This is actually a short story.': wanted_dict_ss}


def get_common_elements(ad_response_times, ss_response_times):
    """
    make a dictionary of the common elements between two dictionaries and averages them
    :param ad_response_times: the first dictionary to compare
    :param ss_response_times: the second dictionary to compare
    :return: one dictionary
    """
    # Start making a combined dictionary that does not separate based on context
    wanted_dict_combined = {}
    for word in ad_response_times.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_combined[word] = ad_response_times[word]

    # Continue building the combined dictionary with short story dictionary
    for word in ss_response_times.keys():
        # Average current response with new data
        if word in wanted_dict_combined.keys():
            wanted_dict_combined[word] = (wanted_dict_combined[word] + ss_response_times[word]) / 2

        # Add the new data
        else:
            wanted_dict_combined[word] = ss_response_times[word]

    return wanted_dict_combined


def reread_time_difference(ad_response_times, ss_response_times):
    """
    make a dictionary of which context had a longer reread time for each response and the difference
    :param ad_response_times: dictionary of ad response times
    :param ss_response_times: dictionary of ss response times
    :return: dict{response:[context,time]}
    """
    # Make a dictionary that gives the name of the context with the longer average response time
    # and difference between two contexts if a response is common to both contexts
    wanted_dict_difference = {}

    for word in ad_response_times.keys():
        if word in ss_response_times.keys():
            if ad_response_times[word] > ss_response_times[word]:
                wanted_dict_difference[word] = ["ad", ad_response_times[word]
                                                - ss_response_times[word]]

            else:
                wanted_dict_difference[word] = ["short story", ss_response_times[word]
                                                - ad_response_times[word]]

    return wanted_dict_difference


def total_reading_time_exclusive(wanted_dict_ad, wanted_dict_ss):
    """
    returns two dictionaries of the exclusive key:value pairs between two dictionaries
    :param wanted_dict_ss: the first dictionary to compare
    :param wanted_dict_ad: the second dictionary to compare
    :return: 2 dictionaries
    """
    # Make a dictionary of the responses used in ad context that were not used in short story
    # context and their total reading times
    wanted_dict_combined = get_common_elements(wanted_dict_ad, wanted_dict_ss)
    wanted_dict_ad_exclusive = defaultdict(list)
    wanted_dict_ss_exclusive = defaultdict(list)

    for word in wanted_dict_ad.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ad_exclusive[word].append(wanted_dict_ad[word])

    # Make a list of the responses used in short story context that were not used in ad context
    # and their total reading times
    for word in wanted_dict_ss.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ss_exclusive[word].append(wanted_dict_ss[word])

    return {'This is an ad.': wanted_dict_ad_exclusive, 'This is actually a short story.':
            wanted_dict_ss_exclusive}


def build_average_dict(input_dict):
    """
    Given a dictionary, return a dictionary with the same keys and the average of the values

    :param input_dict: dictionary {key:[values]}
    :return: dictionary {key: float}
    """
    output_dict = {}
    for key in input_dict.keys():
        output_dict[key] = sum(input_dict[key]) / len(input_dict[key])

    return output_dict


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
