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

'''
Analysis ideas
- Aggregating connotations of words
- Sort words into different tones or moods
- What are the most common responses?
- Words and frequencies
- The first reading response vs. the second reading response
    - how often does the response stay the same vs. change?
    - how does the connotation of the response change?
- Compare lengths of readings
- Number of rereadings (and avg etc.)

Data collection ideas
- What happens if we reverse the order of the contexts?

'''


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    print(student_data[0])


if __name__ == '__main__':
    run_analysis()
