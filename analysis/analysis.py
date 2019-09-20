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


def compile_response(student_data, question):
    data = {}
    for elem in student_data:
        if elem['question'] == question:
            if elem['context'] not in data:
                data[elem['context']] = {elem['response']: 1}
            else:
                if elem['response'] in data[elem['context']]:
                    data[elem['context']][elem['response']] += 1
                else:
                    data[elem['context']][elem['response']] = 1
    return data

def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    print(compile_response(student_data, "In one word, how does this text make you feel?"))




if __name__ == '__main__':
    run_analysis()
