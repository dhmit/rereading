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

    '''def total_view_times(self):
        total_view_time = 0
        segment_data = self.readings.segment_data.all()
        for datum in segment_data:
            total_view_time += datum.view_times
        return 5'''
        # qrs = segment_data.segment_responses.all()

    def mean_reading_time_for_a_segment(self):
        total_and_median_time = self.total_and_median_view_time()
        segment_count = len(self.segments)
        return round(total_and_median_time[0] / segment_count, 2)
