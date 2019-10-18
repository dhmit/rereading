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
        return total_view_time

    def compute_median_view_time(self):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for response in self.responses:
            for view_time in response.get_parsed_views():
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time

    def compute_mean_response_length(self):
        """
        Given a list of student response dicts,
        return the mean character length (across all users) of the response
        :return: float, mean number of characters in the user's response
        """
        list_of_responses = [r.response for r in self.responses]
        mean_response_length = 0
        for response in list_of_responses:
            mean_response_length += len(response)
        return mean_response_length / len(list_of_responses)

    @staticmethod
    def description_has_relevant_words(story_meaning_description, relevant_words):
        """
        Determine if the user's description contains a word relevant to the story's meaning
        :param story_meaning_description: The user's three word description of the story
        :param relevant_words: a list of words which show an understanding of the story's meaning
        :return True if the description contains one of the relevant words or relevant_words is
        empty. False otherwise
        """
        if not relevant_words:
            return True

        lowercase_relevant_words = list(map(lambda s: s.lower(), relevant_words))
        words_used_in_description = story_meaning_description.lower().split(' ')

        for word in lowercase_relevant_words:
            if word.lower() in words_used_in_description:
                return True
        return False

    @staticmethod
    def percent_students_using_relevant_words(student_data, target_context, relevant_words):
        """
        Find the percentage of students that used relevant words in their responses
        :param student_data: the data to analyze
        :param target_context: the context (e.g. 'This is an ad') to take responses from
        :param relevant_words: a list of words which show an understanding of the story's meaning
        :return: The percentage [0.00, 1.00] of students that used relevant words in their
        responses. 0 if there are no responses.
        """

        def row_has_correct_context_and_question(row):
            # Helper method to filter out irrelevant response data
            return row.context.text == target_context and \
                   row.question.text == 'In three words or fewer, what is this text about?'

        number_of_students_using_relevant_words = 0

        filtered_student_data = list(filter(row_has_correct_context_and_question, student_data))
        for row in filtered_student_data:
            if RereadingAnalysis.description_has_relevant_words(row.response,
                                                                relevant_words):
                number_of_students_using_relevant_words += 1

        if filtered_student_data:
            percentage_of_all_students = \
                number_of_students_using_relevant_words / len(filtered_student_data)
        else:
            percentage_of_all_students = 0
        return percentage_of_all_students

    def percent_students_using_relevant_words_in_ad_context(self):
        """
        Find the percentage of students that used relevant words in the ad context
        :return: The percentage [0.00, 1.00] of students that used relevant words in their
        responses. 0 if there are no responses.
        """
        context = 'This is an ad.'

        context = 'This is an ad.'
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]
        percentage = RereadingAnalysis.percent_students_using_relevant_words(self.responses,
                                                                             context,
                                                                             relevant_words)
        return percentage

    def percent_students_using_relevant_words_in_story_context(self):
        """
        Find the percentage of students that used relevant words in the short story context
        :return: The percentage [0.00, 1.00] of students that used relevant words in their
        responses. 0 if there are no responses.
        """
        context = 'This is actually a short story.'
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]
        percentage = RereadingAnalysis.percent_students_using_relevant_words(self.responses,
                                                                             context,
                                                                             relevant_words)
        return percentage
