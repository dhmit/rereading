"""

Analysis.py - initial analyses for dhmit/rereading

This module is too long, but that's okay for now -- we're shortly going to refactor!
"""

# pylint: disable=C0302
import statistics
import math
import csv
import unittest
from ast import literal_eval
from pathlib import Path
from statistics import stdev
from collections import defaultdict


def load_data_csv(csv_path: Path):
    """
    Takes the path to a csv file, reads it, and returns its
    content as a list of OrderedDicts
    :param Path csv_path: path to the CSV file
    :return: List[dict]
    """
    out_data = []
    with open(str(csv_path)) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row['views'] = literal_eval(row['views'])
            for header_name in ('id', 'student_id', 'scroll_ups'):
                row[header_name] = int(row[header_name])
            row = dict(row)
            out_data.append(row)
    return out_data

def clean_resp_strings(dataset):
    """
    Removes punctuation from responses in dataset and makes all characters lowercase.
    :param dataset: list of dictionaries, where each dictionary is one response (csv row)
    :return: a copy of dataset with no punctuation and all characters lowercase in the
    value keyed by 'response'
    """
    clean_dataset = []
    for resp in dataset:
        clean_dataset.append(resp)

    for clean_resp in clean_dataset:
        clean_resp['response'] = clean_resp['response'].replace('.', '').lower()
        clean_resp['response'] = clean_resp['response'].replace(',', '')

    return clean_dataset


def extract_responses_by_context(dataset):
    """
    Extracts text responses to "In three words or fewer, what is this text about?" from given csv
    file, depending on context given (story vs. ad). Returns lists of words used in question
    responses. Also removes duplicates.
    :param dataset: list of dictionaries, where each dictionary is one response (csv row)
    :return: response_ad and response_story, lists of strings of all words used in user responses
    (duplicates included)
    """
    # cycling through dataset to find prompt responses, sorting based on context
    responses_ad = []
    responses_story = []
    question = "In three words or fewer, what is this text about?"

    # removing punctuation and making lowercase
    clean_dataset = clean_resp_strings(dataset)  # removing punctuation and making lowercase
    for resp in clean_dataset:
        if resp['question'] == question and resp['context'] == "This is an ad.":
            responses_ad += resp['response'].split()
        elif resp['question'] == question and resp['context'] == "This is actually a short story.":
            responses_story += resp['response'].split()

    return responses_ad, responses_story


def repeated_prompt_words(responses):
    """
    Calculates frequencies of exact words from story prompt used in responses (disregards words
    not in story prompt).
    :param responses: list of words used in a set of responses
    :return: A dictionary, resp_words. Key is a word from the prompt, value is its frequency among
    responses
    """
    # dictionary to store frequencies of words in responses
    resp_words = {}

    # cycling through responses
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    for word in responses:
        print(word)
        if word in resp_words:
            resp_words[word] += 1
        elif word not in stop_words:
            resp_words[word] = 1

    # list of words in story
    # TODO for longer story, would want to read it from csv file instead of hardcoding
    story_vocab_list = ["for", "sale", "baby", "shoes", "never", "worn"]

    # eliminating all words not in prompt
    for word in responses:
        if word not in story_vocab_list and word in resp_words:
            del resp_words[word]

    # TODO Will add this to frontend to display data collected

    # uncomment for most commonly repeated word

    # print("Most commonly repeated words in response:")
    # print(max(resp_words.items(), key=lambda item: item[1]))

    # uncomment for complete list of words used in responses (unsorted)

    # print("All words in responses:")
    # print(resp_words)

    return resp_words


