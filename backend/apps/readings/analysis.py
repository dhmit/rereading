"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from analysis.analysis import description_has_relevant_words
from .models import StudentReadingData, SegmentQuestionResponse


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()

    def relevant_words_by_question(self):
        """
            Return a list of tuples of the form (question,count), where count is
            the number of students who used relevant words in response to that question. This list
            is sorted by question
            :return the return type explained in the function description
        """
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]

        question_context_count_map = {}

        for q in SegmentQuestionResponse.objects.all():
            question = q.question.text
            question_context_count_map[question] = question_context_count_map.get(question, 0)+1
            if description_has_relevant_words(q.response, relevant_words):
                question_context_count_map[question] += 1
        question_count_tup = [(question, count) for question, count in
                              question_context_count_map.items()]
        return question_count_tup

