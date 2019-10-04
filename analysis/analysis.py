"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path


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


def repeated_prompt_words():
    """
    Reports frequencies of exact words from story prompt used in responses. Prints analysis
    :return: tuple (response_ad, response_story), lists of unique responses to be used in further analysis.
    """
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!

    # extracting text responses from csv file, depending on context given (story vs. ad)
    response_ad = []
    response_story = []
    question = "In three words or fewer, what is this text about?"
    for x in student_data:
        x['response'] = x['response'].replace('.', '').lower()  # removing punctuation and making string lowercase
        x['response'] = x['response'].replace(',', '')
        if x['question'] == question and x['context'] == "This is an ad.":
            response_ad += x['response'].split()
        elif x['question'] == question and x['context'] == "This is actually a short story.":
            response_story += x['response'].split()

    # dictionaries to store frequencies of words in responses based on context given
    # word (string) : frequency (int)
    ad_resp_words = {}
    story_resp_words = {}

    # cycling through ad responses
    for word in response_ad:
        if word in ad_resp_words:
            ad_resp_words[word] += 1
        elif word not in stop_words:
            ad_resp_words[word] = 1

    # cycling through story responses
    for word in response_story:
        if word in story_resp_words:
            story_resp_words[word] += 1
        elif word not in stop_words:
            story_resp_words[word] = 1

    # list of words in story - for longer story, would want to read it from csv file using list comprehension
    story_vocab_list = ["for", "sale", "baby", "shoes", "never", "worn"]

    # for the first question given the context of the ad
    print("Given text vocab words that occurred in ad-context responses: ")
    for word in story_vocab_list:
        if word in ad_resp_words:
            print(word, ad_resp_words[word])

    # for the second question given the context of the story
    print("Given text vocab words that occurred in story-context responses: ")
    for word in story_vocab_list:
        if word in story_resp_words:
            print(word, story_resp_words[word])

    # uncomment for most commonly repeated words

    # print("Most commonly repeated words in ad context response:")
    # print(max(ad_resp_words.items(), key=lambda item: item[1]))
    # print("Most commonly repeated words in story context response:")
    # print(max(story_resp_words.items(), key=lambda item: item[1]))

    # uncomment for complete list of words used in responses (unsorted)

    # print("All words in ad context responses:")
    # print(ad_resp_words)
    # print("All words in story context responses:")
    # print(story_resp_words)

    return response_ad, response_story


if __name__ == '__main__':
    repeated_prompt_words()