def compute_reread_counts(student_data, question, context):
    """"
    Given a list of student response dicts,
    return a dictionary containing the number of times students had to reread the text
    :param student_data: list, student response dicts
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
    for row in student_data:
        table_context = row['context']
        table_question = row['question']
        view_count = len(row['views'])
        if context in table_context:
            if question in table_question:
                raw_reread_counts.append(view_count)

    # Tallies the raw reread counts into the dictionary to be returned
    organized_data = {}
    for entry in raw_reread_counts:
        if entry in organized_data.keys():
            organized_data[entry] += 1
        elif len(raw_reread_counts) != 0:
            organized_data.update({entry: 1})

    return organized_data


def unique_word_pattern(student_data):
    """
    Take the list of dictionaries and analyze the readers' responses based on the two different
    contexts of the 2 questions (this is an ad/this is just a short story); analyze if the total
    number of unique responses changed as more and more readers' responses are analyzed.
    Eventually prints out the pattern along with the number of unique word in the text.

    :param student_data
    :return 2 lists of sets specifying unique responses at each point in time as a user
    submits a response
    """
    response_ad = set()
    response_story = set()
    unique_word_tracker_ad = []
    unique_word_tracker_story = []
    question = "In three words or fewer, what is this text about?"

    for data in student_data:
        filtered_word_resp = filter_words(data['response'])
        if data['question'] == question and data['context'] == "This is an ad.":
            word_set = response_ad
            histogram = unique_word_tracker_ad
        elif data['question'] == question and data['context'] == "This is actually a short story.":
            word_set = response_story
            histogram = unique_word_tracker_story
        else:
            continue
        for word in filtered_word_resp:
            word_set.add(word)
        histogram.append(set(word_set))

    return unique_word_tracker_story, unique_word_tracker_ad


def filter_words(string):
    """
    helper method to preprocess the string: remove the stopwords and punctuation
    return: list of words that are non-stopwords
    """
    stop_words_and_punct = ["i", "for", "in", "is", "are", "on", "are", "'s", ".", ","]
    return [ch for ch in string.lower().split() if ch not in stop_words_and_punct]


def get_sentiments() -> dict:
    """
    Returns a dictionary of sentiment scores, with the keys being the word
    and the values being their score

    :return: dict mapping words to their sentiment scores
    """
    sentiment_path = Path('data', 'sentiments.txt')

    sentiments = dict()
    with open(sentiment_path, 'r') as file:
        word = file.readline()

        # We want to handle each word individually, rather than as a whole set
        while word:

            # This particular file starts lines with '#' for non-sentiment comments, so skip them
            if word[0] == '#' or word[0] == '\t':
                word = file.readline()
                continue

            # All words use tabs to define the different parts of the data
            attributes = word.split('\t')

            # Pull out the word from the line
            data = attributes[4]
            data = data.split('#')
            new_word = data[0]
            positive_score = float(attributes[2])
            negative_score = float(attributes[3])

            # If the word is already in the dictionary, pick the larger value
            # This is not optimal, but standardizes data
            if new_word in sentiments:
                if abs(sentiments[new_word]) > abs(positive_score) and abs(sentiments[new_word]) > \
                                    abs(negative_score):
                    word = file.readline()
                    continue

            # Find the largest sentiment score for the word, and define negative sentiments
            # as negative values (if there's a tie, the sentiment is 0)
            if positive_score == negative_score:
                score = 0
            elif positive_score > negative_score:
                score = float(positive_score)
            else:
                score = -float(negative_score)

            sentiments[new_word] = score

            word = file.readline()

    return sentiments


def question_sentiment_analysis(student_data, question_text):
    """
    Takes in a list of student response dicts, and a question prompt (or a substring of one) and
    returns the average sentiment score and standard deviation for all responses to that question

    :param student_data: list of dicts
    :param question_text: question string or substring
    :return: tuple in the form (average, standard_dev)
    """

    sentiments = get_sentiments()

    # Set up data for calculating data
    num_scores = 0
    sentiment_sum = 0
    score_list = list()

    for response in student_data:

        if question_text in response['question']:
            words = response['response'].lower().split()

            # Find the sentiment score for each word, and add it to our data
            for word in words:
                # Ignore the word if it's not in the sentiment dictionary
                if word in sentiments:
                    sentiment_sum += sentiments[word]
                    num_scores += 1
                    score_list.append(sentiments[word])

    average = sentiment_sum / num_scores
    standard_dev = stdev(score_list)

    return average, standard_dev


def word_time_relations(student_data: list) -> dict:
    """
    Takes a list of dicts representing student data and aggregates case-insensitive responses
    into a dictionary, with the response as the key and the average time (across all similar
    responses) viewing the story as the value.

    :param student_data: list of dicts obtained from load_data_csv
    :return: dict, responses as keys and values as average view times for that response
    """

    # First gather all responses in an easy-to-handle format of dict(response: times)
    responses = dict()
    for response_data in student_data:

        # Find total time spent looking at story
        total_time = 0
        for view in response_data['views']:
            total_time += view

        # Add this time to the response dictionary (case-insensitive)
        response = response_data['response'].lower()
        if response not in responses:
            responses[response] = [total_time]
        else:
            responses[response].append(total_time)

    # Now compute the average time for each response and add them to a new dictionary
    averages = dict()
    for response in responses:
        times = responses[response]
        total = sum(times)
        average = total / len(times)
        averages[response] = average

    return averages


def compute_total_view_time(student_data):
    """
    Given a list of student response dicts,
    return the total time (across all users) spent reading the text
    """
    total_view_time = 0
    for row in student_data:
        for view_time in row.get('views'):
            total_view_time += view_time
    return total_view_time


def compute_mean_reading_times_each_response(student_data):
    """
    For each rereading, compute the mean response time across all students
    by summing the durations of each round of reading and dividing each sum
    by the total number of participants.
    :param student_data: list of OrderedDicts, set of responses
    :return a list containing 1) total number of participants,
    2) the mean reading time for the first response, and
    3) the mean reading time for the second response.
    """
    total_first_response = 0
    total_second_response = 0
    total_participants = 0
    last_student_id = -1  # value not present in the data
    for line in student_data:
        context = line["context"]
        question = line["question"]
        student_id = line["student_id"]
        if question == "In one word, how does this text make you feel?":
            if context == 'This is an ad.':
                for duration in line["views"]:
                    total_first_response += duration
            elif context == "This is actually a short story.":
                for duration in line["views"]:
                    total_second_response += duration
        if student_id != last_student_id:
            total_participants += 1
            last_student_id = student_id

    if total_participants == 0:
        return []
    mean_first_response = total_first_response / total_participants
    mean_second_response = total_second_response / total_participants
    result = [total_participants, mean_first_response, mean_second_response]
    return result


def get_responses_for_question(student_data, question):
    """
    For a certain question, returns the set of responses as a dictionary with keys being the
    context and values being nested dictionaries containing each response and their frequency.
    :param student_data: list of OrderedDicts, set of responses
    :param question: string, question
    :return: dictionary mapping strings to integers
    """
    responses = {}
    for elem in student_data:
        student_question = elem['question']
        student_response = elem['response'].lower()
        question_context = elem['context']
        if student_question == question:
            if question_context not in responses:
                responses[question_context] = {student_response: 1}
            else:
                if student_response in responses[question_context]:
                    responses[question_context][student_response] += 1
                else:
                    responses[question_context][student_response] = 1
    return responses


def most_common_response(student_data, question, context):
    """
    Returns a list of the most common response(s) given a set of data, a question, and a context.
    :param student_data: list of OrderedDicts, student response data
    :param question: string, question
    :param context: string, context
    :return: list of strings
    """
    max_response = []
    response_dict = get_responses_for_question(student_data, question)
    responses_by_context = response_dict[context]
    max_response_frequency = max(responses_by_context.values())
    for response in responses_by_context:
        if responses_by_context[response] == max_response_frequency:
            max_response.append(response)
    return max_response


def get_word_frequency_differences(student_data):
    """
    Looks over the data and compares responses from people who have read the text vs.
    people who have not read the text before this exercise
    :return: a list of word frequency differences, by increasing order of frequency differences
    """

    # Iterate through all data, and separate ids of students who have vs. have not read the text
    yes_id = []
    no_id = []

    for response in student_data:
        if 'Have you encountered this text before' in response['question'] \
                            and 'This is an ad.' in response['context']:
            if 'yes' not in response['response'].lower():
                no_id.append(response['student_id'])
            else:
                yes_id.append(response['student_id'])

    # Iterate through all responses, store words and word frequencies of yes vs. no responses as
    # keys and values in 2 dictionaries

    yes_responses = dict()
    no_responses = dict()

    for element in student_data:
        if 'In one word' in element['question'] and 'This is an ad' in element['context']:
            response = element['response'].lower()
            if element['student_id'] in yes_id:
                if response in yes_responses:
                    yes_responses[response] += 1
                else:
                    yes_responses[response] = 1
            else:
                if response in no_responses:
                    no_responses[response] += 1
                else:
                    no_responses[response] = 1

    # Iterate through yes_responses and no_responses, store words and frequency differences as keys
    # and values of a dictionary
    diff_responses = dict()

    for word in yes_responses:
        if word in no_responses:
            diff_responses[word] = yes_responses[word] - no_responses[word]
        else:
            diff_responses[word] = yes_responses[word]
    for word in no_responses:
        if word not in yes_responses:
            diff_responses[word] = - no_responses[word]

    # Convert diff_responses from a dictionary to a list of tuples
    diff_responses_list = []
    for word in diff_responses:
        diff_responses_list.append((word, diff_responses[word]))

    # Order diff_responses and return ordered list
    ordered_responses = sorted(diff_responses_list, key=lambda x: x[1])
    return ordered_responses


def mean_view_time_sentiment_comparison(student_data):
    """
    Calculate the mean view time of three groups (those who had a negative-word response, a
    neutral-word response, and a positive-word response) for comparison.
    :param student_data: a list of dictionaries
    :return: a tuple of floats, the mean view times of negative, neutral, and positive
            respectively.
    """
    negative_total_view_time = 0
    neutral_total_view_time = 0
    positive_total_view_time = 0
    negative_responses = 0
    neutral_responses = 0
    positive_responses = 0
    for response_dict in student_data:
        if (response_dict['question'] == 'In three words or fewer, what is this text about?') \
                and (response_dict['context'] == 'This is an ad.'):
            response: str = response_dict['response'].lower()
            response_rank = sentiment_of_a_response(response)
            if response_rank == -1:
                negative_responses += 1
                negative_total_view_time += sum(response_dict['views'])
            elif response_rank == 1:
                positive_responses += 1
                positive_total_view_time += sum(response_dict['views'])
            else:
                neutral_responses += 1
                neutral_total_view_time += sum(response_dict['views'])
    if negative_responses == 0:
        negative_mean_view_time = 0
    else:
        negative_mean_view_time = negative_total_view_time / negative_responses
    if positive_responses == 0:
        positive_mean_view_time = 0
    else:
        positive_mean_view_time = positive_total_view_time / positive_responses
    if neutral_responses == 0:
        neutral_mean_view_time = 0
    else:
        neutral_mean_view_time = neutral_total_view_time / neutral_responses
    return negative_mean_view_time, neutral_mean_view_time, positive_mean_view_time


def sentiment_of_a_response(response):
    """
    Calculate the sentiment score for each word in a response and takes the extreme-most
    score across all words in teh response to determine whether the response is negative,
    neutral, or positive
    :param response: a string
    :return: an int -1, 0, or 1 corresponding to whether the response is deemed negative,
    neutral, or positive
    """
    dict_sentiments = get_sentiments()
    response_list = response.split()
    response_sentiment_list = []
    for word in response_list:
        if word in dict_sentiments:
            response_sentiment_list.append(dict_sentiments[word])
        else:
            response_sentiment_list.append(0)
    sentiment_score = max(response_sentiment_list, key=abs)
    if sentiment_score < 0:
        return -1
    elif sentiment_score > 0:
        return 1
    else:
        return 0


def compute_median_view_time(student_data):
    """
     Given a list of student response dicts,
    return the median time (across all users) spent reading the text

    :param student_data: list, student response dicts
    :return: float, median amount of time users spend reading the text
    """
    list_of_times = []
    for row in student_data:
        for view_time in row.get('views'):
            list_of_times.append(view_time)
    if not list_of_times:
        median_view_time = 0
    else:
        list_of_times.sort()
        median_view_time = statistics.median(list_of_times)
    return median_view_time


def compute_mean_response_length(student_data):
    """
    Given a list of student response dicts,
    return the mean character length (across all users) of the response

    :param student_data: list, student response dicts
    :return: float, mean number of characters in the user's response
    """

    list_of_responses = []
    for row in student_data:
        list_of_responses.append(row.get("response"))
    mean_response_length = 0
    for response in list_of_responses:
        mean_response_length += len(response)
    return mean_response_length / len(list_of_responses)


def run_time_analysis_functions(student_data):
    """
    Runs analysis functions related to the time students took to read the passage
    :param student_data: the data to analyze
    Runs the analytical method on the reading data
    :return: None
    """
    median_view_time = compute_median_view_time(student_data)
    total_view_time = compute_total_view_time(student_data)
    mean_response_length = compute_mean_response_length(student_data)
    print(f'The total view time of all students was {total_view_time}.')
    print(f'The median view time of all students was {median_view_time}.')
    print(f'The mean response length of all students was {mean_response_length} characters.')


def description_has_relevant_words(story_meaning_description, relevant_words):
    """
    Determine if the user's description contains a word relevant to the story's meaning
    :param story_meaning_description: The three word description of the story that the user supplied
    :param relevant_words: a list of words which show an understanding of the story's meaning
    :return True if the description contains one of the relevant words or relevant_words is empty.
        False otherwise
    """
    if len(relevant_words) == 0:
        return True

    lowercase_relevant_words = list(map(lambda s: s.lower(), relevant_words))
    words_used_in_description = story_meaning_description.lower().split(' ')

    for word in lowercase_relevant_words:
        if word.lower() in words_used_in_description:
            return True
    return False


def percent_students_using_relevant_words(student_data, target_context, relevant_words):
    """
    Find the percentage of students that used relevant words in their responses
    :param student_data: the data to analyze
    :param target_context: the context (e.g. "This is an ad") to take responses from
    :param relevant_words: a list of words which show an understanding of the story's meaning
    :return: The percentage [0.00, 1.00] of students that used relevant words in their
    responses. 0 if there are no responses.
    """
    number_of_students_using_relevant_words = 0
    total_students = 0
    for row in student_data:
        if (row.get('context') == target_context and
                row.get('question') == 'In three words or fewer, what is this text about?'):
            total_students += 1
            if description_has_relevant_words(row.get('response'), relevant_words):
                number_of_students_using_relevant_words += 1

    if total_students:
        percentage_of_all_students = number_of_students_using_relevant_words / total_students
    else:
        percentage_of_all_students = 0
    return percentage_of_all_students


def run_relevant_word_analysis(student_data):
    """
    Runs analysis functions related to the relevancy of words students wrote in their responses
    :param student_data: the data to analyze
    """
    target_context = 'This is actually a short story.'
    relevant_words_file_path = 'data/words_related_to_story.txt'
    relevant_words_file = open(relevant_words_file_path, 'r')
    untrimmed_relevant_words = relevant_words_file.readlines()
    relevant_words = list(map(lambda s: s.strip(), untrimmed_relevant_words))

    relevant_words_used_percent = percent_students_using_relevant_words(
        student_data, target_context, relevant_words)
    print(f'{relevant_words_used_percent * 100}% of students used words related to '
          f'the story\'s intended meaning.')


def run_analysis():
    """
    Runs analysis given student data
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    mean_view_time_sentiment_comparison(student_data)
    reread_counts = compute_reread_counts(student_data, "In one word", "ad")
    print("Number of times students reread text based on question or context:\n")
    print(reread_counts)

    response_groups_freq_dicts = get_response_groups_frequencies(student_data)
    show_response_groups(response_groups_freq_dicts)
    run_time_analysis_functions(student_data)
    run_relevant_word_analysis(student_data)

    total_view_time = compute_total_view_time(student_data)
    print(f'The total view time of all students was {total_view_time}.')
    print(f'Mean number of revisits per unique question: ', compute_mean_revisits(student_data))
    print(f'Median number of revisits per unique question: ', compute_median_revisits(student_data))
    print(
        get_responses_for_question(student_data, "In one word, how does this text make you feel?"))
    print(most_common_response(
        student_data,
        "In one word, how does this text make you feel?",
        "This is an ad."
    ))
    print(unique_word_pattern(student_data)[0])
    print(unique_word_pattern(student_data)[1])


