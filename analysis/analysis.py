"""

Analysis.py - initial analyses for rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
import statistics
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


def extract_response(student_data, question, context):
    """
    Takes a dataset, a specific question, and a context
    returns all responses that correspond to them
    :param student_data: list, student response dicts
    :param question: str, question of interest
    :param context: str, context of interest
    :return: list, all responses corresponding to the question & context
    """
    response = []
    for dictionary in student_data:
        if (dictionary["context"] == context
                and dictionary["question"] == question):
            response.append(dictionary["response"])
    return response


def extract_views(student_data, question, context):
    """
    Takes a dataset, a specific question, and a context
    returns the number of views for each response that correspond to them
    :param student_data: list, student response dicts
    :param question: str, question of interest
    :param context: str, context of interest
    :return: list, the number of views for each response
    """
    views = []
    for dictionary in student_data:
        if (dictionary["context"] == context
                and dictionary["question"] == question):
            views.append(len(dictionary["views"]))
    return views


def count_word(responses, word):
    """
    Takes a list and a specific string
    returns the number of entries that contain the string
    :param responses: list[str]
    :param word: str, string or word of interest
    :return: int, the number of entries that contain the string
    """
    count = 0
    for r in responses:
        if word in r.lower():
            count += 1
    return count


def analyze_word_count(student_data, question, word):
    """
    Takes a dataset, a specific question, and a word
    returns the number of responses that contain the word from the ad context & the story context
    :param student_data: list, student response dicts
    :param question: str, question of interest
    :param word: str, word of interest
    :return: tuple, contains the number of responses that contain the word in the ad context
    and the number of responses in the story context
    """
    response_ad = extract_response(student_data, question, "This is an ad.")
    response_story = extract_response(student_data, question, "This is actually a short story.")
    count_ad = count_word(response_ad, word)
    count_story = count_word(response_story, word)
    return count_ad, count_story


def print_analysis_word_count(student_data, question, word):
    """
    Takes a dataset, a specific question, and a word
    prints the number of responses that contain the word for the ad context vs. the story context
    :param student_data: list, student response dicts
    :param question: str, question of interest
    :param word: str, word of interest
    :return: None
    """
    result = analyze_word_count(student_data, question, word)
    print(f'For the question: "{question}":')
    print(f"Given the ad context, the number of responses that include '{word}' is"
          f" {result[0]}")
    print(f"In comparison, given the context of a story, the number is {result[1]}")
    print()


def print_total_analysis_word_count(student_data):
    """
    Takes a dataset,
    prints the comparison between ad and story context
    number of times "sad" appeared in one-word responses
    & number of times "shoe" appeared in three-word responses
    :param student_data: list, student response dicts
    :return: None
    """
    print_analysis_word_count(student_data, "In one word, how does this text make you feel?", "sad")
    print_analysis_word_count(student_data, "In three words or fewer, what is this text about?",
                              "shoe")


def print_analysis_views(student_data, question):
    """
    Takes a dataset and a specific question,
    prints the statistical summaries on
    the number of views people took for the question for ad & story contexts
    :param student_data: list, student response dicts
    :param question: str, question of interest
    :return: None
    """
    views_ad = extract_views(student_data, question, "This is an ad.")
    views_story = extract_views(student_data, question, "This is actually a short story.")
    print(f'For the question: "{question}":')
    print(f"Given the context of an ad, the average number of views taken to give a response is "
          f"{'{0:.3g}'.format(sum(views_ad) / len(views_ad))}")
    print(f"(Min: {min(views_ad)}, Max: {max(views_ad)}, Median: {statistics.median(views_ad)})")
    print(f"In comparison, given the context of a story, the average number is "
          f"{'{0:.3g}'.format(sum(views_story) / len(views_story))}")
    print(f"(Min: {min(views_story)}, Max: {max(views_story)}, "
          f"Median: {statistics.median(views_story)})")
    print()


def print_total_analysis_views(student_data):
    """
    Takes a dataset, prints the analysis results
    on the number of views (compared between ad & story context)
    :param student_data: list, student response dicts
    :return: None
    """
    print_analysis_views(student_data, "In one word, how does this text make you feel?")
    print_analysis_views(student_data, "In three words or fewer, what is this text about?")


def load_data():
    """
    Loads data from csv file
    :return: list[dict], student data
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    return load_data_csv(csv_path)


def print_analysis(data):
    """
    Takes data, prints analyses from word count and number of views
    :param data: list, student response dicts
    :return: None
    """
    print_total_analysis_word_count(data)
    print_total_analysis_views(data)


def run_analysis():
    """
    Runs the whole analysis
    :return: None
    """
    print_analysis(load_data())


class TestAnalysisMethods(unittest.TestCase):
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
        self.test_question = "In one word, how does this text make you feel?"
        self.test_context = "This is an ad."

    def test_extract_response(self):
        response_ad = extract_response(self.test_student_data, self.test_question,
                                       self.test_context)
        self.assertEqual(response_ad, ["Sad"])

        response_ad = extract_response(self.default_student_data, self.test_question,
                                       self.test_context)
        self.assertEqual(response_ad, [])

    def test_extract_views(self):
        views = extract_views(self.test_student_data, self.test_question, self.test_context)
        self.assertEqual(views, [1])

        views = extract_views(self.default_student_data, self.test_question, self.test_context)
        self.assertEqual(views, [])

    def test_count_word(self):
        response = extract_response(self.test_student_data, self.test_question, self.test_context)
        count = count_word(response, "sad")
        self.assertEqual(count, 1)

        response = extract_response(self.default_student_data, self.test_question,
                                    self.test_context)
        count = count_word(response, "sad")
        self.assertEqual(count, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
