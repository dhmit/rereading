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
    """"
    This program shows how many times students had to reread the text depending
    on the context (ad or short story) and the question.
    """

    q1_ad = []
    q1_short = []
    q2_ad = []
    q2_short = []
    q3_ad = []
    q3_short = []
    for row in student_data:
        # "encountered" signifies the "Have you encountered this text before?" question
        # "one" signifies the "In one word, how does this make you feel?" question
        # "three" signifies the "In three words or fewer, what is this text about?" question
        # "ad" signifies the "This is an ad." context
        # "short" signifies the "This is a short story." context
        view_count = len(row['views'])
        question = row['question']
        context = row['context']
        if "ad" in context:
            if "encountered" in question:
                q1_ad.append(view_count)
            elif "one" in question:
                q2_ad.append(view_count)
            elif "three" in question:
                q3_ad.append(view_count)

        if "short" in context:
            if "encountered" in question:
                q1_short.append(view_count)
            elif "one" in question:
                q2_short.append(view_count)
            elif "three" in question:
                q3_short.append(view_count)


q1_final_ad = []
q2_final_ad = []
q3_final_ad = []
q1_final_short = []
q2_final_short = []
q3_final_short = []
zero_counter = 0
one_counter = 0
two_counter = 0
three_counter = 0
four_counter = 0
five_above= 0

for x in q1_ad:
    if(x==0):
        zero_counter+=1
    elif(x==1):
        one_counter+=1
    elif (x == 2):
        two_counter += 1
    elif (x == 3):
        three_counter += 1
    elif (x == 4):
        four_counter += 1
    else:
        five_above +=1






    print(student_data)


if __name__ == '__main__':
    run_analysis()
