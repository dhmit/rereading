"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""

from .models import StudentReadingData


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()

    def total_view_times(self):
        total_view_time = 0
        segment_data = self.readings.segment_data.all()
        for datum in segment_data:
            total_view_time += datum.view_times
        return 5
        # qrs = segment_data.segment_responses.all()

