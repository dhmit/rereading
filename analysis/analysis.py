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
    print(student_data)


if __name__ == '__main__':
    run_analysis()
#select responses with negative connotations (sad, missacarriage) when the context
# was "This is an ad." and find the difference between avg view times of these
# students' with those of neutral connotations (confused, sale). Our 'hypothesis' is that there
# might be a statistically significant difference showing students with responses of negative
# connotations (i.e. got the deeper meaning of text w/o clue from context) had a correlation
# with spending more time with the text

# select students with responses with neutral connotations (confused, sale) when the context was
# "This is an ad." but had responses with negative connotations when the context was
# "This is a short story." Subtract the former from latter and take the average. This will tell us
# about how much time it takes for students to make the deeper connection.

# take average of view time with context of "This is an ad."


#take average of view time with context of "This is actually a short story."