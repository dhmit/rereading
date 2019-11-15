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
        pass
        self.readings = StudentReadingData.objects.all()


    def compute_mean_response_length(self):
        """
        Given a list of student response dicts,
        return the mean character length (across all users) of the response
        :return: float, mean number of characters in the user's response
        """
        mean_response_length = 0
        for row in self.responses:
            mean_response_length += len(row.response)
        return round(mean_response_length / len(self.responses), 2)


