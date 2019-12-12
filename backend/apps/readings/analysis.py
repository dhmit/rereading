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
from .analysis_helpers import string_contains_words


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()
        self.segments = StudentSegmentData.objects.all()
        self.questions = SegmentQuestionResponse.objects.all()

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

    def percent_using_relevant_words_by_question(self):
        """
        Return a list of tuples with (question, percent), for each of the questions in the
        Segment Data and percent: percent of students who used relevant
        words in that question
        :return the return type explained in the function description
        """
        relevant_words = ["stereotypes", "bias", "assumptions", "assume", "narrator", "memory",
                          "forget", "Twyla", "Maggie", "Roberta", "black", "white", "prejudice",
                          "mothers", "segregation", "hate", "hatred", "love", "love-hate",
                          "remember", "children", "recall", "kick", "truth", "dance", "sick",
                          "fade", "old", "Mary", "sandy", "race", "racial", "racism",
                          "colorblind", "disabled", "marginalized", "poor", "rich", "wealthy",
                          "middle-class", "working-class", "consumers", "shopping", "read",
                          "misread", "reread", "reconsider", "confuse", "wrong", "mistaken",
                          "regret", "mute", "voiceless", "women", "age", "bird", "time", "scene",
                          "setting", "Hendrix ", "universal", "binary", "deconstruct",
                          "question", "wrong", "right", "incorrect", "false", "claims", "true",
                          "truth", "unknown", "ambiguous", "unclear"]

        question_count_map = {}
        for segment in self.questions:
            question = segment.question
            if question not in question_count_map:
                question_count_map[question] = 0
            if string_contains_words(segment.response, relevant_words):
                question_count_map[question] += 1

        total_student_count = len(self.readings)
        percent_question_count_map = []
        for question in question_count_map:
            percent_question_count_map.append(
                (question.text, question_count_map[question] / total_student_count)
            )
        return [relevant_words, percent_question_count_map]

    def get_all_heat_maps(self):
        """
        This function shows a heat map for each segment. It will show how long in total was spent
        on different sections of the segment.
        :return: a dictionary of dictionaries which correspond to the view times of section of
        segments
        """
        heat_map = {}

        for segment in self.segments:
            segment_identifier = segment.reading_data.document.title + " " +\
                                 str(segment.segment.sequence)
            if segment_identifier not in heat_map:
                heat_map[segment_identifier] = {"reading": {}, "rereading": {}}
            for scroll_position in segment.get_parsed_scroll_data():
                if scroll_position < 0:
                    continue
                section_number = int(scroll_position) // 500
                section_identifier = str(section_number * 500) + " — " +\
                    str((section_number + 1) * 500)
                is_rereading = "rereading" if segment.is_rereading else "reading"
                if section_identifier not in heat_map[segment_identifier][is_rereading]:
                    heat_map[segment_identifier][is_rereading][section_identifier] = 1
                else:
                    heat_map[segment_identifier][is_rereading][section_identifier] += 1
        return heat_map

    def all_responses(self):
        """
        Returns a list of all of the responses in the DB, in the form:
        [Segment Num, Question Seq Num, Question Text, Response]

        :return: List of lists
        """

        responses = []

        for segment_data in self.segments:
            segment_num = segment_data.segment.sequence

            for response in segment_data.segment_responses.all():
                question = response.question
                question_num = question.sequence
                question_text = question.text
                student_response = response.response
                evidence = response.evidence

                response_list = [
                    segment_num,
                    question_num,
                    question_text,
                    student_response,
                    evidence,
                ]
                responses.append(response_list)

        return responses

    @staticmethod
    def get_top_words_for_question(question):
        """
        Returns the top 3 most common words used to answer a question


        :param question: Question object
        :return: List of tuples in the form (response, frequency)
        """

        # Keep track of frequency of each response
        responses_frequency = Counter()

        # Get all responses to the given question, based on whether its a doc or segment question
        if isinstance(question, SegmentQuestion):
            responses = SegmentQuestionResponse.objects.filter(question=question)
        else:
            responses = DocumentQuestionResponse.objects.filter(question=question)

        # Iterate through and count all of the words in the responses
        for student_response in responses:
            student_answer_words = student_response.response.lower().split()
            for word in student_answer_words:
                responses_frequency[word] += 1

        # Find the most common words for the question
        most_common_words = responses_frequency.most_common(3)

        # Turn the words into a string for it to display properly in the frontend
        words = ''
        for frequency_pair in most_common_words:
            word = frequency_pair[0]
            words += word + ', '

        # Strip the trailing whitespace and comma from the string of words
        words = words[:-2]

        return words

    def most_common_words_by_question(self):
        """
        Returns a dictionary mapping all question texts to their most common responses and
        frequencies

        :return: List of lists, where each inner list is a question. Lists are of the form
        [segment_num, question_num, question_text, responses]
        """

        # Find the document and segment questions
        doc_questions = DocumentQuestion.objects.all()
        segment_questions = SegmentQuestion.objects.all()

        # Initialize a list of lists to keep track of the top responses
        top_words = list()

        # Iterate through the questions to find the top response for each, and store it
        for question in doc_questions:
            top_question_words = self.get_top_words_for_question(question)
            question_text = question.text
            question_num = question.sequence
            data_list = ['Global', question_num, question_text, top_question_words]
            top_words.append(data_list)

        for question in segment_questions:
            top_question_words = self.get_top_words_for_question(question)
            question_text = question.text
            segment_num = question.segment.sequence
            question_num = question.sequence
            data_list = [segment_num, question_num, question_text, top_question_words]
            top_words.append(data_list)

        return top_words