def compute_mean_revisits(data):
    """
    Returns the mean count of revisits per question

    :param data: list, student response dict
    :return: dict, Key = question, string. Value = average number of revisits, float.
    """
    results = {}

    # Accumulates the total views and number of responses per unique question
    for entry in data:
        question = entry['question']
        num_views = len(entry['views'])
        result = results.get(question)
        if result:
            view_count, view_sum = result
            view_count += 1
            view_sum += num_views
            results[question] = [view_count, view_sum]
        else:  # Create a key with starting values
            results[question] = [1, num_views]

    # Averages the number of revisits per unique question
    for question in results:
        total_count, total_views = results[question]
        views_per_count = total_views / total_count
        results[question] = round(views_per_count, 2)

    return results


def compute_median_revisits(data):
    """
    Returns the median count of revisits per unique question

    :param data: list, student responses
    :return: dict, key = question, string. value = median, int.
    """
    results = {}

    # Append number of revisits into a list per unique question
    for entry in data:
        question = entry['question']
        num_views = len(entry['views'])
        result = results.get(question)
        if result:
            result.append(num_views)
        else:  # Create the key with the list
            results[question] = [num_views]

    # Compute the median count of revisits per unique question
    for question in results:
        results[question] = statistics.median(results[question])

    return results


def context_vs_read_time(student_data):
    """
    compares average viewtimes, given different context (ad vs story)
    :param student_data: list, student response dicts
    :return a tuple of the average ad view and the average story view
    """
    ad_sum = 0
    ad_count = 0
    story_sum = 0
    story_count = 0

    for row in student_data:
        if row['context'] == "This is an ad.":
            if len(row["views"]) != 0:
                for view in row["views"]:
                    ad_sum = ad_sum + view
            ad_count += 1
        elif row["context"] == "This is actually a short story.":
            if len(row["views"]) != 0:
                for view in row["views"]:
                    story_sum = story_sum + view
            story_count += 1

    if ad_count == 0:
        mean_ad_view = 0
    else:
        mean_ad_view = ad_sum / ad_count
    if story_count == 0:
        mean_story_view = 0
    else:
        mean_story_view = story_sum / story_count

    return mean_ad_view, mean_story_view


