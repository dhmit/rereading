"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics

from .models import StudentReadingData, StudentSegmentData


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

    def compute_reread_counts(self):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :return: int, number of times segment with sequence segment_number is reread
        """
        segment_dictionary = {}
        segment_list = []

        # For all segment objects
        for segments in self.segments:
            # Increment reread count in dictionary if the entry already in dictionary
            if (segments.segment.sequence in segment_dictionary and segments.view_time > 1.0 and
                segments.is_rereading):
                segment_dictionary[segments.segment.sequence] += 1
            # Add entry to dictionary if entry does not already exist
            elif (segments.segment.sequence not in segment_dictionary and segments.view_time > 1.0
                  and segments.is_rereading):
                segment_dictionary[segments.segment.sequence] = 1

        # Turns dictionary data into a list of lists
        keys_list = list(segment_dictionary.keys())
        keys_list.sort()
        for key in keys_list:
            segment_list.append([key, round(segment_dictionary[key] / len(self.readings), 2)])

        return segment_list

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
        if num_students != 0:
            mean_reading_time = reading_time / num_students
            mean_rereading_time = rereading_time / num_students
        else:
            return 0.0 , 0.0
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
