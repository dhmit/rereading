"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from .models import StudentReadingData, SegmentQuestionResponse
from .analysis_helpers import description_has_relevant_words


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()

    @staticmethod
    def relevant_words_by_question(self):
        """
            Return a list of tuples of the form (question,count), where count is
            the number of students who used relevant words in response to that question. This list
            is sorted by question
            :return the return type explained in the function description
        """
        # TODO -- get a list of words from Sandy OR eventually make this interactive
        relevant_words = [
            "maggie"
        ]

        question_context_count_map = {}

        for response in SegmentQuestionResponse.objects.all():
            question = response.question.text
            question_context_count_map[question] = question_context_count_map.get(question, 0) + 1
            if description_has_relevant_words(response.response, relevant_words):
                question_context_count_map[question] += 1
        question_count_tup = list(question_context_count_map.items())
        return question_count_tup

