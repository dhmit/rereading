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
                section_number = int(scroll_position) // 500
                section_identifier = str(section_number * 500) + " — " +\
                    str((section_number + 1) * 500)
                is_rereading = "rereading" if segment.is_rereading else "reading"
                if section_identifier not in heat_map[segment_identifier][is_rereading]:
                    heat_map[segment_identifier][is_rereading][section_identifier] = 1
                else:
                    heat_map[segment_identifier][is_rereading][section_identifier] += 1
        return heat_map
