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
    average_rereading_time_first_question()


def average_rereading_time_first_question():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!
    average_ad_time = 0
    average_short_story_time = 0
    ad_count = 0
    short_story_count = 0
    for student_data_dictionary in student_data:
        if student_data_dictionary['question'].find("feel") != -1:
            if student_data_dictionary['context'] == "This is an ad.":

                average_views = 0
                for view_time in student_data_dictionary['views']:
                    average_views += view_time
                if len(student_data_dictionary['views']) != 0:
                    ad_count += 1
                    average_ad_time += average_views / len(student_data_dictionary['views'])
            else:

                average_views = 0
                for view_time in student_data_dictionary['views']:
                    average_views += view_time
                if len(student_data_dictionary['views']) != 0:
                    short_story_count += 1
                    average_short_story_time += average_views / len(student_data_dictionary['views'])
    average_short_story_time /= short_story_count
    average_ad_time /= ad_count

    print("Number of people who reread the text thinking it was an ad: "
          + str(ad_count) + ".")
    print("Their average reread time for the first question was "
          + str(round(average_ad_time, 2)) + " seconds.")
    print("Number of people who reread the text thinking it was a short story: "
          + str(short_story_count) + ".")
    print("Their average reread time for the first question was "
          + str(round(average_short_story_time, )) + " seconds.")
    print(student_data)


if __name__ == '__main__':
    run_analysis()
