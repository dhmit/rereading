"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from collections import Counter

from .models import (
    StudentReadingData,
    StudentSegmentData,
    SegmentQuestion,
    DocumentQuestion,
    DocumentQuestionResponse,
    SegmentQuestionResponse,
)


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()
        self.segments = StudentSegmentData.objects.all()

    def total_and_median_view_time(self):
        """
        This function totals the overall view times and calculates the median view time per student
        :return: a tuple containing (total view time, median view time per student)
        """
        total_time = 0  # track the total reading time while looking at segment times
        ret_dict = {}
        in_dict = []  # prevent calling ret_dict.keys() repeatedly
        for segment in self.segments:
            # prime two variable to reduce calls to database
            view_time = segment.view_time
            reading_data = segment.reading_data
            # add the segment view times to a dictionary entry for each student reading session
            if reading_data not in in_dict:
                ret_dict[reading_data] = [view_time]
                in_dict.append(reading_data)
            else:
                ret_dict[reading_data].append(view_time)
            total_time += view_time
        student_total_view_time = []
        # do not cycle through something that doesn't exist
        if not ret_dict.values():
            median_view_time = 0
        else:
            for item in ret_dict.values():
                # total the segment view times for each student
                student_total_view_time.append(sum(item))
            # find the mean of the total reading time for each student
            median_view_time = statistics.median(student_total_view_time)
        ret_tuple = (round(total_time), round(median_view_time))
        return ret_tuple

    def mean_reading_vs_rereading_time(self):
        """
        Compares mean view times of reading segments vs rereading segments
        :return a tuple with (mean reading time, mean rereading time)
        """
        reading_time = 0
        rereading_time = 0
        # cycle through every segment
        for segment in self.segments:
            view_time = segment.view_time
            is_rereading = segment.is_rereading
            # if rereading, add to total rereading time
            if is_rereading:
                rereading_time += view_time
            # if reading, add to total reading time
            else:
                reading_time += view_time

        num_students = len(self.readings)
        self.most_common_response_by_question()
        # divide by total number of readings
        mean_reading_time = reading_time / num_students
        mean_rereading_time = rereading_time / num_students
        return round(mean_reading_time), round(mean_rereading_time)

    def get_number_of_unique_students(self):
        """
        This function finds the number of unique students who have participated in the study
        :return: an integer value
        """
        student_names = []

        # go through all data in readings to get name of each user and add to set student_names
        for reading in self.readings:
            name = reading.student.name
            if not name:
                student_names.append('Anonymous')  # count one per anonymous student
            name = name.lower()
            student_names.append(name)

        return len(student_names)

    @staticmethod
    def get_top_response_for_question(question):
        """
        Returns the most common response for the given question


        :param question: Question object
        :return: Tuple in the form (response, frequency)
        """

        # Keep track of frequency of each response
        responses_frequency = Counter()

        # Get all responses to the given question, based on whether its a doc or segment question
        if isinstance(question, SegmentQuestion):
            responses = SegmentQuestionResponse.objects.filter(question=question)
        else:
            responses = DocumentQuestionResponse.objects.filter(question=question)

        # Iterate through and count all of the responses
        for student_response in responses:
            student_answer = student_response.response.lower()
            responses_frequency[student_answer] += 1

        # Find the most common response for the question
        most_common_response = responses_frequency.most_common(1)[0]

        return most_common_response

    def most_common_response_by_question(self):
        """
        Returns a dictionary mapping all question texts to their most common responses and
        frequencies

        :return: Dict mapping question strings to a tuple of the form (response, frequency)
        """

        # Find the document and segment questions
        doc_questions = DocumentQuestion.objects.all()
        segment_questions = SegmentQuestion.objects.all()

        # Initialize a list of lists to keep track of the top responses
        top_responses = list()

        # Iterate through the questions to find the top response for each, and store it
        for question in doc_questions:
            top_response = self.get_top_response_for_question(question)
            question_text = question.text
            response = top_response[0]
            frequency = top_response[1]
            data_list = [question_text, response, frequency]
            top_responses.append(data_list)

        for question in segment_questions:
            top_response = self.get_top_response_for_question(question)
            question_text = question.text
            response = top_response[0]
            frequency = top_response[1]
            data_list = [question_text, response, frequency]
            top_responses.append(data_list)

        return top_responses


