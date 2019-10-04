"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
from statistics import stdev
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
#    negative_responses_view_times_list = []
#    neutral_responses_view_times_list = []
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
    except ZeroDivisionError:
        negative_mean_view_time = 0
    try:
        neutral_mean_view_time = neutral_total_view_time / neutral_responses
    except ZeroDivisionError:
        neutral_mean_view_time = 0

    print('People who understood the deeper meaning the first time read the message for ' + str(negative_mean_view_time) + ' seconds on average (mean). While people who did not, read the text for ' + str(round(neutral_mean_view_time, 3)) + ' seconds.')
    print('\nThere were ' + str(negative_responses) + ' negative responses and ' + str(neutral_responses) + ' neutral responses.\n')

    return negative_mean_view_time, neutral_mean_view_time
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
def get_word_frequency_differences(student_data):
    """
    Looks over the data and compares responses from people who have read the text vs.
    people who have not read the text before this exercise
    :return: a list of word frequency differences, by increasing order of frequency differences
    """

    # Iterate through all data, and separate ids of students who have vs. have not read the text
    yes_id = []
    no_id = []

    for response in student_data:
        if 'Have you encountered this text before' in response['question'] \
                and 'This is an ad.' in response['context']:
            if 'yes' not in response['response'].lower():
                no_id.append(response['student_id'])
            else:
                yes_id.append(response['student_id'])

    # Iterate through all responses, store words and word frequencies of yes vs. no responses as
    # keys and values in 2 dictionaries

    yes_responses = dict()
    no_responses = dict()

    for element in student_data:
        if 'In one word' in element['question'] and 'This is an ad' in element['context']:
            response = element['response'].lower()
            if element['student_id'] in yes_id:
                if response in yes_responses:
                    yes_responses[response] += 1
                else:
                    yes_responses[response] = 1
            else:
                if response in no_responses:
                    no_responses[response] += 1
                else:
                    no_responses[response] = 1

    # Iterate through yes_responses and no_responses, store words and frequency differences as keys
    # and values of a dictionary
    diff_responses = dict()

    for word in yes_responses:
        if word in no_responses:
            diff_responses[word] = yes_responses[word] - no_responses[word]
        else:
            diff_responses[word] = yes_responses[word]
    for word in no_responses:
        if word not in yes_responses:
            diff_responses[word] = - no_responses[word]

    # Convert diff_responses from a dictionary to a list of tuples
    diff_responses_list = []
    for word in diff_responses:
        diff_responses_list.append((word, diff_responses[word]))

    # Order diff_responses and return ordered list
    ordered_responses = sorted(diff_responses_list, key=lambda x: x[1])
    return ordered_responses


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

    def test_mean_view_time_comparison(self):
        """
        Test that the mean view times equal expected values.
        """
        result = mean_view_time_comparison(self.default_student_data)
        self.assertEqual(result, (0,0))

    def test_question_sentiment_analysis(self):
        """
        test that the average and standard deviation of test data equals the expected values
        """
        single_word_data = question_sentiment_analysis(self.test_student_data, 'one word')
        self.assertEqual(single_word_data, (-.75, 0))

        three_words_data = question_sentiment_analysis(self.test_student_data, 'three words')
        self.assertEqual(three_words_data, (0, 0))

    def test_get_sentiments(self):
        """
        test that the get_sentiments method returns the correct data for each word
        """

        sentiments = get_sentiments()
        competent_score = sentiments['competent']
        self.assertEqual(competent_score, 0.75)

        inefficient_score = sentiments['inefficient']
        self.assertEqual(inefficient_score, -0.5)

        length = len(sentiments)
        self.assertEqual(length, 89631)

    def test_word_frequency_differences(self):
        """
        Test the word_frequency_differences function
        """

        word_frequency_differences = get_word_frequency_differences(self.test_student_data)
        expected = [('sad', -1)]
        self.assertEqual(word_frequency_differences, expected)

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
