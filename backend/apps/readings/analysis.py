"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from collections import Counter

from .models import StudentReadingData, StudentSegmentData, SegmentQuestionResponse, DocumentQuestionResponse


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()
        self.segments = StudentSegmentData.objects.all()
        self.questions =
        self.segment_responses = SegmentQuestionResponse.objects.all()
        self.question_responses = DocumentQuestionResponse.objects.all()

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

    def get_number_of_unique_students(self):
        """
        This function finds the number of unique students who have participated in the study
        :return: an integer value
        """
        student_names = set()

        # go through all data in readings to get name of each user and add to set student_names
        for reading in self.readings:
            name = reading.student.name
            # convert to lower just in case some students forget to capitalize
            name = name.lower()
            # add name to set
            student_names.add(name)
        # return length of set (represents unique number of students)
        return len(student_names)

    def get_responses_for_question(self, question):
        """
        For a certain question and context, returns the set of responses as a dictionary with keys
        being the response and values being the frequency.
        :param question: string, question
        :return: dictionary mapping strings to integers
        """
        responses_frequency = Counter()
        response_list = []
        for response in self.segment_responses:
            student_question = response.question.text
            student_answer = response.response.lower()
            if student_question == question:
                response_list.append(student_answer)
        for answer in response_list:
            responses_frequency[answer] += 1
        return responses_frequency

    def most_common_response_by_question(self, question):
        """
        Returns a list of the most common response(s) given a set of data, a question,
        and a context.
        :param question: string, question
        :return: list of strings
        """
        max_response = []
        response_dict = self.get_responses_for_question(question)
        max_response_frequency = max(response_dict.values())
        for response in response_dict:
            if response_dict[response] == max_response_frequency:
                max_response.append(response)
        return max_response



