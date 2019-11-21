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
        self.readings = StudentReadingData.objects.all()
        self.segmentData = StudentSegmentData.objects.all()

    def run_compute_reread_counts(self):
        """
        Runs the analysis on the data loaded from the CSV file by looking at the reread count for
        each question and the context that the question was given in and
        prints it in a nice readable format.
        :return: the info wed like to put on js
        """
        questions = []
        contexts = []
        student_data = self.responses[:]
        for response in student_data:
            if response.question.text not in questions:
                questions.append(response.question.text)
            if response.context.text not in contexts:
                contexts.append(response.context.text)

        compute_reread_counts_data = []

        for question in questions:
            for context in contexts:
                compute_reread_counts_data.append(self.compute_reread_counts(
                    question, context))

        return compute_reread_counts_data

    def compute_reread_counts(self, question, context):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :param question: string, question for which reread counts is collected
        :param context: string, context for which reread counts is collected
        :return: dictionary, each key in dictionary is the number of times the text was reread
        and value is the number of students who reread that many times
        """

        # Checks that the question and context are not blank
        if question == '' or context == '':
            return {}

        # Collects the reread count for every student id of the provided context and question
        raw_reread_counts = []
        for row in self.responses:
            table_context = row.context.text
            table_question = row.question.text
            view_count = len(row.get_parsed_views())
            if context in table_context:
                if question in table_question:
                    raw_reread_counts.append(view_count)

        # Tallies the raw reread counts into the dictionary to be returned
        organized_data = {}
        mean_reread_count = 0
        sum_of_views = 0
        student_count = 0
        final_student_count = 0

        for entry in raw_reread_counts:
            if entry in organized_data.keys():
                organized_data[entry] += 1
            elif len(raw_reread_counts) != 0:
                organized_data.update({entry: 1})
        keys_of_dictionary = organized_data.keys()
        for entry in keys_of_dictionary:
            sum_of_views += entry * organized_data[entry]
            student_count += organized_data[entry]

        if student_count == 0:
            return 0
        else:
            mean_reread_count = round((sum_of_views / student_count), 2)
            sum_of_views = 0
            final_student_count = student_count
            student_count = 0

        print(organized_data)
        return [question, context, mean_reread_count, final_student_count]


