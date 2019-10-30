"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from .models import StudentResponse


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
        return round(total_view_time)

    def compute_median_view_time(self):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in self.responses:
            for view_time in row.get_parsed_views():
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return round(median_view_time)

    '''def compute_median_view_time(student_data):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text

        :param student_data: list, student response dicts
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in student_data:
            for view_time in row.get('views'):
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time
        '''
    def filter_words(string):
        """
        helper method to preprocess the string: remove the stopwords and punctuation
        return: list of words that are non-stopwords
        """
        stop_words_and_punct = ["i", "for", "in", "is", "are", "on", "are", "'s", ".", ","]
        return [ch for ch in string.lower().split() if ch not in stop_words_and_punct]

    def unique_word_pattern(self):
        """
        Take the list of dictionaries as a parameter and analyze the readers' responses based on the
        two different contexts of the 2 questions (this is an ad/this is just a short story);
        analyze if
        the total number of unique responses changed as more and more readers' responses are
        analyzed. Will be used for future analysis and visualization on the webapp
        :param student_data
        :return 2 lists of sets specifying unique responses at each point in time as a user
        submits a
        response
        """
        response_ad = set()
        response_story = set()
        unique_word_tracker_ad = []
        unique_word_tracker_story = []
        question = "In three words or fewer, what is this text about?"

        for response in self.responses:
            # print(response.response)
            filtered_word_resp = filter_words(response.response)
            print(filtered_word_resp)
            '''if data['question'] == question and data['context'] == "This is an ad.":
                word_set = response_ad
                histogram = unique_word_tracker_ad
            elif data['question'] == question and data[
                'context'] == "This is actually a short story.":
                word_set = response_story
                histogram = unique_word_tracker_story
            else:
                continue
            for word in filtered_word_resp:
                word_set.add(word)
            histogram.append(set(word_set))

        return unique_word_tracker_story, unique_word_tracker_ad
        '''
