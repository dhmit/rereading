"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""

from .models import StudentReadingData, StudentSegmentData


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        pass
        self.readings = StudentReadingData.objects.all()
        self.segmentData = StudentSegmentData.objects.all()


    def compute_mean_response_length(self):
        """
        Given a list of student response dicts,
        return the mean character length (across all users) of the response
        :return: float, mean number of characters in the user's response
        """
        mean_response_length = {}
        for entry in self.segmentData:
            mean_response_length[entry.segment.text] = len(entry.segment.text)
        return mean_response_length


