"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from .models import StudentResponse
import math


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

    def print_self(self):
        print(self.responses)

    @property
    def run_mean_reading_analysis_for_questions(self):
        """
        Runs the analysis on the data loaded from the CSV file by looking at the average
        read time for each question and the context that the question was given in and
        prints it in a nice readable format.
        :return: None
        """
        self.print_self()
        return self.mean_reading_time_for_a_question(
            "In one word, how does this text make you feel?",
            "ad"
            )

        """


        question_one = "In one word, how does this text make you feel?"
        question_two = "In three words or fewer, what is this text about?"
        question_three = "Have you encountered this text before?"

        hello = self.response.get_context()

        mean_reading_time_results_data = [
            mean_reading_time_for_a_question(self.responses.get_parsed_views(), question_one, "ad"),
            mean_reading_time_for_a_question(self.responses, question_two, "ad"),
            mean_reading_time_for_a_question(self.responses, question_three, "ad"),
            mean_reading_time_for_a_question(self.responses, question_one, "short story"),
            mean_reading_time_for_a_question(self.responses, question_two, "short story"),
            mean_reading_time_for_a_question(self.responses, question_three, "short story")
        ]

        for reading_result in mean_reading_time_results_data:
            if reading_result[3] != 0:
                print(f"Out of those who thought the reading was a(n) {reading_result[1]}"
                      f"and were asked {reading_result[0]}\"")
                print(
                    f"{reading_result[3]} subject(s) read the text for an average of "
                    f"{round(reading_result[2], 3)} seconds.")
            else:
                print(f"No one who thought the reading was a(n) {reading_result[1]} and were asked "
                      f"\"{reading_result[0]}\" read the text.")
            print("")
    """

    def mean_reading_time_for_a_question(self, question, context):
        """
        Given the student response dicts, computes the mean read time for a
        specific question (given by its keyword) and the context in which it was asked.
        Returns the question, context, mean read time, and number of people who read.
        :param student_data: list, student response dicts
        :param question: string, to determine which question was being asked
        :param context: string, what the reader thought the reading was
        :return: tuple, in order of the question asked (full question), the context,
        the mean read time, and the number of people who read it
        """
        mean_time = 0
        number_of_readers = 0
        question_count = 0
        reading_time = []
        total_question_view_time = 0
        student_data = self.responses[:]
        for response in student_data:
            print(response.question.text)
            # print(response.context.text)
            # print(response.get_parsed_views())
            if question != response.question.text or \
               context != response.context.text:
                continue
            if len(response.get_parsed_views()) != 0:
                number_of_readers += 1
            for view_time in response.get_parsed_views():
                reading_time.append(view_time)
        if len(reading_time) != 0:
            student_data.remove_outliers(reading_time)

        view_time = 0
        while view_time < len(reading_time):
            question_count += 1
            total_question_view_time += reading_time[view_time]
            view_time += 1

        if len(reading_time) != 0:
            mean_time = round(total_question_view_time / len(reading_time), 2)
        return question, context, mean_time, number_of_readers

    def remove_outliers(self, reading_time):
        """
        Given a list of times, calculates and removes outliers, which are the data points that
        are outside the interquartile range of the data
        :param reading_time: list, reading times for a specific question
        :return: list, reading times for a specific question with outliers removed
        """
        reading_time.sort()
        quartile_one = reading_time[math.trunc(len(reading_time) * 0.25)]
        quartile_three = reading_time[math.trunc(len(reading_time) * 0.75)]
        interquartile_range = quartile_three - quartile_one
        lower_fence = quartile_one - (1.5 * interquartile_range)
        upper_fence = quartile_three + (1.5 * interquartile_range)

        view_time_two = 0
        while view_time_two < len(reading_time):
            if (reading_time[view_time_two] < lower_fence) \
                    or (reading_time[view_time_two] > upper_fence):
                reading_time.remove(reading_time[view_time_two])
                view_time_two -= 1
            else:
                view_time_two += 1

        return reading_time
