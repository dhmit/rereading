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
#    print(student_data[0]['question'])

    # Iterate through all records, and separate
    yes_id = []
    no_id = []
    for response in student_data:
        if (response['question'].find('Have you encountered this text before') == 0
                and response['context'].find('This is an ad.') == 0):
            if response['response'].lower().find('yes')  == -1:
                no_id.append(response['student_id'])
            else:
                yes_id.append(response['student_id'])
    print(yes_id)
    print(no_id)

    # Iterate through all responses to
    ad_yes_words = []
    ad_no_words = []
    for element in student_data:
        if element['question'].find('In one word') == 0 \
                and element['context'].find('This is an ad') == 0:
            if element['student_id'] in yes_id:
                ad_yes_words.append(element['response'].lower())
            else:
                ad_no_words.append(element['response'].lower())
    print(ad_yes_words)
    print(ad_no_words)

    yes_responses = dict()
    no_responses = dict()

    for response in ad_yes_words:
        if response in yes_responses:
            yes_responses[response] += 1
        else:
            yes_responses[response] = 1

    for response in ad_no_words:
        if response in no_responses:
            no_responses[response] += 1
        else:
            no_responses[response] = 1

    print(yes_responses)
    print(no_responses)

    diff_responses = dict()

    for word in yes_responses:
        if word in no_responses:
            diff_responses[word] = yes_responses[word] - no_responses[word]
        else:
            diff_responses[word] = yes_responses[word]
    for word in no_responses:
        if word not in yes_responses:
            diff_responses[word] = - no_responses[word]

    print(diff_responses)

    diff_responses_list = []
    for word in diff_responses:
        diff_responses_list.append((word, diff_responses[word]))
    print(diff_responses_list)











if __name__ == '__main__':
    run_analysis()