def frequency_feelings(student_data):
    """
    :param student_data: list, student response dicts
    :return a list of tuples of words that appear more than once, and how often they occur,
    in order of their frequency
    """
    feelings = {}
    for row in student_data:
        if row['question'] == "In one word, how does this text make you feel?":
            lower_case_word = row['response'].lower()
            if feelings.get(lower_case_word, 0) == 0:
                feelings[lower_case_word] = 1
            else:
                feelings[lower_case_word] += 1

    frequent_words = []  # list of tuples in the format (frequency, word)
    for word in feelings:
        if feelings[word] > 1:
            frequent_words.append((word, feelings[word]))

    print(frequent_words)

    for i in range(len(frequent_words) - 1):
        for j in range(i + 1, len(frequent_words)):
            if (frequent_words[i])[1] < (frequent_words[j])[1]:
                frequent_words[i], frequent_words[j] = frequent_words[j], frequent_words[i]

    print(frequent_words)
    return frequent_words


def run_mean_reading_analysis_for_questions(student_data):
    """
    Runs the analysis on the data loaded from the CSV file by looking at the average
    read time for each question and the context that the question was given in and
    prints it in a nice readable format.
    :return: None
    """
    question_one = "In one word, how does this text make you feel?"
    question_two = "In three words or fewer, what is this text about?"
    question_three = "Have you encountered this text before?"

    mean_reading_time_results_data = [
        mean_reading_time_for_a_question(student_data, question_one, "ad"),
        mean_reading_time_for_a_question(student_data, question_two, "ad"),
        mean_reading_time_for_a_question(student_data, question_three, "ad"),
        mean_reading_time_for_a_question(student_data, question_one, "short story"),
        mean_reading_time_for_a_question(student_data, question_two, "short story"),
        mean_reading_time_for_a_question(student_data, question_three, "short story")
    ]

    for reading_result in mean_reading_time_results_data:
        if reading_result[3] != 0:
            print(f"Out of those who thought the reading was a(n) {reading_result[1]}"
                  f"and were asked {reading_result[0]}\"")
            print(
                f"{reading_result[3]} subject(s) read the text for an average of "
                f"{round(reading_result[2], 3)} seconds.")
        else:
            print(f"No one who thought the reading was a(n) {reading_result[1]} and were asked "
                  f"\"{reading_result[0]}\" read the text.")
        print("")


def mean_reading_time_for_a_question(student_data, question, context):
    """
    Given the student response dicts, computes the mean read time for a
    specific question (given by its keyword) and the context in which it was asked.
    Returns the question, context, mean read time, and number of people who read.
    :param student_data: list, student response dicts
    :param question: string, to determine which question was being asked
    :param context: string, what the reader thought the reading was
    :return: tuple, in order of the question asked (full question), the context, the mean read
             time, and the number of people who read it
    """
    mean_time = 0
    number_of_readers = 0
    question_count = 0
    reading_time = []
    total_question_view_time = 0

    for student_data_dictionary in student_data:
        if question != student_data_dictionary['question'] or \
                context != student_data_dictionary['context']:
            continue
        if len(student_data_dictionary['views']) != 0:
            number_of_readers += 1
        for view_time in student_data_dictionary['views']:
            reading_time.append(view_time)

    if len(reading_time) != 0:
        remove_outliers(reading_time)

    view_time = 0
    while view_time < len(reading_time):
        question_count += 1
        total_question_view_time += reading_time[view_time]
        view_time += 1

    if len(reading_time) != 0:
        mean_time = round(total_question_view_time / len(reading_time), 2)

    return question, context, mean_time, number_of_readers


def remove_outliers(reading_time):
    """
    Given a list of times, calculates and removes outliers, which are the data points that
    are outside the interquartile range of the data
    :param reading_time: list, reading times for a specific question
    :return: list, reading times for a specific question with outliers removed
    """
    reading_time.sort()
    quartile_one = reading_time[math.trunc(len(reading_time) * 0.25)]
    quartile_three = reading_time[math.trunc(len(reading_time) * 0.75)]
    interquartile_range = quartile_three - quartile_one
    lower_fence = quartile_one - (1.5 * interquartile_range)
    upper_fence = quartile_three + (1.5 * interquartile_range)

    view_time_two = 0
    while view_time_two < len(reading_time):
        if (reading_time[view_time_two] < lower_fence) \
                                or (reading_time[view_time_two] > upper_fence):
            reading_time.remove(reading_time[view_time_two])
            view_time_two -= 1
        else:
            view_time_two += 1

    return reading_time


def mean_reading_time(data):
    """
    Takes the data and finds the mean time of all the view times in the data
    :param data: list of responses
    :return: float representing the average view times
    :return: None when there are no entries for viewing time
    """
    times = 0
    count = 0
    for dictionary in data:
        views = dictionary["views"]
        for view in views:
            times += view
            count += 1
    if count == 0:
        return None
    return times / count


