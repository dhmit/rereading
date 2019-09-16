"""

Analysis.py - initial analyses for dhmit/rereading

"""

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
            row['views'] = eval(row['views'])  # eval the list
            out_data.append(row)
    return out_data


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    """"
    This program shows how many times students had to reread the text depending
    on the context (ad or short story) and the question.
    """

    # Question 1
    q1_ad = []
    q1_short = []
    for row in student_data:
        # "encountered" signifies the "Have you encountered this text before?" question
        # "ad" signifies the "This is an ad." context
        # "short" signifies the "This is a short story." context
        if "ad" in row['context'] and "encountered" in row['question']:
            view_count = len(row['views'])
            q1_ad.append(view_count)
        elif "short" in row['context'] and "encountered" in row['question']:
            view_count = len(row['views'])
            q1_short.append(view_count)

    # Question 2
    q2_ad = []
    q2_short = []
    for row in student_data:
        # "one" signifies the "In one word, how does this make you feel?" question
        # "ad" signifies the "This is an ad." context
        # "short" signifies the "This is a short story." context
        if "ad" in row['context'] and "one" in row['question']:
            view_count = len(row['views'])
            q2_ad.append(view_count)
        elif "short" in row['context'] and "one" in row['question']:
            view_count = len(row['views'])
            q2_short.append(view_count)

    # Question 3
    q3_ad = []
    q3_short = []
    for row in student_data:
        # "three" signifies the "In three words or fewer, what is this text about?" question
        # "ad" signifies the "This is an ad." context
        # "short" signifies the "This is a short story." context
        if "ad" in row['context'] and "three" in row['question']:
            view_count = len(row['views'])
            q3_ad.append(view_count)
        elif "short" in row['context'] and "three" in row['question']:
            view_count = len(row['views'])
            q3_short.append(view_count)


if __name__ == '__main__':
    run_analysis()
