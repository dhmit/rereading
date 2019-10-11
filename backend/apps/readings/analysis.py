"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from django.test import TestCase

from .models import StudentResponse


class RereadingAnalysis:
    """
    This class loads all student responses from the db,
    and implements analysis methods on these responses.

    We use .serializers.AnalysisSerializer to send these analysis results to the
    frontend for display.
    """

    def __init__(self):
        """ On initialization, we load all of the StudentResponses from the db """
        self.responses = StudentResponse.objects.all()

    def total_view_time(self):
        """
        Queries the db for all StudentResponses,
        and computes total time (across all users) spent reading the text

        :return: float, the total time all users spent reading the text
        """
        total_view_time = 0
        for response in self.responses:
            for view_time in response.get_parsed_views():
                total_view_time += view_time
        return total_view_time


class AnalysisTests(TestCase):
    """
    Test case for running tests on the new Django-i-fied version of our analyses.
    When Django test cases are run, Django spins up a new blank database, which means
    there's no data in here yet!
    BIG TODO(ra): load data fixtures so we're not just testing against an empty db!
    """
    def setUp(self):
        self.analyzer = RereadingAnalysis()  # this loads all student responses from db at init time

    def test_total_view_time(self):
        """ tests for total_view_time method of RereadingAnalysis """
        total_view_time = self.analyzer.total_view_time()
        self.assertEqual(0, total_view_time)
