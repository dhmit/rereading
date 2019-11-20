"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
from collections import defaultdict

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
        total_time = 0
        ret_dict = defaultdict(list)
        for segment in self.segments:
            view_time = segment.view_time
            ret_dict[segment.reading_data] = view_time
            total_time += view_time
        student_total_view_time = []
        if not ret_dict.values():
            median_view_time = 0
        else:
            for item in ret_dict.values():
                student_total_view_time.append(sum(item))
            median_view_time = statistics.median(student_total_view_time)
        ret_tuple = (round(total_time), round(median_view_time))
        return ret_tuple


