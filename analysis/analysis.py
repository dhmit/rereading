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


def compute_reread_counts(student_data):
    """"
    Given a list of student response dicts,
    return a matrix containing the number of times students had to reread
    the text based on the context and question.
    :param student_data: list, student response dicts
    :return: matrix, rows being context & question, columns having tallies
    of how many students reread 1 time, 2 times, etc.
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

        all_arrays = [q1_ad, q1_short, q2_ad, q2_short, q3_ad, q3_short]
        zero_counter = 0
        one_counter = 0
        two_counter = 0
        three_counter = 0
        four_counter = 0
        five_above= 0

        for x in all_arrays:
            for y in x:
                if y == 0:
                    zero_counter += 1
                elif y == 1:
                    one_counter += 1
                elif y == 2:
                    two_counter += 1
                elif y == 3:
                    three_counter += 1
                elif y == 4:
                    four_counter += 1
                else:
                    five_above += 1
                clear(x)
                x.append(zero_counter)
                x.append(one_counter)
                x.append(two_counter)
                x.append(three_counter)
                x.append(four_counter)
                x.append(five_above)
        return all_arrays  # We need to format our output


def run_analysis():
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)
    reread_counts = compute_reread_counts(student_data)
    print("Number of times students reread text based on question or context:\n")
    print(reread_counts)


if __name__ == '__main__':
    run_analysis()
