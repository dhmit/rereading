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
    mean_rereading_times()


def mean_rereading_times():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    mean_rereading_time_for_a_question(student_data, "feel", "ad")
    mean_rereading_time_for_a_question(student_data, "about", "ad")
    mean_rereading_time_for_a_question(student_data, "encountered", "ad")
    mean_rereading_time_for_a_question(student_data, "feel", "short story")
    mean_rereading_time_for_a_question(student_data, "about", "short story")
    mean_rereading_time_for_a_question(student_data, "encountered", "short story")


def mean_rereading_time_for_a_question(student_data, question_keyword, context):
    mean_time = 0
    number_of_rereaders = 0
    question_asked = ""
    for student_data_dictionary in student_data:
        if student_data_dictionary['question'].find(question_keyword) != -1:
            question_asked = student_data_dictionary['question']
            if student_data_dictionary['context'].find(context) != -1:
                mean_views = 0
                for view_time in student_data_dictionary['views']:
                    mean_views += view_time
                if len(student_data_dictionary['views']) != 0:
                    number_of_rereaders += 1
                    mean_time += mean_views / len(student_data_dictionary['views'])
    if number_of_rereaders != 0:
        mean_time /= number_of_rereaders
        mean_time = round(mean_time, 2)
        print(f"When those who thought the reading was a(n) {context} were asked \"{question_asked}\"")
        print(f"{number_of_rereaders} subjects reread the text for an average of {mean_time} seconds.")
    else:
        print(f"No who thought the reading was a(n) {context} and were asked \"{question_asked}\" reread the text.")

    print()

if __name__ == '__main__':
    run_analysis()
