"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from collections import Counter

from .models import StudentResponse


def get_responses_for_question(all_responses, question, context):
    """
    For a certain question and context, returns the set of responses as a dictionary with keys
    being the response and values being the frequency.
    :param all_responses: QuerySet of all student responses
    :param question: string, question
    :param context: string, context
    :return: dictionary mapping strings to integers
    """
    responses_frequency = Counter()
    response_list = []
    for student_response in all_responses:
        student_question = student_response.question.text
        student_context = student_response.context.text
        student_answer = student_response.response.lower()
        if student_question == question and student_context == context:
            response_list.append(student_answer)
    for answer in response_list:
        responses_frequency[answer] += 1
    return responses_frequency


def most_common_response_by_question_and_context(all_responses, question, context):
    """
    Returns a list of the most common response(s) given a set of data, a question,
    and a context.
    :param all_responses: student response object
    :param question: string, question
    :param context: string, context
    :return: list of strings
    """
    max_response = []
    response_dict = get_responses_for_question(all_responses, question, context)
    max_response_frequency = max(response_dict.values())
    for response in response_dict:
        if response_dict[response] == max_response_frequency:
            max_response.append(response)
    return max_response


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

    def all_responses(self):
        """
        Given a list of student response dicts, returns the most common responses for each
        question and in each context.
        :return: list of dictionaries storing each question, context, and most common answers
        """
        questions = []
        contexts = []
        all_responses = []
        for response in self.responses:
            if response.question.text not in questions:
                questions.append(response.question.text)
            if response.context.text not in contexts:
                contexts.append(response.context.text)
        for question in questions:
            for context in contexts:
                answers = most_common_response_by_question_and_context(
                    self.responses,
                    question,
                    context,
                )
                response_by_question_and_context = {
                    'question': question,
                    'context': context,
                    'answers': answers
                }
                all_responses.append(response_by_question_and_context)

        return all_responses

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
