"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
import statistics
import string
from collections import Counter, OrderedDict
from operator import itemgetter

from .models import (
    StudentReadingData,
    StudentSegmentData,
    SegmentQuestion,
    DocumentQuestion,
    DocumentQuestionResponse,
    SegmentQuestionResponse,
    Segment)
from .analysis_helpers import string_contains_words

# all relevant words used for two functions
RELEVANT_WORDS = ["stereotypes", "bias", "assumptions", "assume", "narrator", "memory",
                  "forget", "Twyla", "Maggie", "Roberta", "black", "white", "prejudice",
                  "mothers", "segregation", "hate", "hatred", "love", "love-hate",
                  "remember", "children", "recall", "kick", "truth", "dance", "sick",
                  "fade", "old", "Mary", "sandy", "race", "racial", "racism",
                  "colorblind", "disabled", "marginalized", "poor", "rich", "wealthy",
                  "middle-class", "working-class", "consumers", "shopping", "read",
                  "misread", "reread", "reconsider", "confuse", "wrong", "mistaken",
                  "regret", "mute", "voiceless", "women", "age", "bird", "time", "scene",
                  "setting", "Hendrix ", "universal", "binary", "deconstruct",
                  "question", "wrong", "right", "incorrect", "false", "claims", "true",
                  "truth", "unknown", "ambiguous", "unclear"]

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
             "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
             'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
             'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
             'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
             'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
             'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
             "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
             'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
             "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
             "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn',
             "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()\
            .prefetch_related('student',
                              'document')
        self.segments = StudentSegmentData.objects.all()\
            .prefetch_related('reading_data__document',
                              'segment')
        self.responses = SegmentQuestionResponse.objects.all()\
            .prefetch_related('student_segment_data__segment',
                              'question')
        self.doc_questions = DocumentQuestion.objects.all()
        self.doc_questions_response = DocumentQuestionResponse.objects.all()
        self.segment_questions = SegmentQuestion.objects.all()\
            .prefetch_related('segment')

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

    def compute_reread_counts(self):
        """"
        Given a list of student response dicts,
        return a dictionary containing the number of times students had to reread the text
        :return: int, number of times segment with sequence segment_number is reread
        """
        segment_dictionary = {}
        segment_list = []

        # For all segment objects
        for segments in self.segments:
            # Increment reread count in dictionary if the entry already in dictionary
            if (segments.segment.sequence in segment_dictionary and segments.view_time > 1.0 and
                    segments.is_rereading):
                segment_dictionary[segments.segment.sequence] += 1
            # Add entry to dictionary if entry does not already exist
            elif (segments.segment.sequence not in segment_dictionary and segments.view_time > 1.0
                  and segments.is_rereading):
                segment_dictionary[segments.segment.sequence] = 1

        # Turns dictionary data into a list of lists
        keys_list = list(segment_dictionary.keys())
        keys_list.sort()
        for key in keys_list:
            segment_list.append([key, round(segment_dictionary[key] / len(self.readings), 2)])

        return segment_list

    def relevant_words_by_question(self):
        """
            Return a list of tuples of the form (question,count), where count is
            the number of students who used relevant words in response to that question. This list
            is sorted by question
            :return the return type explained in the function description
        """

        question_context_count_map = {}
        for response in self.responses:
            question = response.question.text
            question_context_count_map[question] = question_context_count_map.get(question, 0) + 1
            if string_contains_words(response.response, RELEVANT_WORDS):
                question_context_count_map[question] += 1
        question_count_tup = list(question_context_count_map.items())
        return question_count_tup

    def relevant_words_percent_display_question(self):
        """
            Return a list of list which contains the question, the percentage, the count of total
            relevant words that a student used for the question, and a list of tuple inside each
            sublist with the words and the counts
            :return:the return type explained in the function description
        """
        # this is the combination + of the relevant words percentage and frequency function with
        # word frequency display. Need to resolve the duplicated code fragment later

        question_context_count_map = {} # show the relevant word usage with word frequency per
        # question
        question_count_map = {}
        for question in SegmentQuestion.objects.all():
            question_context_count_map[question] = {}

        for segment in self.responses:
            question = segment.question
            single_response = segment.response
            for word in single_response.split():
                if word in RELEVANT_WORDS:
                    question_context_count_map[question][word] = \
                        question_context_count_map[question].get(word, 0) + 1
                    question_context_count_map[question] = OrderedDict(sorted(
                        question_context_count_map[question].items(), key=itemgetter(1),
                        reverse=True))

            if string_contains_words(single_response, RELEVANT_WORDS):
                question_count_map[question] = question_count_map.get(question, 0) + 1
            else:
                question_count_map[question] = question_count_map.get(question, 0)

        total_student_count = len(self.readings)
        percent_question_count_map = {}
        for question in question_count_map:
            percent = "{:.2%}".format(round(
                (question_count_map[question] / total_student_count), 2))
            percent_question_count_map[question.text] = percent
        return_list = []
        for question in question_context_count_map:
            question_row = [
                question.text,
                percent_question_count_map[question.text],
                question_count_map[question],
                question_context_count_map[question],
            ]
            return_list.append(question_row)
        return return_list

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
        if num_students != 0:
            mean_reading_time = reading_time / num_students
            mean_rereading_time = rereading_time / num_students
        else:
            return 0.0, 0.0
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

    def percent_using_relevant_words_by_question(self):
        """
        Return a list of tuples with (question, percent), for each of the questions in the
        Segment Data and percent: percent of students who used relevant
        words in that question
        :return the return type explained in the function description
        """
        question_count_map = {}
        for segment in self.responses:
            question = segment.question
            if string_contains_words(segment.response, RELEVANT_WORDS):
                question_count_map[question] = question_count_map.get(question, 0) + 1
            else:
                question_count_map[question] = question_count_map.get(question, 0)

        total_student_count = len(self.readings)
        percent_question_count_map = []
        for question in question_count_map:
            percent_question_count_map.append(
                (question.text, question_count_map[question] /
                 total_student_count)
            )
        return [RELEVANT_WORDS, percent_question_count_map]



    def get_all_heat_maps(self):
        """
        This function shows a heat map for each segment. It will show how long in total was spent
        on different sections of the segment.
        :return: a dictionary of dictionaries which correspond to the view times of section of
        segments
        """
        heat_map = {}
        for segment in self.segments:
            segment_identifier = segment.reading_data.document.title + " " + \
                                 str(segment.segment.sequence)
            if segment_identifier not in heat_map:
                heat_map[segment_identifier] = {"reading": {}, "rereading": {}}
            for scroll_position in segment.get_parsed_scroll_data():
                if scroll_position < 0:
                    continue
                section_number = int(scroll_position) // 500
                section_identifier = str(section_number * 500) + " — " + \
                                     str((section_number + 1) * 500)
                is_rereading = "rereading" if segment.is_rereading else "reading"
                if section_identifier not in heat_map[segment_identifier][is_rereading]:
                    heat_map[segment_identifier][is_rereading][section_identifier] = 1
                else:
                    heat_map[segment_identifier][is_rereading][section_identifier] += 1
        return heat_map

    @staticmethod
    def get_number_of_segments():
        """
        Returns the number of segments.

        :return: int (number of segments)
        """
        return len(Segment.objects.all())

    def all_responses(self):
        """
        Returns a list of all of the responses in the DB, in the form:
        [Segment Num, Question Seq Num, Question Text, Response]

        :return: List of lists
        """

        responses = []
        responses_dict = {}

        for response in (
                self.responses.order_by(
                    'student_segment_data__segment__sequence',
                    'question__sequence',
                )
        ):
            segment_num = response.student_segment_data.segment.sequence
            question = response.question
            question_num = question.sequence

            question_text = question.text
            student_response = response.response
            evidence = response.parse_evidence()

            response_list = [
                segment_num,
                question_num,
                question_text,
                student_response,
                evidence,
            ]

            responses.append(response_list)

        for response in responses:
            response_list = [
                response[0],
                response[1],
                response[3],
                response[4],
            ]
            if response[2] in responses_dict:
                responses_dict[response[2]].append(response_list)
            else:
                responses_dict[response[2]] = []
                responses_dict[response[2]].append(response_list)

        collated_responses = []
        for question in responses_dict:
            segment_num = responses_dict[question][0][0]
            question_num = responses_dict[question][0][1]
            student_evidence = []

            for response in responses_dict[question]:
                student_evidence.append((response[2], response[3]))

            collated_responses.append([segment_num,
                                       question_num,
                                       question,
                                       student_evidence, ])

        return collated_responses

    def get_top_words_for_question(self, question):
        """
        Returns the top 3 most common words used to answer a question


        :param question: Question object
        :return: List of tuples in the form (response, frequency)
        """

        # Keep track of frequency of each response
        responses_frequency = Counter()

        # Get all responses to the given question, based on whether its a doc or segment question

        if isinstance(question, SegmentQuestion):
            # for res in self.responses:
            #     print(res.question.id == question.id)
            responses = filter(lambda x: x.question.id == question.id, self.responses)
        else:
            responses = filter(lambda x: x.question.id == question.id, self.doc_questions_response)

        # Iterate through and count all of the words in the responses
        for student_response in responses:
            student_answer_words = student_response.response.lower().split()
            filtered_words = filter(lambda x: x not in STOPWORDS and x not in string.punctuation,
                                    student_answer_words)
            for word in filtered_words:
                # If you wanted to, you can remove some of the punctuation attached to words here
                responses_frequency[word] += 1

        # Find the most common words for the question
        results_to_show = 5
        most_common_words = responses_frequency.most_common(results_to_show)

        # Turn the words into a string for it to display properly in the frontend
        words = ''
        for frequency_pair in most_common_words:
            word = frequency_pair[0]
            words += word + ', '

        # Strip the trailing whitespace and comma from the string of words
        words = words[:-2]
        return words

    def most_common_words_by_question(self):
        """
        Returns a dictionary mapping all question texts to their most common responses and
        frequencies

        :return: List of lists, where each inner list is a question. Lists are of the form
        [segment_num, question_num, question_text, responses]
        """
        # Initialize a list of lists to keep track of the top responses
        top_words = list()

        # Iterate through the questions to find the top response for each, and store it
        for question in self.doc_questions:
            top_question_words = self.get_top_words_for_question(question)
            question_text = question.text
            question_num = question.sequence
            data_list = ['Global', question_num, question_text, top_question_words]
            top_words.append(data_list)

        for question in self.segment_questions:
            top_question_words = self.get_top_words_for_question(question)
            question_text = question.text
            segment_num = question.segment.sequence
            question_num = question.sequence
            data_list = [segment_num, question_num, question_text, top_question_words]
            top_words.append(data_list)

        return top_words
