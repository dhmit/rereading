"""

Analysis.py - initial analyses for dhmit/rereading

"""
from ast import literal_eval
import csv
from pathlib import Path
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


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    wanted_dict = defaultdict(list)
    wanted_dict_ss = defaultdict(list)
    for entry in student_data:
        #context = This is an ad
        if ((entry['id'] - 59) % 6 == 0):
            response = entry['response']
            views = sum(entry['views'])
            wanted_dict[response].append(views)

        #context = this is a short story
        elif ((entry['id']-62)%6 == 0):
            response = entry['response']
            views = sum(entry['views'])
            wanted_dict_ss[response].append(views)

    for word in wanted_dict:
        sum = 0
        wanted_dict[word]
    print(wanted_dict_ss)
    print(wanted_dict)





if __name__ == '__main__':
    run_analysis()
