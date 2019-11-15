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


