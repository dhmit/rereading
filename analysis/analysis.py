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


def fetch_responses(dataset):
    """
    Extracts text responses to "In three words or fewer, what is this text about?" from given csv file, depending on
    context given (story vs. ad). Returns lists of words used in question responses.
    :param dataset: list of loaded data to analyze
    :return: response_ad and response_story, lists of strings of all words used in user responses (duplicates included)
    """
    # cycling through dataset to find prompt responses, sorting based on context
    responses_ad = []
    responses_story = []
    question = "In three words or fewer, what is this text about?"
    for x in dataset:
        x['response'] = x['response'].replace('.', '').lower()  # removing punctuation and making string lowercase
        x['response'] = x['response'].replace(',', '')
        if x['question'] == question and x['context'] == "This is an ad.":
            responses_ad += x['response'].split()
        elif x['question'] == question and x['context'] == "This is actually a short story.":
            responses_story += x['response'].split()

    return responses_ad, responses_story


def repeated_prompt_words(dataset):
    """
    Calculates frequencies of exact words from story prompt used in ad and story context responses (disregards words
    not in story prompt).
    :param dataset: list of loaded data to analyze
    :return: Two dictionaries, ad_resp_words and story_resp_words. Key is word, value is frequency among responses.
    """

    # extracting responses from csv file
    responses_ad, responses_story = fetch_responses(dataset)

    # dictionaries to store frequencies of words in responses based on context given
    # word (string) : frequency (int)
    ad_resp_words = {}
    story_resp_words = {}

    # cycling through ad responses
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    for word in responses_ad:
        if word in ad_resp_words:
            ad_resp_words[word] += 1
        elif word not in stop_words:
            ad_resp_words[word] = 1

    # cycling through story responses
    for word in responses_story:
        if word in story_resp_words:
            story_resp_words[word] += 1
        elif word not in stop_words:
            story_resp_words[word] = 1

    # list of words in story
    # TODO for longer story, would want to read it from csv file using list comprehension instead of hardcoding
    story_vocab_list = ["for", "sale", "baby", "shoes", "never", "worn"]

    # for the first question given the context of the ad
    to_delete = []
    for word in ad_resp_words.keys():
        if word not in story_vocab_list:
            to_delete.append(word)
    for x in to_delete:
        del ad_resp_words[x]

    # for the second question given the context of the story
    to_delete = []
    for word in story_resp_words.keys():
        if word not in story_vocab_list:
            to_delete.append(word)
    for x in to_delete:
        del story_resp_words[x]

    # TODO Will add this to frontend to display data collected

    # uncomment for most commonly repeated words

    # print("Most commonly repeated words in ad context response:")
    # print(max(ad_resp_words.items(), key=lambda item: item[1]))
    # print("Most commonly repeated words in story context response:")
    # print(max(story_resp_words.items(), key=lambda item: item[1]))

    # uncomment for complete list of words used in responses (unsorted)

    # print("All words in ad context responses:")
    # print(ad_resp_words)
    # print("All words in story context responses:")
    # print(story_resp_words)

    return ad_resp_words, story_resp_words


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

    def test_fetch_responses(self):
        """
        Tests that the fetch_responses() function correctly extracts words from different context responses. Tests
        against test_data.csv and the default dataset.
        """
        # testing against test_data.csv
        test_ad_responses, test_story_responses = fetch_responses(self.test_student_data)
        expected_ad_responses = ["miscarriage"]
        expected_story_responses = ["miscarriage"]

        self.assertEqual(test_ad_responses, expected_ad_responses)
        self.assertEqual(test_story_responses, expected_story_responses)

        # testing against default dataset
        test_ad_responses, test_story_responses = fetch_responses(self.default_student_data)
        expected_ad_responses = []
        expected_story_responses = []

        self.assertEqual(test_ad_responses, expected_ad_responses)
        self.assertEqual(test_story_responses, expected_story_responses)

    def test_repeated_prompt_words(self):
        """
        Tests that the repeated_prompt_words() function returns the right repeated word counts for the story text.
        Tests against test_data.csv and the default dataset.
        """
        # testing against test_data.csv
        test_ad_words, test_story_words = repeated_prompt_words(self.test_student_data)
        expected_ad_words = {}
        expected_story_words = {}

        self.assertEqual(test_ad_words, expected_ad_words)
        self.assertEqual(test_story_words, expected_story_words)

        # testing against default dataset
        test_ad_words, test_story_words = repeated_prompt_words(self.default_student_data)
        expected_ad_words = {}
        expected_story_words = {}

        self.assertEqual(test_ad_words, expected_ad_words)
        self.assertEqual(test_story_words, expected_story_words)


if __name__ == '__main__':
    unittest.main()
