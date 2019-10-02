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
        #length = len(get_sentiments())
        #self.assertEqual(length, 117659)

        sentiments = get_sentiments()
        competent_score = sentiments['competent']
        self.assertEqual(competent_score, 0.75)

        inefficient_score = sentiments['inefficient']
        self.assertEqual(inefficient_score, -0.5)

        length = len(sentiments)
        self.assertEqual(length, 89631)




if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
