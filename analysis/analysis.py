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
    # Arrays for each type of context
    q1_ad = []
    q1_short = []
    for row in student_data:
        # "ad" signifies the "This is an ad." context
        # "encountered" signifies the "Have you encountered this text before?" question
        if "ad" in row['context'] and "encountered" in row['question']:
            view_count = len(row['views'])
            q1_ad.append(view_count)
    print(q1_ad)


if __name__ == '__main__':
    run_analysis()
