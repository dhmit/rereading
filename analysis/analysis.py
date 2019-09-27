"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
import unittest

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

def find_connotation_change(student_data):
    """
    Given a list of student response dicts,
    return the mean time (across each view) spent reading the text
    if the list is empty, then it returns 0
    :param student_data: a list of dictionaries
    :return: a float, the total time all users spent reading the text divided by total views
    """   
#    print(response_dict['question'])
#    print(response_dict['context'])
    negative_total_view_time = 0
    neutral_total_view_time = 0
    negative_responses = 0
    neutral_responses = 0
    
    for response_dict in student_data:
        
        if (response_dict['question'] == "In three words or fewer, what is this text about?") \
        and (response_dict['context'] == "This is an ad."):
            response = response_dict['response'].lower()
            print(response)
            print(response.split())
            for word in response.split():
                print(word)
                if word in negative_key_words_list:
                    negative_total_view_time += sum(response_dict['views'])
                    negative_responses += 1
                else:
                    neutral_total_view_time += sum(response_dict['views'])
                    neutral_responses += 1
        
    if negative_responses == 0:
        negative_mean_view_time = 0
    else:
        negative_mean_view_time = negative_total_view_time/negative_responses
    
    if neutral_responses == 0:
        neutral_mean_view_time = 0
    else:
        neutral_mean_view_time = neutral_total_view_time/neutral_responses
    
    print("People who understood the deeper meaning the first time read the \
          message for " + str(negative_mean_view_time) + " on average. While \
          people who did not, read the text for " + str(neutral_mean_view_time))
    print(negative_responses, neutral_responses)
                
            
            
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
    find_connotation_change(student_data)


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


if __name__ == '__main__':
    run_analysis()
#    unittest.main()  # run the tests

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
