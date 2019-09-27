"""

Analysis.py - creates multiple dictionaries to analyze rereading data

Creates:


"""
from ast import literal_eval
import csv
from pathlib import Path
from collections import defaultdict


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
    """
    For each context, creates a list of 2-element lists corresponding response and average time of reading
    :return: List[List[response,average time]]
    """
    csv_path = Path('data', 'rereading_data_2019-09-13.csv')
    student_data = load_data_csv(csv_path)


def compute_average_view_time_per_response(student_data):
    """
    :param student_data: list, student response dicts
    :return:
    wanted_dict_ad - Dictionary ('ad context response in lowercase': [total reading times for each user])
    wanted_dict_ss - Dictionary ('short story context response in lowercase': [total reading times for each user])
    wanted_dict_ad_exclusive - Dictionary ('ad context response in lowercase not in short story context responses':
        [total reading times for each user])
    wanted_dict_ss_exclusive - Dictionary ('short story context response in lowercase not in ad context responses':
        [total reading times for each user])
    wanted_dict_ad_exclusive_avg - Dictionary ('ad context response in lowercase not in short story context responses':
        average reading time)
    wanted_dict_ss_exclusive_avg - Dictionary ('short story context response in lowercase not in ad context responses':
        average reading time)
    wanted_dict_combined - Dictionary ('responses from both ad and short story context': average reading time)
    wanted_dict_difference - Dictionary ('responses common to both ad and short story context':
        [which context had a longer average reading time, the difference between the averages of the two contexts])
    ad_response_times - Dictionary ('ad context response in lowercase': average reading time)
    ss_response_times - Dictionary ('short story context response in lowercase': average reading time)
    """

    # Collect the data from the response and time fields and compile them into dictionaries (1 per context)
    header_1 = ('question', 'In one word, how does this text make you feel?')
    header_2 = [('context', 'This is an ad.'), ('context', 'This is actually a short story')]
    target_headers = ('response', 'views')
    desired_data = (header_1, header_2, target_headers)
    data_dict = extract_data(student_data, desired_data)
    wanted_dict_ad = defaultdict(list)
    wanted_dict_ss = defaultdict(list)
    for entry in student_data:
        if entry['question'] == 'In one word, how does this text make you feel?':
            if entry['context'] == 'This is an ad.':
                response = entry['response']
                # Ensure capitalization does not separate duplicate answers
                response = response.lower()
                views = sum(entry['views'])
                wanted_dict_ad[response].append(views)

            elif entry['context'] == 'This is actually a short story.':
                response = entry['response']
                # Ensure capitalization does not separate duplicate answers
                response = response.lower()
                views = sum(entry['views'])
                wanted_dict_ss[response].append(views)

    # Average the response times for each response and make new dictionaries (1 per context)
    ad_response_times = {}
    ss_response_times = {}
    for word in wanted_dict_ad:
        running_sum = sum(wanted_dict_ad[word])
        avg = running_sum / len(wanted_dict_ad[word])
        ad_response_times[word] = avg

    for word in wanted_dict_ss:
        running_sum = sum(wanted_dict_ss[word])
        avg = running_sum / len(wanted_dict_ss[word])
        ss_response_times[word] = avg

    # Start making a combined dictionary that does not separate based on context, begin with ad context
    wanted_dict_combined = {}
    for word in ad_response_times.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_combined[word] = ad_response_times[word]

    # Continue building the combined dictionary with short story dictionary
    for word in ss_response_times.keys():
        # Average current response with new data
        if word in wanted_dict_combined.keys():
            wanted_dict_combined[word] = (wanted_dict_combined[word] + ss_response_times[word]) / 2
        # Add the new data
        else:
            wanted_dict_combined[word] = ss_response_times[word]

    # Make a dictionary that gives the name of the context with the longer average response time and difference
    # between two contexts if a response is common to both contexts
    wanted_dict_difference = {}
    for word in ad_response_times.keys():
        if word in ss_response_times.keys():
            if ad_response_times[word] > ss_response_times[word]:
                wanted_dict_difference[word] = ["ad", ad_response_times[word] - ss_response_times[word]]
            else:
                wanted_dict_difference[word] = ["short story", ss_response_times[word] - ad_response_times[word]]

    # Make a dictionary of the responses used in ad context that were not used in short story context and their total
    # reading times
    wanted_dict_ad_exclusive = defaultdict(list)
    wanted_dict_ss_exclusive = defaultdict(list)
    wanted_dict_ad_exclusive_avg = {}
    wanted_dict_ss_exclusive_avg = {}
    for word in wanted_dict_ad.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ad_exclusive[word].append(wanted_dict_ad[word])
            # Make a separate dictionary of average times of responses exclusive to ad context
            wanted_dict_ad_exclusive_avg[word] = sum(wanted_dict_ad[word]) / len(wanted_dict_ad[word])

    # Make a list of the responses used in short story context that were not used in ad context and their total
    # reading times
    for word in wanted_dict_ss.keys():
        if word not in wanted_dict_combined.keys():
            wanted_dict_ss_exclusive[word].append(wanted_dict_ss[word])
            # Make a separate dictionary of average times of responses exclusive to short story context
            wanted_dict_ss_exclusive_avg[word] = sum(wanted_dict_ss[word]) / len(wanted_dict_ss[word])


def extract_data(student_data, data_headers):
    """
    Extracts the desired data fields from the data
    :param student_data: list, student response dicts
    :param data_headers: Tuple(Tuple(First Header:Text), List[Tuple(Second Header: Text)], List[Target Headers])
    :return: desired data dict
    """

    return_dict = defaultdict(list)
    for entry in student_data:
        if entry[data_headers(1)(1)] == data_headers(1)(2):
            for i in range(len(data_headers(2))):
                if entry[data_headers(2)[i](1)] == entry[data_headers(2)[i](2)]:
                    for h in range(len(data_headers(3))):
                        # append the data to data header list
                        return_dict[data_headers(2)[i](2)].append({data_headers(3)[h]:entry[data_headers(3)[h]]})
    return return_dict


if __name__ == '__main__':
    run_analysis()
