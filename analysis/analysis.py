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

# def collect_word_frequencies(responses):
#     csv_path = Path('data', 'rereading_data_2019-09-13.csv')
#     student_data = load_data_csv(csv_path)
#
#     response_ad = []
#     response_story = []
#
#     for x in student_data:
#         if x['question'] == "In three words or fewer, what is this text about?" and x['context'] == "This is an ad.":
#             response_ad.append(x['response'])
#         elif x['question'] == "In three words or fewer, what is this text about?" and x['context']
#         == "This is actually a short story.":
#             response_story.append(x['response'])
#     print(response_ad)
#     print(response_story)
#
#     response_dict_ad = {}
#     response_dict_story = {}
#
#     for response in response_ad:
#
#
#         if "ad" in response[2]:
#             response_dict_ad[response[3]] = response_dict_ad.get(response[3], 0) + 1
#
#             else:
#             response_dict_story[response[3]] = response_dict_story.get(response[3], 0) + 1
#
#     return response_dict_ad
#     return response_dict_story

# analysis of verbs versus nouns in ad responses and story responses - OLD ANALYSIS PROGRAM

def run_analysis():
    stop_words = ['a', 'and', 'the', 'of', 'an', 'for']
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    response_ad = []
    response_story = []
    response_story_unique = []
    unique_words_in_story = set()

    for x in student_data:
        x['response'] = x['response'].replace('.', '').lower()
        x['response'] = x['response'].replace(',', '')
        if x['question'] == "In three words or fewer, what is this text about?" and x['context'] == "This is an ad.":
            response_ad += x['response'].split()
        elif x['question'] == "In three words or fewer, what is this text about?" and x['context'] == "This is actually a short story.":
            words = x['response'].split()
            response_story += words
            unique_words_in_story |= set(words)
            response_story_unique.append(len(unique_words_in_story))
    for n in response_story_unique:
        print ("#"*n)

    print(response_story_unique)

    ad_resp_words = {}
    story_resp_words = {}
    for word in response_ad:

        if word in ad_resp_words:
            ad_resp_words[word] += 1
        elif word not in stop_words:
            ad_resp_words[word] = 1
    # change to story responses
    for word in response_story:
        if word in story_resp_words:
            story_resp_words[word] += 1
        elif word not in stop_words:
            story_resp_words[word] = 1
    # count the words in the response that repeat the original story
    story_vocab_list = ["for", "sale", "baby", "shoes", "never", "worn"]
    # for the first question with the context of the ad
    print("Given text vocab words that occurred in ad-context responses: ")
    for word in story_vocab_list:
        if word in ad_resp_words:
            print(word, ad_resp_words[word])
    # for the 2nd question with the context of the story
    print("Given text vocab words that occurred in story-context responses: ")
    for word in story_vocab_list:
        if word in story_resp_words:
            print(word, story_resp_words[word])
#
    # print(max(story_resp_words.items(), key=lambda item: item[1]))

    # print(ad_resp_words)
    # print(story_resp_words)
    # print([w for w in response_ad if w not in ad_resp_words])

    # only 36 unique words

    # what if there're 1000 people? will there be a pattern? Overlaps? approach: take segments of
    # data and analyze it to find patters and plot it
    # manually tag the words (36 unique words) or just pick some representative words
    # group the similar words together
    # Q: how many times the responses contain negative words in the ad_response vs. story_response?


if __name__ == '__main__':
    run_analysis()
