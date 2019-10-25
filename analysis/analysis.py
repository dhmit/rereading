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
        if (
            not (not (dictionary["context"] == context) or not (
                dictionary["question"] == question))):
            response.append(dictionary["response"])
    return response


def response_and_question_relationship(student_data, question, context):
    """
    Takes a dataset, a specific question, and a context
    Returns the number of times a certain word was responded based on the context and question
    :param student_data: list, student response dictionaries
    :param question: str, question of interest
    :param context: str, context of interest
    :returns: dictionary with number of views as keys and response frequencies as values
    """
    word_response_data = {}
    for dictionary in student_data:
        number_of_views = len(dictionary["views"])
        if dictionary["context"] == context and dictionary["question"] == question:
            if number_of_views in word_response_data.keys():
                word_response_data[number_of_views].append(dictionary["response"].lower())
            elif number_of_views not in word_response_data.keys():
                word_response_data.update({number_of_views: [dictionary["response"].lower()]})
    # Determine the number of different words to quantify
    for number_of_views in word_response_data.keys():
        word_types = []
        for word in range(len(word_response_data[number_of_views])):
            if word_response_data[number_of_views][word] not in word_types:
                word_types.append(word_response_data[number_of_views][word])
        # Quantify number of discrete words in the dictionary
        word_quantities = []
        for word in word_types:
            quantity = word_response_data[number_of_views].count(word)
            if [quantity, word] not in word_quantities:
                word_quantities.append([quantity, word])
        word_response_data[number_of_views] = word_quantities
    return word_response_data


def print_response_and_question_relationship(student_data):
    questions = [
        "In one word, how does this text make you feel?",
        "In three words or fewer, what is this text about?",
        "Have you encountered this text before?",
    ]
    contexts = [
        "This is an ad.",
        "This is actually a short story.",
    ]
    for question in questions:
        for context in contexts:
            print("For the question:", question)
            print("With the context:", context)
            word_response_data = response_and_question_relationship(student_data, question, context)
            for number_of_views in word_response_data:
                print("People who reread the text", number_of_views, "times responded:")
                for word in word_response_data[number_of_views]:
                    print(word[1], "x" + str(word[0]))
            print()


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
        if (
            not (not (dictionary["context"] == context) or not (
                dictionary["question"] == question))):
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


def determine_average_total_rereading_time(data, question=None, context=None):
    """
        Takes a dataset, a specific question, and a context
        Returns the average of the total rereading time of each person
        :param data: list, student response dictionaries
        :param question: str, question of interest (optional)
        :param context: str, context of interest (optional)
        *If a question or context is specified, only responses that have the specified question
        and/or context will be averaged
        :returns: float to 4 decimal places, The average total rereading time of each person
        """
    total_rereading_times = []
    # Adds the total rereading time of a person to a list if the response data matches the
    # specified params
    for response in data:
        if ((question == response["question"] and context == response["context"]) or
            (question == response["question"] and context is None) or
            (question is None and context == response["context"]) or
            (question is None and context is None)):
            response_rereading_times = response["views"]
            total_rereading_times.append(sum(response_rereading_times))
    # Return 0 if no total rereading times are collected
    if len(total_rereading_times) == 0:
        average_total_rereading_time = 0
    else:
        # Average of collected totals
        average_total_rereading_time = round(sum(total_rereading_times) /
                                             len(total_rereading_times), 4)
    return average_total_rereading_time


def print_determine_average_total_rereading_time(data, question=None, context=None):
    """
    Prints the average total rereading time
    Optional params of question and context to specify responses to use in the average
    :param data: list, student response dicts
    :param question: str, question of interest (optional)
    :param context: str, context of interest (optional)
    :return: None
    """
    average_total_rereading_time = determine_average_total_rereading_time(data, question, context)
    if question is None and context is None:
        print("The average total rereading time is:", end=" ")
    elif question is not None and context is None:
        print(f"For the question \'{question},\' the average total rereading time is:", end=" ")
    elif question is None and context is not None:
        print(f"For the context \'{context},\' the average total rereading time is:", end=" ")
    elif question is not None and context is not None:
        print(f"For the question \'{question},\' and the context \'{context},\' "
              f"the average total rereading time is:", end=" ")
    print(average_total_rereading_time)


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
    print_response_and_question_relationship(data)
    print_total_analysis_word_count(data)
    print_total_analysis_views(data)
    print_determine_average_total_rereading_time(data)


def run_analysis():
    """
    Runs the whole analysis
    :return: None
    """
    print("HERE:", determine_average_total_rereading_time(load_data()))
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

    def test_response_and_question_relationship(self):
        response_data = response_and_question_relationship(self.test_student_data,
                                                           self.test_question, self.test_context)
        self.assertEqual(response_data, {1: [[1, 'sad']]})
        response_data = response_and_question_relationship(self.default_student_data,
                                                           self.test_question, self.test_context)
        self.assertEqual(response_data, {})

    def test_determine_average_total_rereading_time(self):
        # Neither Question or Context specified
        average_total_rereading_time = determine_average_total_rereading_time(
            self.test_student_data)
        self.assertEqual(average_total_rereading_time, 1.0642)
        # Only Question specified
        average_total_rereading_time = determine_average_total_rereading_time(
            self.test_student_data, self.test_question)
        self.assertEqual(average_total_rereading_time, 1.7200)
        # Only Context specified
        average_total_rereading_time = determine_average_total_rereading_time(
            self.test_student_data, None, self.test_context)
        self.assertEqual(average_total_rereading_time, 1.7547)
        # Question and Context specified
        average_total_rereading_time = determine_average_total_rereading_time(
            self.test_student_data, self.test_question, self.test_context)
        self.assertEqual(average_total_rereading_time, 2.3190)
        # Test with default student data
        average_total_rereading_time = determine_average_total_rereading_time(
            self.default_student_data)
        self.assertEqual(average_total_rereading_time, 0)


if __name__ == '__main__':
    run_analysis()
    unittest.main()  # run the tests
