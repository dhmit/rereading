"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from .models import StudentResponse, Context


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

    def frequency_feelings(self):
        """
        Compute the frequencies of a word in a specific question. Not sensitive to case.
        :return a list of tuples of words that appear more than once, and how often they occur,
        in order of their frequency
        """
        feelings = {}
        for response in self.responses:
            if response.question.text == "In one word, how does this text make you feel?":
                lower_case_word = response.response.lower()
                if feelings.get(lower_case_word, 0) == 0:
                    feelings[lower_case_word] = 1
                else:
                    feelings[lower_case_word] += 1

        frequent_words = []  # list of tuples in the format (frequency, word)
        for word in feelings:
            if feelings[word] > 1:
                frequent_words.append((word, feelings[word]))
        frequent_words.sort(key=lambda x: x[1], reverse=True)
        return frequent_words

    def context_vs_read_time(self):
        """
        Compares mean view times, of all contexts
        :return a tuple of the mean ad view and the mean story view
        """

        all_contexts = Context.objects.all()
        total_contexts_view_times = {context.text: {
                                                "total_view_time": 0,
                                                "count": 0
                                              }
                                     for context in all_contexts}
        for response in self.responses:
            context = response.context.text
            total_contexts_view_times[context]["total_view_time"] += \
                sum(response.get_parsed_views())
            total_contexts_view_times[context]["count"] += 1

        # For each context in total_contexts_view_time, calculate the average view time
        average_context_view_times = {context:
                                      total_contexts_view_times[context]["total_view_time"] /
                                      total_contexts_view_times[context]["count"]
                                      for context in total_contexts_view_times}
        return average_context_view_times

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
        return median_view_time
