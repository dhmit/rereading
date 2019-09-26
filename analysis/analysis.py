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
    '''
    Analyze answer response times by computing a ratio of the response
    time of the first question to the response time of the second question;
    if multiple responses are recorded for the same question, add 
    response times first.
    '''
    # TODO: do something with student_data that's not just printing it!
    # print(student_data)

    total_first_response = 0
    total_second_response = 0
    total_participants = 0
    last_student_id = -1  # value not present in the data
    for line in student_data:
        context = line["context"]
        question = line["question"]
        student_id = line["student_id"]
        if question == "In one word, how does this text make you feel?":
            if context == 'This is an ad.':
                for duration in line["views"]:
                    total_first_response += duration
            elif context == "This is actually a short story.":
                for duration in line["views"]:
                    total_second_response += duration
        if student_id != last_student_id:
            total_participants += 1
            last_student_id = student_id

    mean_first_response = total_first_response / total_participants
    mean_second_response = total_second_response / total_participants

    print(f"total participants: {total_participants}")
    print(f"Mean first response: {mean_first_response}")
    print(f"Mean first response: {mean_second_response}")



if __name__ == '__main__':
    run_analysis()
