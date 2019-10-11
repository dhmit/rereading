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


def fetch_responses():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!

    # extracting text responses from csv file, depending on context given (story vs. ad)
    response_ad = []
    response_story = []
    question = "In three words or fewer, what is this text about?"
    for x in student_data:
        x['response'] = x['response'].replace('.', '').lower()  # removing punctuation and making string lowercase
        x['response'] = x['response'].replace(',', '')
        if x['question'] == question and x['context'] == "This is an ad.":
            response_ad += x['response'].split()
        elif x['question'] == question and x['context'] == "This is actually a short story.":
            response_story += x['response'].split()

    return response_ad, response_story


def repeated_prompt_words():
    """
    Reports frequencies of exact words from story prompt used in responses. Prints analysis.
    :return: tuple (response_ad, response_story), lists of unique responses to be used in further analysis.
    """

    # extracting responses from csv file
    response_ad, response_story = fetch_responses()

    # dictionaries to store frequencies of words in responses based on context given
    # word (string) : frequency (int)
    ad_resp_words = {}
    story_resp_words = {}

    # cycling through ad responses
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    for word in response_ad:
        if word in ad_resp_words:
            ad_resp_words[word] += 1
        elif word not in stop_words:
            ad_resp_words[word] = 1

    # cycling through story responses
    for word in response_story:
        if word in story_resp_words:
            story_resp_words[word] += 1
        elif word not in stop_words:
            story_resp_words[word] = 1

    # list of words in story - for longer story, would want to read it from csv file using list comprehension
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


def test_repeated_prompt_words():
    """
    Take the CSV File and analyze the readers' responses based on the two different contexts of the
    2 questions (this is an ad/this is just a short story); analyze if the total number of unique
    responses changed as more and more readers' responses are analyzed. Eventually prints out the
    pattern along with the number of unique word in the text.
    return: none
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    response_ad = set()
    response_story = set()
    unique_word_tracker_ad = []
    unique_word_tracker_story = []
    question = "In three words or fewer, what is this text about?"

    for data in student_data:
        filtered_word_resp = filter(data['response'])
        if data['question'] == question and data['context'] == "This is an ad.":
            for word in filtered_word_resp:
                response_ad.add(word)
                unique_word_tracker_ad.append(len(response_ad))

        elif data['question'] == question and data['context'] == "This is actually a short story.":
            for word in filtered_word_resp:
                response_story.add(word)
                unique_word_tracker_story.append(len(response_story))

    print("This is the frequency tracker for responses with the story context: ")
    for num in unique_word_tracker_story:
        print(str(num)+"" + "*"*num)

    print("This is the frequency tracker for responses with the ad context: ")
    for num in unique_word_tracker_ad:
        print(str(num) + "" + "*" * num)


def filter(string):
    """
    helper method to preprocess the string: remove the stopwords and punctuation
    return: list of words that are non-stopwords
    """
    stop_words_and_punct = ["i", "for", "in", "is", "are", "on", "are", "'s", ".", ","]
    return [ch for ch in string.lower().split() if ch not in stop_words_and_punct]


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


if __name__ == '__main__':
    print(repeated_prompt_words())
    test_repeated_prompt_words()

