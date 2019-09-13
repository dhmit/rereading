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
    """This analysis function compares the average view time for when the responder
     was told the text was an ad versus a story"""

    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)

    ad_views = 0
    ad_views_counter = 0
    story_views = 0
    story_views_counter = 0

    for elem in student_data:
        if elem['context'] == 'This is an ad.':
            if len(elem['views']) == 0:
                ad_views += 0
                ad_views_counter += 1
            else:
                ad_views += elem['views'][0]
                ad_views_counter += 1
        else:
            if len(elem['views']) == 0:
                story_views += 0
                story_views_counter += 1
            else:
                story_views += elem['views'][0]
                story_views_counter += 1

    average_ad = ad_views/ ad_views_counter
    average_story = story_views/ story_views_counter

    print("The average viewing time for when the responder was told it was an ad was ", average_ad,
           "while the average viewing time for when the responder was told it was a story was ", average_story)
if __name__ == '__main__':
    run_analysis()
