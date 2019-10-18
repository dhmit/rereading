"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
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
        :return: the info wed like to put on js
        """

        question_one = "In one word, how does this text make you feel?"
        question_two = "In three words or fewer, what is this text about?"
        question_three = "Have you encountered this text before?"
        context_one = "This is an ad."
        context_two = "This is actually a short story."

        mean_reading_time_results_data = [
            self.mean_reading_time_for_a_question(question_one, context_one),
            self.mean_reading_time_for_a_question(question_two, context_one),
            self.mean_reading_time_for_a_question(question_three, context_one),
            self.mean_reading_time_for_a_question(question_one, context_two),
            self.mean_reading_time_for_a_question(question_two, context_two),
            self.mean_reading_time_for_a_question(question_three, context_two)
        ]

        return mean_reading_time_results_data

    def mean_reading_time_for_a_question(self, question, context):
        """
        Given the student response dicts, computes the mean read time for a
        specific question (given by its keyword) and the context in which it was asked.
        Returns the question, context, mean read time, and number of people who read.
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
            if question != response.question.text or \
               context != response.context.text:
                continue
            if len(response.get_parsed_views()) != 0:
                number_of_readers += 1
            for view_time in response.get_parsed_views():
                reading_time.append(view_time)

        if len(reading_time) != 0:
            self.remove_outliers(reading_time)

        view_time = 0
        while view_time < len(reading_time):
            question_count += 1
            total_question_view_time += reading_time[view_time]
            view_time += 1

        if len(reading_time) != 0:
            mean_time = round(total_question_view_time / len(reading_time), 2)

        return "Question: " + question + " Context: "+context+" Mean time with outliers " \
            "removed: " + str(mean_time) + " Total number of readers: " + str(number_of_readers)

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

    def compute_median_view_time(self):
        """
         Given a list of student response dicts,
        return the median time (across all users) spent reading the text
        :return: float, median amount of time users spend reading the text
        """
        list_of_times = []
        for row in self.responses:
            for view_time in row.get('views'):
                list_of_times.append(view_time)
        if not list_of_times:
            median_view_time = 0
        else:
            list_of_times.sort()
            median_view_time = statistics.median(list_of_times)
        return median_view_time
