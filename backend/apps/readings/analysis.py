"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from .models import StudentResponse


def repeated_prompt_words(responses):
    """
    Calculates frequencies of exact words from story prompt used in responses (disregards words
    not in story prompt).
    :param responses: list of words used in a set of responses
    :return: A dictionary, resp_words. Key is a word from the prompt, value is its frequency
    among
    responses
    """
    # dictionary to store frequencies of words in responses
    resp_words = {}

    # cycling through responses
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    for word in responses:
        print(word)
        if word in resp_words:
            resp_words[word] += 1
        elif word not in stop_words:
            resp_words[word] = 1

    # list of words in story
    # TODO for longer story, would want to read it from csv file instead of hardcoding
    story_vocab_list = ["for", "sale", "baby", "shoes", "never", "worn"]

    # eliminating all words not in prompt
    for word in responses:
        if word not in story_vocab_list and word in resp_words:
            del resp_words[word]

    # TODO Will add this to frontend to display data collected

    # uncomment for most commonly repeated word

    # print("Most commonly repeated words in response:")
    # print(max(resp_words.items(), key=lambda item: item[1]))

    # uncomment for complete list of words used in responses (unsorted)

    # print("All words in responses:")
    # print(resp_words)

    return resp_words


class RereadingAnalysis:
    """
    This class loads all student responses from the db,
    and implements analysis methods on these responses.

    We use .serializers.AnalysisSerializer to send these analysis results to the
    frontend for display.
    """

    def __init__(self):
        """ On initialization, we load all of the StudentResponses from the db """
        self.responses = StudentResponse.objects.all()

    def total_view_time(self):
        """
        Queries the db for all StudentResponses,
        and computes total time (across all users) spent reading the text

        :return: float, the total time all users spent reading the text
        """
        total_view_time = 0
        for response in self.responses:
            for view_time in response.get_parsed_views():
                total_view_time += view_time
        return total_view_time

    def compute_median_view_time(self):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in self.responses:
            for view_time in row.get('views'):
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time

    def clean_resp_strings(self):
        """
        Removes punctuation from responses in dataset and makes all characters lowercase.
        :return: a copy of dataset with no punctuation and all characters lowercase in the
        value keyed by 'response'
        """
        clean_dataset = []
        for resp in self.responses:
            clean_dataset.append(resp)

        for clean_resp in clean_dataset:
            clean_resp.response = clean_resp.response.replace('.', '').lower()
            clean_resp.response = clean_resp.response.replace(',', '')

        return clean_dataset

    def extract_responses_by_context(self):
        """
        Extracts text responses to "In three words or fewer, what is this text about?" from given
        csv
        file, depending on context given (story vs. ad). Returns lists of words used in question
        responses. Also removes duplicates.
        :return: response_ad and response_story, lists of strings of all words used in user
        responses
        (duplicates included)
        """
        # cycling through dataset to find prompt responses, sorting based on context
        responses_ad = []
        responses_story = []
        question = "In three words or fewer, what is this text about?"

        # removing punctuation and making lowercase
        clean_dataset = self.clean_resp_strings()  # removing punctuation and making lowercase
        for resp in clean_dataset:
            if resp.question == question and resp.context == "This is an ad.":
                responses_ad += resp['response'].split()
            elif resp.question == question and resp.context == "This is actually a short story.":
                responses_story += resp['response'].split()

        return responses_ad, responses_story

    def all_contexts_repeated_prompt_words(self):
        responses_ad, responses_story = self.extract_responses_by_context()
        return repeated_prompt_words(responses_ad), repeated_prompt_words(responses_story)
