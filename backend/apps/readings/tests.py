"""
Tests for the Rereading app.
"""

from django.test import TestCase

from .analysis import RereadingAnalysis


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

    def test_context_vs_read_time(self):
        """
        Tests for context_vs_read_time method of Rereading Analysis
        """
        mean_read_times = self.analyzer.context_vs_read_time()
        # Currently it is the default data, so there should be nothing there
        self.assertEqual({}, mean_read_times)

