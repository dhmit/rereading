"""
Tests for the Rereading app.
"""

from django.test import TestCase

from .analysis import RereadingAnalysis, remove_outliers


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

    def test_frequency_feelings(self):
        """
        Tests for frequency_feelings method of Rereading Analysis
        """
        frequency_feelings = self.analyzer.frequency_feelings()
        self.assertEqual([], frequency_feelings)

    def test_compute_median_view_time(self):
        """
        Tests for compute_median_view_time method of Rereading Analysis
        """
        median_view_time = self.analyzer.compute_median_view_time()
        self.assertEqual(0, median_view_time)

    def test_mean_reading_time_for_a_question(self):
        """
        Test for mean_reading_time_for_a_question method of Rereading Analysis
        """
        mean_reading_time_for_a_question = self.analyzer.mean_reading_time_for_a_question("", "")
        self.assertEqual(["", "", 0, 0], mean_reading_time_for_a_question)

    def test_remove_outliers(self):
        """
        Test the remove_outlier functions on a list to see if it removes the outliers
        """
        outliers_data_1 = [-100, -50, 1, 2, 3, 4, 5, 100]
        outliers_data_2 = [1, 2, 3, 4, 5]

        outliers_data_3 = remove_outliers(outliers_data_1)
        print(outliers_data_3)
        self.assertEqual(outliers_data_3, outliers_data_2)
