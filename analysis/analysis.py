"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
from statistics import stdev
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


def get_sentiments() -> dict:
    """
    Returns a dictionary of sentiment scores, with the keys being the word and the values being
    their score

    :return: dict mapping words to their sentiment scores
    """
    sentiment_path = Path('data', 'sentiments.txt')

    sentiments = dict()
    with open(sentiment_path, 'r') as file:
        word = file.readline()

        # We want to handle each word individually, rather than as a whole set
        while word:

            # This particular file starts lines with '#' for non-sentiment comments, so skip them
            if word[0] == '#' or word[0] == '\t':
                word = file.readline()
                continue

            # All words use tabs to define the different parts of the data
            attributes = word.split('\t')

            # Pull out the word from the line
            data = attributes[4]
            data = data.split('#')
            new_word = data[0]
            positive_score = float(attributes[2])
            negative_score = float(attributes[3])

            # If the word is already in the dictionary, pick the larger value
            # This is not optimal, but standardizes data
            if new_word in sentiments:
                if abs(sentiments[new_word]) > abs(positive_score) and abs(sentiments[new_word]) > \
                        abs(negative_score):
                    word = file.readline()
                    continue

            # Find the largest sentiment score for the word, and define negative sentiments
            # as negative values (if there's a tie, the sentiment is 0)
            if positive_score == negative_score:
                score = 0
            elif positive_score > negative_score:
                score = float(positive_score)
            else:
                score = -float(negative_score)

            sentiments[new_word] = score

            word = file.readline()

    return sentiments


def question_sentiment_analysis(student_data, question_text):
    """
    Takes in a list of student response dicts, and a question prompt (or a substring of one) and
    returns the average sentiment score and standard deviation for all responses to that question

    :param student_data: list of dicts
    :param question_text: question string or substring
    :return: tuple in the form (average, standard_dev)
    """

    sentiments = get_sentiments()

    # Set up data for calculating data
    num_scores = 0
    sentiment_sum = 0
    score_list = list()

    for response in student_data:

        if question_text in response['question']:
            words = response['response'].lower().split()

            # Find the sentiment score for each word, and add it to our data
            for word in words:
                # Ignore the word if it's not in the sentiment dictionary
                if word in sentiments:
                    sentiment_sum += sentiments[word]
                    num_scores += 1
                    score_list.append(sentiments[word])

    average = sentiment_sum / num_scores
    standard_dev = stdev(score_list)

    return average, standard_dev


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
    mean_view_time_comparison(student_data)

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
