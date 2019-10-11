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

    def compute_reread_counts(self, question, context):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :param student_data: list, student response dicts
        :param question: string, question for which reread counts is collected
        :param context: string, context for which reread counts is collected
        :return: dictionary, each key in dictionary is the number of times the text was reread
        and value is the number of students who reread that many times
        """

        # Checks that the question and context are not blank
        if question == '' or context == '':
            return {}

        # Collects the reread count for every student id of the provided context and question
        raw_reread_counts = []
        for response in self.responses:
            table_context = response.context.text
            table_question = response.question.text
            view_count = len(response.get_parsed_views())
            if context in table_context:
                if question in table_question:
                    raw_reread_counts.append(view_count)

        # Tallies the raw reread counts into the dictionary to be returned
        organized_data = {}
        for entry in raw_reread_counts:
            if entry in organized_data.keys():
                organized_data[entry] += 1
            elif len(raw_reread_counts) != 0:
                organized_data.update({entry: 1})

        return organized_data

    @property
    def reread_counts(self):
        question = "In one word, how does this text make you feel?"
        context = "This is an ad."
        return compute_reread_counts(self, question, context)
