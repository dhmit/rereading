"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""

from .models import StudentReadingData, SegmentQuestionResponse


class RereadingAnalysis:
    """
    This class loads all StudentReadingData objects from the db,
    and implements analysis methods on these responses.
    """

    def __init__(self):
        self.readings = StudentReadingData.objects.all()

    @staticmethod
    def description_has_relevant_words(story_meaning_description, relevant_words):
        """
        Determine if the user's description contains a word relevant to the story's meaning
        :param story_meaning_description: The user's three word description of the story
        :param relevant_words: a list of words which show an understanding of the story's meaning
        :return True if the description contains one of the relevant words or relevant_words is
        empty. False otherwise
        """
        if not relevant_words:
            return True

        lowercase_relevant_words = []
        for word in relevant_words:
            lowercase_relevant_words.append(word.lower())

        words_used_in_description = story_meaning_description.lower().split(" ")

        for word in lowercase_relevant_words:
            if word.lower() in words_used_in_description:
                return True
        return False

    def relevant_words_by_question(self):
        """
            Return a list of tuples of the form (question,count), where count is
            the number of students who used relevant words in response to that question. This list
            is sorted by question
            :return the return type explained in the function description
        """
    relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                      "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]

    question_context_count_map = {}

    for q in SegmentQuestionResponse.objects.all():
        question = q.question.text
        question_context_count_map[question] = question_context_count_map.get(question,0)+1
        if description_has_relevant_words(q.response,relevant_words):
            question_context_count_map[question] += 1
            
    question_count_tup = [(question,count) for question, count in
                           question_context_count_map.items()]
    return question_count_tup

