"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
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

    @property
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

    @property
    def frequency_feelings(self):
        """
        :param self
        :return a list of tuples of words that appear more than once, and how often they occur,
        in order of their frequency
        """
        feelings = {}
        for response in self.responses:
            # print(response)
            # print(response.question.text)
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

        # print(frequent_words)

        for i in range(len(frequent_words) - 1):
            for j in range(i + 1, len(frequent_words)):
                if (frequent_words[i])[1] < (frequent_words[j])[1]:
                    frequent_words[i], frequent_words[j] = frequent_words[j], frequent_words[i]

        # print(frequent_words)
        return frequent_words

    @property
    def context_vs_read_time(self):
        """
        compares average viewtimes, given different context (ad vs story)
        :return a tuple of the average ad view and the average story view
        """
        ad_sum = 0
        ad_count = 0
        story_sum = 0
        story_count = 0

        for response in self.responses:
            context = response.context.text
            parsed_views = response.get_parsed_views()
            if context == "This is an ad.":
                if len(parsed_views) != 0:
                    for view in parsed_views:
                        ad_sum = ad_sum + view
                ad_count += 1
            elif context == "This is actually a short story.":
                if len(parsed_views) != 0:
                    for view in parsed_views:
                        story_sum = story_sum + view
                story_count += 1

        if ad_count == 0:
            mean_ad_view = 0
        else:
            mean_ad_view = ad_sum / ad_count
        if story_count == 0:
            mean_story_view = 0
        else:
            mean_story_view = story_sum / story_count

        return mean_ad_view, mean_story_view
