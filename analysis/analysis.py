"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
import unittest
from statistics import stdev

neutral_words_list = [
    'baby shoes',
    'sale',
    'selling',
    'advertisement',
    'ad',
    'asking'
]

negative_key_words_list = [
    'miscarriage',
    'lost child',
    'death',
    'grief',
    'giving up hope',
    'deceased',
    'loss'
]


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


def mean_view_time(student_data):
    """
    Given a list of student response dicts,
    return the mean time (across each view) spent reading the text
    if the list is empty, then it returns 0
    :param student_data: a list of dictionaries
    :return: a float, the total time all users spent reading the text divided by total views
    """
    sum_of_views = 0
    count = 0
    for row_dict in student_data:
        for view_times in row_dict['views']:
            sum_of_views += view_times
            count += 1
    if count == 0:
        return 0
    else:
        return sum_of_views / count


def change_sum_list_count(list_of_views, num_of_responses, total_viewtime,
                          responses_viewtimes_list):
    """
    :param
    list_of_views (is response_dict['views']) is a list of viewtimes associated with that answer
    num_of_responses is the growing sum total of responses
    total_viewtime is the toal sum of the viewtimes
    responses_viewtimes_list is a growing list of views pulled from first parameter

    :return: a float, the total time all users spent reading the text divided by total views

    """
    total_viewtime += sum(list_of_views)
    assert isinstance(num_of_responses, int)
    num_of_responses += 1
    if len(list_of_views) == 1:
        responses_viewtimes_list.extend(list_of_views)
    else:
        for individual_viewtime in list_of_views:
            responses_viewtimes_list.append(individual_viewtime)

    return num_of_responses, total_viewtime, responses_viewtimes_list


def mean_view_time_comparison(student_data):
    """
    Given a list of student response dicts, determine if a response to a 
    specific context and question indicates that the reader understood the deeper
    meaining of the text the first time. Calculate the mean view time of both 
    groups (those who understood and those did not) for comparison.
    :param student_data: a list of dictionaries
    :return: a tuple of floats, the mean view times of negative and neutral
            respectively.
    """
    
    negative_total_view_time = 0
    neutral_total_view_time = 0
    negative_responses = 0
    neutral_responses = 0
#    negative_responses_viewtimes_list = []
#    neutral_responses_viewtimes_list = []
#    
    # Iterate through the responses that pertaining to the context and question desired
    for response_dict in student_data:
        is_not_negative = True
        if (response_dict['question'] == 'In three words or fewer, what is this text about?') \
            and (response_dict['context'] == 'This is an ad.'):
            response = response_dict['response'].lower()
            
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
            
    # Find the mean view time, assign it as zero if division fails
    try:
        negative_mean_view_time = round(negative_total_view_time / negative_responses, 3)
    except:
        negative_mean_view_time = 0
    try:
        neutral_mean_view_time = neutral_total_view_time / neutral_responses
    except:
        neutral_mean_view_time = 0
    
    print('People who understood the deeper meaning the first time read the message for ' + str(negative_mean_view_time) + ' seconds on average (mean). While people who did not, read the text for ' + str(round(neutral_mean_view_time, 3)) + ' seconds.')
    print('\nThere were ' + str(negative_responses) + ' negative responses and ' + str(neutral_responses) + ' neutral responses.\n')
    
    return (negative_mean_view_time, neutral_mean_view_time)
#    try:
#        negative_mean_view_time: float = negative_total_view_time / negative_responses
#        neutral_mean_view_time: float = neutral_total_view_time / neutral_responses
#        standard_deviation_neutral_responses: float = stdev(neutral_responses_viewtimes_list)
#        standard_deviation_negative_responses: float = stdev(negative_responses_viewtimes_list)
#        standard_error: float = (standard_deviation_negative_responses ** 2 / negative_responses
#                                 + standard_deviation_neutral_responses ** 2 / neutral_responses) \
#                                ** (1 / 2)
#        t_value: float = (negative_mean_view_time - neutral_mean_view_time) / standard_error
#        print('People who understood the deeper meaning the first time read the \
#                  message for ' + str(negative_mean_view_time) + ' on average. While \
#                  people who did not, read the text for ' + str(neutral_mean_view_time))
#        print('The sample size of the negative responses is ' + str(negative_responses),
#              ' and the sample size of the neutral responses is ' + str(neutral_responses))
#        print('The t-value is ' + str(t_value))
#        if (neutral_responses + negative_responses) < 30:
#            print('Caution: Our sample size does not pass a t-test condition.')
#    except ZeroDivisionError:
#        # should cover for if we have zero responses or our _responses_viewtimes_list is empty and
#        # what about?? being called upon by stdev() function
#        print("We did not have any responses for at least one of our criterion")


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
        result = mean_view_time_comparison(self.default_student_data)
        self.assertEqual(result, (0,0))

if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests

# select responses with negative connotations (sad, miscarriage) when the context
# was "This is an ad." and find the difference between avg view times of these
# students' with those of neutral connotations (confused, sale). Our 'hypothesis' is that there
# might be a statistically significant difference showing students with responses of negative
# connotations (i.e. got the deeper meaning of text w/o clue from context) had a correlation
# with spending more time with the text


# select students with responses with neutral connotations (confused, sale) when the context was
# "This is an ad." but had responses with negative connotations when the context was
# "This is a short story." Subtract the former from latter and take the average. This will tell us
# about how much time it takes for students to make the deeper connection.

# take average of view time with context of "This is an ad."


# take average of view time with context of "This is actually a short story."
