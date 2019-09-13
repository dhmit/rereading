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
        if (response['question'].find('encountered this text') == 0
                and response['context'].find('This is an ad.') == 0):
            if response['response'].lower().find('yes')  == -1:
                no_id.append(response['student_id'])
            else:
                yes_id.append(response['student_id'])
    print(yes_id)
    print(no_id)

    ad_yes_words = []
    ad_no_words = []
    for element in student_data:
        if element['question'].find('In one word') == 0:






if __name__ == '__main__':
    run_analysis()

