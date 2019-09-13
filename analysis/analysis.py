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


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    # print(student_data)
    people_with_multiple_views = []
    people_with_one_view = []

    # one word answers for each question separated out by view count (one vs multiple)
    single_view_responses_to_c1 = []
    single_view_responses_to_c2 = []
    multiple_view_responses_to_c1 = []
    multiple_view_responses_to_c2 = []

    for person_response in student_data:
        # filter out responses from people who didn't go back
        # this sorting doesn't work. We need to find a way to sort people with 1, +1 views...
        if len(person_response['views']) == 1:
            people_with_one_view.append(person_response)
        else:
            people_with_multiple_views.append(person_response)

    for person in people_with_one_view:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                single_view_responses_to_c2.append(person['response'].lower())
            else:
                single_view_responses_to_c1.append(person['response'].lower())

    for person in people_with_multiple_views:
        if person['question'] == "In one word, how does this text make you feel?":
            if person['context'] == "This is actually a short story.":
                multiple_view_responses_to_c2.append(person['response'].lower())
            else:
                multiple_view_responses_to_c1.append(person['response'].lower())

    for i in (single_view_responses_to_c1, single_view_responses_to_c2,
              multiple_view_responses_to_c1, multiple_view_responses_to_c2):
        print(find_word_frequency(i))
        print("\n")


def find_word_frequency(response_list):
    freq = {}
    for word in response_list:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


if __name__ == '__main__':
    run_analysis()
