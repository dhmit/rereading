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


def mean_view_time_comparison(student_data):
    """
    Calculate the mean view time of both groups (those who had a negative-word response and those
    did not) for comparison.
    :param student_data: a list of dictionaries
    :return: a tuple of floats, the mean view times of negative and neutral
            respectively.
    """
    negative_total_view_time = 0
    neutral_total_view_time = 0
    negative_responses = 0
    neutral_responses = 0
    # list of negative words used to separate students' responses
    negative_key_words_list = [
        'miscarriage',
        'lost child',
        'death',
        'grief',
        'giving up hope',
        'deceased',
        'loss'
    ]
    # iterates through all responses in student_data
    for response_dict in student_data:
        is_not_negative = True
        if (response_dict['question'] == 'In three words or fewer, what is this text about?') \
            and (response_dict['context'] == 'This is an ad.'):
            response = response_dict['response'].lower()
            print(response_dict)
            # Iterate through negative words checking whether it can be found
            # in the current response. Keeps track of number of responses and
            # total times.
            for word in negative_key_words_list:
                if word in response:
                    negative_responses += 1
                    negative_total_view_time += sum(response_dict['views'])
                    is_not_negative = False
                    break
            if is_not_negative:  # only run this if no negative word was found
                neutral_responses += 1
                neutral_total_view_time += sum(response_dict['views'])

    if negative_responses == 0:
        negative_mean_view_time = 0
    else:
        negative_mean_view_time = negative_total_view_time / negative_responses
    if neutral_responses == 0:
        neutral_mean_view_time = 0
    else:
        neutral_mean_view_time = neutral_total_view_time / neutral_responses

    print('People who responded with a negative-word to the neutral ad-context '
          'read the message for '+ str(round(negative_mean_view_time, 3)) +
          ' seconds on average (mean). People who did not respond with a negative-word to the '
          'neutral ad-context read the text for ' + str(round(neutral_mean_view_time, 3)) +
          ' seconds on average (mean).')
    print('\nThere were ' + str(negative_responses) + ' negative responses and '
          + str(neutral_responses) + ' neutral responses.\n')

    return negative_mean_view_time, neutral_mean_view_time



def run_analysis():
    """
    Runs the analytical method on the reading data
    :return: None
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    #    total_view_time = compute_total_view_time(student_data)
    #    print(f'The total view time of all students was {total_view_time}.')

    # TODO: do something with student_data that's not just printing it!
    #    print(student_data)
    mean_view_time_comparison(student_data)


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
        self.test_mean_view_time_comparison_student_data = [
            {'id': 60, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Miscarriage', 'views': [2.945],
             'student_id': 15, 'scroll_ups': 0},
            {'id': 66, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'New baby shoes', 'views': [],
             'student_id': 16, 'scroll_ups': 0},
            {'id': 72, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Baby shoes', 'views': [3.807],
             'student_id': 17, 'scroll_ups': 0},
            {'id': 78, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Something for sale', 'views': [],
             'student_id': 18, 'scroll_ups': 0},
            {'id': 84, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Selling baby shoes', 'views': [],
             'student_id': 19, 'scroll_ups': 0},
            {'id': 90, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Advertisement', 'views': [],
             'student_id': 20, 'scroll_ups': 0},
            {'id': 96, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'New baby shoes', 'views': [],
             'student_id': 21, 'scroll_ups': 0},
            {'id': 102, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'baby shoe ad', 'views': [], 'student_id': 22,
             'scroll_ups': 0},
            {'id': 108, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Shoes on sale', 'views': [],
             'student_id': 23, 'scroll_ups': 0},
            {'id': 114, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'selling baby shoes', 'views': [],
             'student_id': 24, 'scroll_ups': 0},
            {'id': 120, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'A lost child', 'views': [], 'student_id': 25,
             'scroll_ups': 0},
            {'id': 126, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Story', 'views': [], 'student_id': 26,
             'scroll_ups': 0},
            {'id': 132, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': 'Giving up hope', 'views': [],
             'student_id': 27, 'scroll_ups': 0},
            {'id': 138, 'question': 'In three words or fewer, what is this text about?',
             'context': 'This is an ad.', 'response': "an infant's death", 'views': [],
             'student_id': 28, 'scroll_ups': 0}
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

    def test_mean_view_time_comparison(self):
        """
        Test that the mean view times equal expected values.
        """
        result = mean_view_time_comparison(self.test_mean_view_time_comparison_student_data)
        self.assertEqual(result, (.73625, .3807))

        result = mean_view_time_comparison(self.default_student_data)
        self.assertEqual(result, (0,0))




if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