def mean_reading_time_student(data, student_id):
    """
    Takes the data and an id and computes the average time overall of the entry with that id
    :param student_id: integer, represents specific id number of student
    :param data: list of responses
    :return: float: represents the average view time of the student with this id
    :return: None: when there is no data entries for this specific id
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_id = dictionary["student_id"]
        if dict_id == student_id:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times / count


def mean_reading_time_question_context(data, question, context):
    """
    Takes the data, a question, and context and computes the average time of the
    views of this specific context and question
    :param question: String representing a specific question
    :param context: String representing a specific context
    :param data: list of responses
    :return: float: represents the average view time spent on this specific question and context
    :return: None: when there is no data entries for this specific question and context
    """
    count = 0
    times = 0
    for dictionary in data:
        dict_question = dictionary["question"]
        dict_context = dictionary["context"]
        if dict_question == question and dict_context == context:
            for view in dictionary["views"]:
                count += 1
                times += view
    if count == 0:
        return None
    return times / count


def frequent_responses(freq_dict):
    """
    Takes in a dictionary with values that are frequency dictionaries
    Returns a dictionary showing the most frequent responses to each specific question/context
    combination
    :param freq_dict: dictionary, A dictionary with tuples as keys and a
    frequency dictionary as values.
    :return: dictionary, A dictionary with tuples as keys and a dictionary as values.
    The values are dictionaries with different information about the most frequent responses
    such as a list of the most common responses as well as the number of times they occurred
    """
    output = {}
    for key in freq_dict:
        details = {}
        a_freq_dict = freq_dict[key]
        max_occurrences = 0
        max_list = []
        for word in a_freq_dict:
            occurrence = a_freq_dict[word]
            if occurrence > max_occurrences:
                max_occurrences = occurrence
                max_list = [word]
            elif occurrence == max_occurrences:
                max_list.append(word)
        details['most_frequent_words'] = max_list
        details['max_occurrences'] = max_occurrences
        output[key] = details
    return output


def word_freq_all(data):
    """
    Takes in the list of responses
    Returns a dictionary linking question/context combinations to a frequency dictionary
    :param data: list, A list of all of the data entries from the survey
    :return: dictionary, A dictionary with a tuple of the question and
    context as keys and with a frequency dictionary as values
    """
    output = {}
    for entry in data:
        the_key = (entry["question"], entry["context"])
        if the_key not in output:
            output[the_key] = {}
        qc_dict = output[the_key]
        response = entry['response'].lower()
        if response not in qc_dict:
            qc_dict[response] = 1
        else:
            qc_dict[response] += 1
    return output


def show_response_groups(response_groups_freq_dicts):
    """
    Given response_groups_freq_dicts list of dictionaries, prints the dicts in readable format
    :param response_groups_freq_dicts, lists of 4 dicts (one for each response
    group)
    mapping words to frequencies within that response group
    :return None
    """
    print(f'Word frequencies for Single view responses to ad context: ',
          response_groups_freq_dicts[0])
    print(f'Word frequencies for Single view responses to short story context: ',
          response_groups_freq_dicts[1])
    print(f'Word frequencies for Multiple view responses to ad context: ',
          response_groups_freq_dicts[2])
    print(f'Word frequencies for Multiple view responses to short story context: ',
          response_groups_freq_dicts[3])


def get_response_groups_frequencies(student_data: list):
    """"
    Given student_data,
    Returns lists of 4 frequency dicts, one for each response group,
     that map response words to frequencies for each response group.
    Response groups are based on single vs. multiple views and ad vs. short story
    context to the "In one word, how does this text make you feel?" question
    :param student_data, list of dicts
    :return: list of four dicts (one for each response group) mapping words
    to frequencies within that response group
    """
    people_with_multiple_views = []
    people_with_one_view = []

    for person_response in student_data:
        if len(person_response['views']) == 1:
            people_with_one_view.append(person_response)
        else:
            people_with_multiple_views.append(person_response)

    single_view_short_story_group, single_view_ad_group = \
        get_groups_by_context(people_with_one_view)
    multiple_view_short_story_group, multiple_view_ad_group = \
        get_groups_by_context(people_with_multiple_views)

    response_groups = [
        single_view_ad_group,
        single_view_short_story_group,
        multiple_view_ad_group,
        multiple_view_short_story_group,
    ]

    response_groups_freq_dicts = []
    for group_name in response_groups:
        freq_dict = find_word_frequency(group_name)
        response_groups_freq_dicts.append(freq_dict)
    return response_groups_freq_dicts


def get_groups_by_context(people_with_view_number):
    """
    :param people_with_view_number: list of responses for people with certain number of views
    :return: two lists, one for responses to short story context and one for ad context
    """
    short_story_context_group = []
    ad_context_group = []
    for person in people_with_view_number:
        if person['question'] == "In one word, how does this text make you feel?":
            response = person['response'].lower()
            if person['context'] == "This is actually a short story.":
                short_story_context_group.append(response)
            else:
                ad_context_group.append(response)
    return short_story_context_group, ad_context_group


def find_word_frequency(response_list):
    """
    :param response_list: list of single-word str
    :return: freq, dict mapping each unique word in response_list to number of appearances in
    response_list
    """
    freq = {}
    for word in response_list:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


def compute_view_time_per_response(student_data):
    """
    Compute the total reread times for each response
    :param student_data: list, student response dicts
    :return:
    wanted_dict_ad - Dictionary ('ad context response in lowercase': [total reading times for
        each user])
    wanted_dict_ss - Dictionary ('short story context response in lowercase': [total reading
        times for each user])
    """

    wanted_dict_ad = defaultdict(list)
    wanted_dict_ss = defaultdict(list)

    for entry in student_data:
        if entry['question'] == 'In one word, how does this text make you feel?':
            response = entry['response'].lower()
            views = sum(entry['views'])

            if entry['context'] == 'This is an ad.':
                wanted_dict_ad[response].append(views)

            elif entry['context'] == 'This is actually a short story.':
                wanted_dict_ss[response].append(views)

    return {'This is an ad.': wanted_dict_ad, 'This is actually a short story.': wanted_dict_ss}


def get_common_elements(ad_response_times, ss_response_times):
    """
    Take two dictionaries of key: float pairs and return the keys common between the two
    dictionaries with the mean of the two values.
    :param ad_response_times: the first dictionary to compare
    :param ss_response_times: the second dictionary to compare
    :return: one dictionary
    """
    # Start making a combined dictionary that does not separate based on context
    wanted_dict_combined = {}
    for word in ad_response_times.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_combined[word] = ad_response_times[word]

    # Continue building the combined dictionary with short story dictionary
    for word in ss_response_times.keys():
        # Take the mean of the current response with new data
        if word in wanted_dict_combined.keys():
            wanted_dict_mean = (wanted_dict_combined[word] + ss_response_times[word]) / 2
            wanted_dict_combined[word] = wanted_dict_mean

        # Add the new data
        else:
            wanted_dict_combined[word] = ss_response_times[word]

    return wanted_dict_combined


def reread_time_difference(ad_response_times, ss_response_times):
    """
    make a dictionary of which context had a longer reread time for each response and the difference
    :param ad_response_times: dictionary of ad response times
    :param ss_response_times: dictionary of ss response times
    :return: dict{response:[context,time]}
    """
    wanted_dict_difference = {}

    for word in ad_response_times.keys():
        if word in ss_response_times.keys():
            if ad_response_times[word] > ss_response_times[word]:
                wanted_difference = ad_response_times[word] - ss_response_times[word]
                wanted_dict_difference[word] = ["ad", wanted_difference]

            else:
                wanted_difference = ss_response_times[word] - ad_response_times[word]
                wanted_dict_difference[word] = ["short story", wanted_difference]

    return wanted_dict_difference


def total_reading_time_exclusive(wanted_dict_ad, wanted_dict_ss):
    """
    returns two dictionaries of the exclusive key:value pairs between two dictionaries
    :param wanted_dict_ss: the first dictionary to compare
    :param wanted_dict_ad: the second dictionary to compare
    :return: 2 dictionaries
    """
    # Make a dictionary of the responses used in ad context that were not used in short story
    # context and their total reading times
    wanted_dict_combined = get_common_elements(wanted_dict_ad, wanted_dict_ss)
    wanted_dict_ad_exclusive = defaultdict(list)
    wanted_dict_ss_exclusive = defaultdict(list)

    for word in wanted_dict_ad.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ad_exclusive[word].append(wanted_dict_ad[word])

    # Make a list of the responses used in short story context that were not used in ad context
    # and their total reading times
    for word in wanted_dict_ss.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ss_exclusive[word].append(wanted_dict_ss[word])

    return {
        'This is an ad.': wanted_dict_ad_exclusive,
        'This is actually a short story.': wanted_dict_ss_exclusive,
    }


def build_mean_dict(input_dict):
    """
    Given a dictionary with a list of floats for values, return a dictionary with the same keys and
    the mean of the values
    :param input_dict: dictionary {key:[values]}
    :return: dictionary {key: float}
    """
    output_dict = {}
    for key in input_dict.keys():
        output_dict[key] = sum(input_dict[key]) / len(input_dict[key])

    return output_dict


class TestAnalysisMethods(unittest.TestCase):
    """
    Test cases to make sure things are running properly
    """

    def setUp(self):
        """
        Sets up the data sets for testing
        """
        test_data_path = Path('data', 'test_data.csv')
        self.test_student_data = load_data_csv(test_data_path)
        self.default_student_data = [  # model default values
            {
                'id': 0,
                'question': '',
                'context': '',
                'response': '',
                'views': [],
                'student_id': 0,
                'scroll_ups': 0,
            }
        ]
        test_data_2_path = Path('data', 'test_data_2.csv')
        self.default_student_data_2 = load_data_csv(test_data_2_path)
        sample_csv_path = Path('data', 'rereading_data_2019-09-13.csv')
        self.student_data = load_data_csv(sample_csv_path)
        test_data_3_path = Path('data', 'test_data_3.csv')
        self.default_student_data_3 = load_data_csv(test_data_3_path)
        self.feel = "In one word, how does this text make you feel?"
        self.about = "In three words or fewer, what is this text about?"
        self.encountered = "Have you encountered this text before?"
        self.ads = "This is an ad."
        self.short_story = "This is actually a short story."


    def test_unique_words_pattern(self):
        """
        Tests unique_words_pattern function with two data sets. The first is
        the default empty dataset and the second is test_data2 which is a small dataset.
        This function tests that it correctly appends the lists of unique words to both
        ads response and story response lists the total unique words in each
        timestamp. Future testing is suggested using larger datasets.
        """

        # first check: empty dataset
        unique_words_story, unique_words_ad = unique_word_pattern(self.default_student_data)
        set_unique_words_story = len(unique_words_story)
        set_unique_words_ad = len(unique_words_ad)
        self.assertEqual(set_unique_words_story, 0)
        self.assertEqual(set_unique_words_ad, 0)

        # second check: smaller dataset
        unique_words_story1, unique_words_ads1 = unique_word_pattern(self.test_student_data)
        set_unique_words_story1 = len(unique_words_story1)
        set_unique_words_ad1 = len(unique_words_ads1)
        self.assertEqual(set_unique_words_story1, 1)
        self.assertEqual(set_unique_words_ad1, 1)


    def test_mean_view_time_sentiment_comparison(self):
        """
        Tests mean_view_time_sentiment_comparison function with two data sets. The first is
        specific to
        our function and the second is generic and just an empty set. It tests that it correctly
        calculates the mean and doesn't break when dividing by 0.
        Comment: this Function uses the Sentiment dictionary, such that 'miscarriage' is considered
        a neutral response and 'Giving up hope' is considered a positive response
        :return:
        """
        total_mean_view_time_sentiment_comparison = mean_view_time_sentiment_comparison(
            self.default_student_data_3)
        self.assertEqual((0.0, 0.9645714285714285, 0.0), total_mean_view_time_sentiment_comparison)
        total_mean_view_time_sentiment_comparison = mean_view_time_sentiment_comparison(
            self.default_student_data)
        self.assertEqual((0, 0, 0), total_mean_view_time_sentiment_comparison)

    def test_extract_responses_by_context(self):
        """
        Tests that the extract_responses_by_context() function correctly extracts words from
        different context responses. Tests against test_data.csv and the default dataset.
        """
        # testing against test_data.csv
        test_ad_resp, test_story_resp = extract_responses_by_context(self.test_student_data)
        expected_ad_resp = ["miscarriage"]
        expected_story_resp = ["miscarriage"]

        self.assertEqual(test_ad_resp, expected_ad_resp)
        self.assertEqual(test_story_resp, expected_story_resp)

        # testing against default dataset
        test_ad_resp, test_story_resp = extract_responses_by_context(self.default_student_data)
        expected_ad_resp = []
        expected_story_resp = []

        self.assertEqual(test_ad_resp, expected_ad_resp)
        self.assertEqual(test_story_resp, expected_story_resp)

    def test_repeated_prompt_words(self):
        """
        Tests that the repeated_prompt_words() function returns the right repeated word counts for
        the story text. Tests against test_data.csv, the default dataset, and the small student
        dataset.
        """
        # testing against test_data.csv
        test_ad_resp, test_story_resp = extract_responses_by_context(self.test_student_data)
        test_ad_words = repeated_prompt_words(test_ad_resp)
        test_story_words = repeated_prompt_words(test_story_resp)
        expected_ad_words = {}
        expected_story_words = {}

        self.assertEqual(test_ad_words, expected_ad_words)
        self.assertEqual(test_story_words, expected_story_words)

        # testing against default dataset
        test_ad_resp, test_story_resp = extract_responses_by_context(self.default_student_data)
        test_ad_words = repeated_prompt_words(test_ad_resp)
        test_story_words = repeated_prompt_words(test_story_resp)
        expected_ad_words = {}
        expected_story_words = {}

        self.assertEqual(test_ad_words, expected_ad_words)
        self.assertEqual(test_story_words, expected_story_words)

        # testing against small rereading dataset
        test_ad_resp, test_story_resp = extract_responses_by_context(self.student_data)
        test_ad_words = repeated_prompt_words(test_ad_resp)
        test_story_words = repeated_prompt_words(test_story_resp)
        expected_ad_words = {'baby': 9, 'shoes': 12, 'sale': 4}
        expected_story_words = {'baby': 4, 'shoes': 6, 'sale': 2}

        self.assertEqual(test_ad_words, expected_ad_words)
        self.assertEqual(test_story_words, expected_story_words)

    def test_mean_reading_time_for_a_question(self):
        """
        Tests mean_reading_time_for_a_question function with many data sets and checks if
        the function crashes when it encounters the default data set. Also test many cases with
        all question and context combinations.
        """
        mean_reading_data = mean_reading_time_for_a_question(self.default_student_data, "", "")
        empty_comparison_tuple = ("", "", 0, 0)
        self.assertEqual(mean_reading_data, empty_comparison_tuple)
        # The expected result times are rounded to 2 decimals here due to Python rounding errors
        # not matching actual rounding.
        results = mean_reading_time_for_a_question(self.test_student_data, self.feel, self.ads)
        self.assertEqual(results, (self.feel, self.ads, round(2.319, 2), 1))
        results = mean_reading_time_for_a_question(self.test_student_data, self.about, self.ads)
        self.assertEqual(results, (self.about, self.ads, round(2.945, 2), 1))
        results = mean_reading_time_for_a_question(self.test_student_data,
                                                   self.encountered,
                                                   self.ads)
        self.assertEqual(results, (self.encountered, self.ads, 0, 0))
        results = mean_reading_time_for_a_question(self.test_student_data,
                                                   self.feel,
                                                   self.short_story)
        self.assertEqual(results, (self.feel, self.short_story, round(1.121, 2), 1))
        results = mean_reading_time_for_a_question(self.test_student_data,
                                                   self.about,
                                                   self.short_story)
        self.assertEqual(results, (self.about, self.short_story, 0, 0))
        results = mean_reading_time_for_a_question(self.test_student_data,
                                                   self.encountered,
                                                   self.short_story)
        self.assertEqual(results, (self.encountered, self.short_story, 0, 0))

    def test_mean_reading_time_for_a_question_reversed(self):
        """
        Tests mean_reading_time_for_a_question function but with the data set reversed
        """
        mean_time = mean_reading_time_for_a_question(reversed(self.test_student_data),
                                                     "Have you encountered this text before?",
                                                     "This is an ad.")

        self.assertEqual(mean_time[0], "Have you encountered this text before?")

    def test_remove_outliers(self):
        """
        Test the remove_outlier functions on a list to see if it removes the outliers
        """
        outliers_data_1 = [-100, -50, 1, 2, 3, 4, 5, 100]
        outliers_data_2 = [1, 2, 3, 4, 5]

        remove_outliers(outliers_data_1)
        self.assertEqual(outliers_data_1, outliers_data_2)

    def test_compute_total_view_time(self):
        """
        Test that the total view time equals the expected values.
        """
        total_view_time = compute_total_view_time(self.test_student_data)
        self.assertEqual(total_view_time, 6.385)

        # check we don't crash on the defaults from the model!
        total_view_time = compute_total_view_time(self.default_student_data)
        self.assertEqual(total_view_time, 0)

    def test_compute_mean_reading_times_each_response(self):
        """
        Tests compute_mean_reading_times for correct means for each reading response time
        """
        expected = compute_mean_reading_times_each_response(self.default_student_data)
        self.assertEqual(expected, [1, 0.0, 0.0])

        expected = compute_mean_reading_times_each_response(self.student_data)
        for i in range(3):
            self.assertAlmostEqual(expected[i], [30, 7.546366666666666, 2.9542][i])

    def test_compute_median_view_time(self):
        """
        Test that the median view time equals the expected values.
        """
        median_view_time = compute_median_view_time(self.test_student_data)
        self.assertEqual(median_view_time, 2.319)

        # check we don't crash on the defaults from the model!
        median_view_time = compute_median_view_time(self.default_student_data)
        self.assertEqual(median_view_time, 0)

    def test_compute_mean_response_length(self):
        """
        Test that the mean response length equals the expected values.
        """
        mean_response_length = compute_mean_response_length(self.test_student_data)
        self.assertEqual(mean_response_length, 5.5)

        # check we don't crash on the defaults from the model!
        mean_response_length = compute_mean_response_length(self.default_student_data)
        self.assertEqual(mean_response_length, 0)

    def test_compute_reread_counts(self):
        """
        Test that the reread count equals the expected values.
        """

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "In one word", "This is an ad.")
        self.assertEqual({1: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "In three words or fewer", "This is an ad.")
        self.assertEqual({1: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "Have you encountered", "This is an ad.")
        self.assertEqual({0: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "In one word", "short story")
        self.assertEqual({1: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "In three words or fewer", "short story")
        self.assertEqual({0: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.test_student_data,
                                                    "Have you encountered", "short story")
        self.assertEqual({0: 1}, total_reread_counts)

        total_reread_counts = compute_reread_counts(self.default_student_data, "", "")
        self.assertEqual({}, total_reread_counts)

    def test_compute_mean_revisits(self):
        """
        Test that the mean number of revisits equals the expected values.
        """
        revisits_per_question = compute_mean_revisits(self.test_student_data)
        self.assertEqual(revisits_per_question['In one word, how does this text make you feel?'], 1)
        self.assertEqual(revisits_per_question['In three words or fewer, what is this text '
                                               'about?'], 0.5)
        self.assertEqual(revisits_per_question['Have you encountered this text before?'], 0)

        # check we don't crash on the defaults
        revisits_per_question = compute_mean_revisits(self.default_student_data)
        self.assertEqual(revisits_per_question[''], 0)

    def test_compute_median_revisits(self):
        """
        Tests that the median number of revisits equals the expected values.
        """
        revisits_per_question = compute_median_revisits(self.test_student_data)
        self.assertEqual(revisits_per_question['In one word, how does this text make you feel?'], 1)
        self.assertEqual(revisits_per_question['In three words or fewer, what is this text '
                                               'about?'], 0.5)
        self.assertEqual(revisits_per_question['Have you encountered this text before?'], 0)

        # check we don't crash on the defaults
        revisits_per_question = compute_mean_revisits(self.default_student_data)
        self.assertEqual(revisits_per_question[''], 0)

    def test_mean_reading_time_question_context(self):
        """
        Test the avg_time_context function to see if it can find the avg view times given a question
        and context. Also tests for if the question or context isn't in the data set.
        """
        avg_time = mean_reading_time_question_context(self.test_student_data,
                                                      self.feel,
                                                      self.ads)
        self.assertAlmostEqual(avg_time, 2.319)

        avg_time = mean_reading_time_question_context(self.default_student_data_2,
                                                      self.feel,
                                                      self.short_story)
        self.assertAlmostEqual(avg_time, 3.1992)

        avg_time = mean_reading_time_question_context(self.default_student_data,
                                                      self.feel,
                                                      self.ads)
        self.assertIsNone(avg_time)

    def test_mean_rereading_time_student(self):
        """
        Test the avg_time_student and see if given a student_id, the function can return
        the average view times for that student, even if they didn't do any viewing.
        """
        avg_time = mean_reading_time_student(self.test_student_data, 15)
        self.assertAlmostEqual(avg_time, 2.128333333333)

        avg_time = mean_reading_time_student(self.default_student_data, 0)
        self.assertIsNone(avg_time)

        avg_time = mean_reading_time_student(self.default_student_data_2, 7)
        self.assertAlmostEqual(avg_time, 2.2)

        avg_time = mean_reading_time_student(self.default_student_data_2, 999)
        self.assertIsNone(avg_time)

    def test_mean_rereading_time(self):
        """
        Test average_time function for many test cases and see if it returns either the correct
        average time or None if there are no view times in the data set
        """
        avg_time = mean_reading_time(self.test_student_data)
        self.assertAlmostEqual(avg_time, 2.128333333333)

        avg_time = mean_reading_time(self.default_student_data)
        self.assertIsNone(avg_time)

        avg_time = mean_reading_time(self.default_student_data_2)
        self.assertAlmostEqual(avg_time, 2.88266666666)

    def test_word_freq_all(self):
        """
        Test the word_freq_all function on the test data set and default data set
        """
        freq_dict = word_freq_all(self.test_student_data)
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {'sad': 1}
        self.assertEqual(freq_dict[specific_question_context], answer)

        freq_dict = word_freq_all(self.default_student_data)
        specific_question_context = ("", "")
        answer = {'': 1}
        self.assertEqual(freq_dict[specific_question_context], answer)

    def test_frequent_responses(self):
        """
        Test the function frequent_responses on the test data set and default data set
        """
        most_frequent_responses = frequent_responses(word_freq_all(self.test_student_data))
        specific_question_context = ('In one word, how does this text make you feel?',
                                     'This is an ad.')
        answer = {'most_frequent_words': ['sad'], 'max_occurrences': 1}
        self.assertEqual(most_frequent_responses[specific_question_context], answer)

        most_frequent_responses = frequent_responses(word_freq_all(self.default_student_data))
        specific_question_context = ("", "")
        answer = {'most_frequent_words': [''], 'max_occurrences': 1}
        self.assertEqual(most_frequent_responses[specific_question_context], answer)

    def test_common_response(self):
        """
        Tests to make sure the function runs properly by checking against known data sets.
        """
        most_common_response_value = most_common_response(self.test_student_data,
                                                          "In one word, how does this text make "
                                                          "you "
                                                          "feel?",
                                                          "This is an ad.")
        self.assertEqual(most_common_response_value, ['sad'])

        # check we don't crash on the defaults from the model!
        most_common_response_value = most_common_response(self.default_student_data, '', '')
        self.assertEqual(most_common_response_value, [''])

    def test_question_sentiment_analysis(self):
        """
        test that the average and standard deviation of test data equals the expected values
        """
        single_word_data = question_sentiment_analysis(self.test_student_data, 'one word')
        self.assertEqual(single_word_data, (-.75, 0))

        three_words_data = question_sentiment_analysis(self.test_student_data, 'three words')
        self.assertEqual(three_words_data, (0, 0))

    def test_get_sentiments(self):
        """
        test that the get_sentiments method returns the correct data for each word
        """

        sentiments = get_sentiments()
        competent_score = sentiments['competent']
        self.assertEqual(competent_score, 0.75)

        inefficient_score = sentiments['inefficient']
        self.assertEqual(inefficient_score, -0.5)

        length = len(sentiments)
        self.assertEqual(length, 89631)

    def test_context_vs_read_time(self):
        """
        test that the context_vs_read_time method returns the expected values
        """
        context_vs_read = context_vs_read_time(self.test_student_data)
        expected = (1.7546666666666664, 0.37366666666666665)
        self.assertEqual(context_vs_read, expected)
        # test that it still works with default values
        context_vs_read = context_vs_read_time(self.default_student_data)
        expected = (0, 0)
        self.assertEqual(context_vs_read, expected)

    def test_frequency_feelings(self):
        """
        Test that frequency_feelings method returns the expected values
        """
        frequency_feels = frequency_feelings(self.test_student_data)
        expected = [("sad", 2)]
        self.assertEqual(frequency_feels, expected)
        # test that it works with default values
        frequency_feels = frequency_feelings(self.default_student_data)
        expected = []
        self.assertEqual(frequency_feels, expected)

    def test_word_frequency_differences(self):
        """
        Test the word_frequency_differences function
        """

        word_frequency_differences = get_word_frequency_differences(self.test_student_data)
        expected = [('sad', -1)]
        self.assertEqual(word_frequency_differences, expected)

    def test_response_group_frequencies(self):
        """
        Tests get_response_groups_frequencies returns correct freq dictionaries when passed
        certain student data set
        """
        response_groups = get_response_groups_frequencies(self.student_data)
        expected = [
            {'sad': 2, 'bored': 1, 'annoyed': 2, 'fine': 1, 'melancholic': 1, 'suspicious': 1,
             'speculative': 1, 'depressed': 1, 'confused': 1},
            {'sad': 8, 'enticed': 1, 'ok': 1, 'inyrigu': 1, 'interested': 2, 'surprised': 1,
             'concerned': 1, 'helped': 1, 'depressed': 2, 'sad/curious': 1, 'intrigued': 1,
             'confused': 1, 'puzzled': 1},
            {'targeted': 1, 'confused': 3, 'informed': 2, 'weird': 1, 'comfortable': 1,
             'melancholy': 2, 'sad': 2, 'concerned': 1, 'uncomfortable': 1, 'curious': 1,
             'disappointed': 1, 'indifferent': 1, 'fine': 1, 'neutral': 1},
            {'somber': 1, 'mysterious': 1, 'curious': 1, 'sad': 1, 'interested': 1,
             'underwhelmed': 1, 'melancholy': 1, 'sadder': 1},
        ]
        self.assertEqual(expected, response_groups)

    def test_word_time_relations(self):
        """
        Test the word_time_relations function against the test data and an empty dataset
        """

        # Expected values for test_data.csv
        expected = {
            'sad': 1.72,
            'miscarriage': 1.4725,
            'no': 0,
            'yes': 0
        }
        test_result = word_time_relations(self.test_student_data)
        self.assertEqual(test_result, expected)

        # Expected dictionary for empty default data
        default_expected = {
            '': 0,
        }
        default_result = word_time_relations(self.default_student_data)
        self.assertEqual(default_result, default_expected)

    def test_description_has_relevant_words(self):
        """
        Tests that the relevant word testing method returns True when relevant words are
        included in a response and False otherwise
        """
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]

        empty_list_response = description_has_relevant_words("description", [])
        self.assertTrue(empty_list_response)

        single_word_positive_response = description_has_relevant_words("died", relevant_words)
        self.assertTrue(single_word_positive_response)

        capitalization_positive_response = description_has_relevant_words("MiScArrIAGe",
                                                                          relevant_words)
        self.assertTrue(capitalization_positive_response)

        multi_word_positive_response = description_has_relevant_words("losing a baby",
                                                                      relevant_words)
        self.assertTrue(multi_word_positive_response)

        negative_response = description_has_relevant_words("irrelevant words", relevant_words)
        self.assertFalse(negative_response)

    def test_percent_students_using_relevant_words(self):
        """
        Tests that the expected number of students are using relevant words.
        """
        relevant_words = ["dead", "death", "miscarriage", "killed", "kill", "losing", "loss",
                          "lost", "deceased", "died", "grief", "pregnancy", "pregnant"]
        story_context = "This is actually a short story."
        calculated_percent_story = percent_students_using_relevant_words(self.test_student_data,
                                                                         story_context,
                                                                         relevant_words)
        self.assertEqual(calculated_percent_story, 1.00)
        default_percent_story = percent_students_using_relevant_words(self.default_student_data,
                                                                      story_context,
                                                                      relevant_words)
        self.assertEqual(default_percent_story, 0)

        ad_context = "This is an ad."
        calculated_percent_ad = percent_students_using_relevant_words(self.test_student_data,
                                                                      ad_context,
                                                                      relevant_words)
        self.assertEqual(calculated_percent_ad, 1.00)
        default_percent_ad = percent_students_using_relevant_words(self.default_student_data,
                                                                   ad_context,
                                                                   relevant_words)
        self.assertEqual(default_percent_ad, 0)

    def test_compute_view_time_per_response(self):
        """
        Test that mean view times per response equals the expected values.
        """
        mean_view_time_per_response = compute_view_time_per_response(self.test_student_data)
        self.assertEqual(mean_view_time_per_response, {
            'This is an ad.': {'sad': [2.319]},
            'This is actually a short story.': {'sad': [1.121]},
        })

        mean_view_time_per_response = compute_view_time_per_response(self.default_student_data)
        self.assertEqual(mean_view_time_per_response, {
            'This is an ad.': {},
            'This is actually a short story.': {},
        })

    def test_reread_time_difference(self):
        """
        Test mean and difference functions with expected values
        """
        view_times_per_response = compute_view_time_per_response(self.test_student_data)
        ad_view_times_dict = view_times_per_response['This is an ad.']
        wanted_dict_ad_avg = build_mean_dict(ad_view_times_dict)
        ss_view_times_dict = view_times_per_response['This is actually a short story.']
        wanted_dict_ss_avg = build_mean_dict(ss_view_times_dict)
        difference = reread_time_difference(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(difference, {'sad': ['ad', 1.198]})

        view_times_per_response = compute_view_time_per_response(self.default_student_data)
        ad_view_times_dict = view_times_per_response['This is an ad.']
        wanted_dict_ad_avg = build_mean_dict(ad_view_times_dict)
        ss_view_times_dict = view_times_per_response['This is actually a short story.']
        wanted_dict_ss_avg = build_mean_dict(ss_view_times_dict)
        difference = reread_time_difference(wanted_dict_ad_avg, wanted_dict_ss_avg)
        self.assertEqual(difference, {})

    def test_get_common_elements(self):
        """
        test that common elements returns the common key:value pairs between two dictionaries
        with the mean of the values between the two dictionaries
        """
        view_times_per_response = compute_view_time_per_response(self.test_student_data)
        ad_dict = view_times_per_response['This is an ad.']
        wanted_dict_ad_mn = build_mean_dict(ad_dict)
        ss_dict = view_times_per_response['This is actually a short story.']
        wanted_dict_ss_mn = build_mean_dict(ss_dict)
        common_dict = get_common_elements(wanted_dict_ad_mn, wanted_dict_ss_mn)
        self.assertEqual(common_dict, {'sad': 1.72})

        view_times_per_response = compute_view_time_per_response(self.default_student_data)
        ad_dict = view_times_per_response['This is an ad.']
        wanted_dict_ad_mn = build_mean_dict(ad_dict)
        ss_dict = view_times_per_response['This is actually a short story.']
        wanted_dict_ss_mn = build_mean_dict(ss_dict)
        common_dict = get_common_elements(wanted_dict_ad_mn, wanted_dict_ss_mn)
        self.assertEqual(common_dict, {})

    def test_total_rereading_time_exclusive(self):
        """
        test that a dictionary of the keys exclusive to two dictionaries is what is expected
        """
        view_times_per_response = compute_view_time_per_response(self.test_student_data)
        ad_dict = view_times_per_response['This is an ad.']
        wanted_dict_ad_mn = build_mean_dict(ad_dict)
        ss_dict = view_times_per_response['This is actually a short story.']
        wanted_dict_ss_mn = build_mean_dict(ss_dict)
        exclusive_responses = total_reading_time_exclusive(wanted_dict_ad_mn, wanted_dict_ss_mn)
        self.assertEqual(exclusive_responses, {
            'This is an ad.': {},
            'This is actually a short story.': {},
        })


if __name__ == '__main__':
    run_analysis()
    print(run_analysis())
    unittest.main()  # run the tests
