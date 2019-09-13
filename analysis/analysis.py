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
    """compares average viewtimes, given different context (ad vs story)"""
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    # TODO: do something with student_data that's not just printing it!

    ad_sum = 0
    ad_count = 0
    story_sum = 0
    story_count = 0


    for dict in student_data:
        if dict['context'] == "This is an ad.":
            if not len(dict["views"])  == 0:
                for view in dict["views"]:
                    ad_sum = ad_sum + view
            ad_count += 1
        elif dict["context"] == "This is actually a short story.":
            if not len(dict["views"])  == 0:
                for view in dict["views"]:
                    story_sum = story_sum + view
            story_count += 1

    print("Average viewtime for ad:", ad_sum/ad_count)
    print("Average viewtime for short story", story_sum/story_count)

    #print(student_data)


if __name__ == '__main__':
    run_analysis()
