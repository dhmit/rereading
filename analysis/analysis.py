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
    # print(student_data)
    freq_dict = word_freq_all(student_data)
    for key in freq_dict:
        print(key)
        print(freq_dict[key])
        print("================")
    most_frequent_responses = frequent_responses(freq_dict)
    for key in most_frequent_responses:
        print(key)
        print(most_frequent_responses[key])
        print("--------------------")


def frequent_responses(freq_dict):
    output = {}
    for key in freq_dict:
        details = {}
        a_freq_dict = freq_dict[key]
        max_occurances = 0
        max_list = []
        for word in a_freq_dict:
            occurance = a_freq_dict[word]
            if  occurance > max_occurances:
                max_occurances = occurance
                max_list = [word]
            elif occurance == max_occurances:
                max_list.append(word)
        details['most_frequent_words'] = max_list
        details['max_occurances'] = max_occurances
        output[key] = details
    return output



def word_freq_all(data):
    '''
    :param data: A list of all of the data entries from the survey
    :return: A dictionary with a tuple of the question and context as keys and with values of a dictionary with the
    words as keys and their frequencies as values
    '''
    output = {}
    for entry in data:
        the_key = (entry["question"], entry["context"])
        if the_key not in output:
            output[the_key] = {}
        qc_dict = output[the_key]
        response = entry['response'].lower()
        if response not in qc_dict:
            qc_dict[response] = 1
        else:
            qc_dict[response] += 1
    return output


if __name__ == '__main__':
    run_analysis()
