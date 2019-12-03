"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics

from .models import StudentReadingData, StudentSegmentData, SegmentQuestionResponse


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

    @staticmethod
    def description_has_relevant_words(story_meaning_description, relevant_words):
        """
        Determine if the user's description contains a word relevant to the story's meaning
        :param story_meaning_description: The user's response
        :param relevant_words: a list of words which show an understanding of the story's meaning
        :return True if the description contains one of the relevant words or relevant_words is
        empty. False otherwise
        """
        if not relevant_words:
            return True

        lowercase_relevant_words = []
        for word in relevant_words:
            lowercase_relevant_words.append(word.lower())

        words_used_in_description = story_meaning_description.lower().split(" ")

        for word in lowercase_relevant_words:
            if word.lower() in words_used_in_description:
                return True
        return False

    def percent_using_relevant_words_by_question(self):
        """
        Return a list of tuples with (question, percent), for each of the questions in the
        Segment Data and percent: percent of students who used relevant
        words in that question
        :return the return type explained in the function description
        """
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]
        # get the list from sandy

        question_count_map = {}
        for segment in self.questions:
            question = segment.question
            if question not in question_count_map:
                question_count_map[question] = 0
            if RereadingAnalysis.description_has_relevant_words(segment.response, relevant_words):
                question_count_map[question] += 1

        total_student_count = len(self.readings)
        percent_question_count_map = []
        for question in question_count_map:
            percent_question_count_map.append(
                (question.text, question_count_map[question] / total_student_count)
            )
        return percent_question_count_map
