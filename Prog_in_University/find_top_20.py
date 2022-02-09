import random


data = [
    {'Name': 'Vasya', 'scores': {'math': 58, 'russian_language': 62, 'computer_science': 48}, 'extra_scores': 0},
    {'Name': 'Fedya', 'scores': {'math': 33, 'russian_language': 85, 'computer_science': 42}, 'extra_scores': 2},
    {'Name': 'Marina', 'scores': {'math': 30, 'russian_language': 88, 'computer_science': 42}, 'extra_scores': 2},
    {'Name': 'Petya', 'scores': {'math': 92, 'russian_language': 33, 'computer_science': 34}, 'extra_scores': 3},
    {'Name': 'Gena', 'scores': {'math': 12, 'russian_language': 13, 'computer_science': 17}, 'extra_scores': 0},
    {'Name': 'Elena', 'scores': {'math': 90, 'russian_language': 79, 'computer_science': 88}, 'extra_scores': 7},
    {'Name': 'Egor', 'scores': {'math': 92, 'russian_language': 32, 'computer_science': 34}, 'extra_scores': 4}
]


def calculate_the_sum_of_the_assessments(value: dict) -> tuple:
    """
    Calculate the sum of the main and other assessments
    :param value: dict with assessments
    :type value: dict
    :return: sum main and sum other assessments
    :rtype: tuple
    """
    math, computer_science = value['scores']['math'], value['scores']['computer_science']
    total_sum = sum(value['scores'].values()) + value['extra_scores']

    return total_sum, math, computer_science


def find_to_20(input_data: list, count_pass: int = 3) -> list:
    """
    We choose the best candidates from the incoming list
    :param input_data: input list with candidates
    :type input_data: list
    :param count_pass: number of vacancies available
    :type count_pass: int
    :return: list with the best candidates
    :rtype: list
    """

    if len(input_data) <= count_pass:
        return input_data

    total_dict = {}
    for value in input_data:
        name = value.get('Name')
        total_dict[name] = (calculate_the_sum_of_the_assessments(value))

    sorted_list = list(sorted(total_dict.items(), key=lambda item: item[1]))[::-1]
    top_candidates = sorted_list[:(count_pass + 1)]

    if top_candidates[-1][1][0] != top_candidates[-2][1][0]:
        top_candidates.pop(-1)
        return top_candidates
    else:
        if top_candidates[-1][1][1] != top_candidates[-2][1][1]:
            top_candidates.pop(-1)
            return top_candidates
        else:
            if top_candidates[-1][1][2] != top_candidates[-2][1][2]:
                top_candidates.pop(-1)
                return top_candidates
            else:
                values = (1, 2)
                choice = random.choice(values)
                top_candidates.pop(-choice)
                return top_candidates


print(find_to_20(data))
