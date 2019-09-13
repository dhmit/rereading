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
    for row in range[1, 181]:
        if "ad" in student_data[row]['context'] and "encountered" in student_data[row]['question']:
            q1_ad[row - 1] = len(student_data[row]['views'])
    print(student_data)


if __name__ == '__main__':
    run_analysis()
