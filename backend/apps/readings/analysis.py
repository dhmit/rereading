"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from .models import StudentResponse


def get_responses_for_question(all_responses, question):
    """
    For a certain question, returns the set of responses as a dictionary with keys being the
    context and values being nested dictionaries containing each response and their frequency.
    :param all_responses: QuerySet of all student responses
    :param question: string, question
    :return: dictionary mapping strings to integers
    """
    responses = {}
    for response in all_responses:
        student_question = response.question.text
        student_answer = response.response.lower()
        question_context = response.context.text
        if student_question == question:
            if question_context not in responses:
                responses[question_context] = {student_answer: 1}
            else:
                if student_answer in responses[question_context]:
                    responses[question_context][student_answer] += 1
                else:
                    responses[question_context][student_answer] = 1
    return responses


def most_common_response(all_responses, question, context):
    """
    Returns a list of the most common response(s) given a set of data, a question,
    and a context.
    :param all_responses: student response object
    :param question: string, question
    :param context: string, context
    :return: list of strings
    """
    max_response = []
    response_dict = get_responses_for_question(all_responses, question)
    responses_by_context = response_dict[context]
    max_response_frequency = max(responses_by_context.values())
    for response in responses_by_context:
        if responses_by_context[response] == max_response_frequency:
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
    def get_most_common_responses_for_all(self):
        question = "In one word, how does this text make you feel?"
        context = "This is an ad."
        most_common_responses = {question: most_common_response(self.responses, question, context)}
        return most_common_responses
