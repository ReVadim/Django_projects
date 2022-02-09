import datetime
import xlsxwriter
from pathlib import Path


YEAR = datetime.datetime.today().year
know_english = ['Vasya', 'Jimmy', 'Max', 'Eric', 'Zoi', 'Felix']
sportsmen = ['Don', 'Peter', 'Eric', 'Jimmy', 'Mark', 'Max']
more_than_20_years = ['Peter', 'Julie', 'Jimmy', 'Mark', 'Max']


def find_athletes_by_set(names: list, hobby: list, age: list) -> set:
    """ Take three lists as input and find matches """

    common_list = [names, hobby, age]
    return set.intersection(*map(set, common_list))


def find_athletes_by_counter(names: list, hobby: list, age: list) -> dict:
    """ Take three lists as input and find matches """
    counter = {}
    common_list = names + hobby + age
    for elem in common_list:
        counter[elem] = counter.get(elem, 0) + 1

    athletes = {element: count for element, count in counter.items() if count == 3}

    return athletes


# print(find_athletes_by_counter(know_english, sportsmen, more_than_20_years))


names = ['Vasya', 'Jimmy', 'Petya', 'Max', 'Eric', 'Zoi', 'Felix', 'Chris', 'Margo', 'Jane']
birthday_years = [1962, 1995, 2009, None, None, None, None, 1998, 2001, 2002]
gender = ['Male', 'Male', 'Male', None, None, 'Female', None, 'Male', None, None]


def check_age(check_data: list, min_age: int = 17, limit_year: int = YEAR, max_age: int = 30) -> list:
    """ check person with age from min_age to max_age """

    name, year = check_data
    if year and min_age < (limit_year - year) < max_age:
        return check_data


def get_inductees(names: list, birthday_years: list, gender: list) -> dict:
    """ Welcome to army """

    ambiguity = []
    military = []

    for position, value in enumerate(names):
        if gender[position] == 'Male':
            candidate = check_age([value, birthday_years[position]])
            if candidate:
                military.append(candidate)
        elif gender[position] is None:
            if birthday_years[position]:
                person = check_age([value, birthday_years[position]])
                if person:
                    ambiguity.append(person)
            else:
                ambiguity.append(value)

    json = {'military': military, 'ambiguity': ambiguity}

    return json


# print(get_inductees(names, birthday_years, gender))


students_avg_scores = {'Max': 4.964, 'Eric': 4.962, 'Peter': 4.923, 'Mark': 4.957, 'Julie': 4.95, 'Jimmy': 4.973,
                       'Felix': 4.937, 'Vasya': 4.911, 'Don': 4.936, 'Zoi': 4.937}


def create_excel_file(data_dict: dict) -> any:
    """ Convert python dict to MS excel format """

    workbook = xlsxwriter.Workbook('top-3.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for key, item in data_dict.items():
        row += 1
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, item)
        row += 1

    workbook.close()
    link = Path('top_3')
    link.symlink_to('top-3.xlsx')
    return link


def make_report_about_top3(scores_dict: dict, top_limit: int = 3) -> any:
    """ Get data from dict, sort values and take 3 best results in excel format """

    sorted_dict = sorted(scores_dict.items(), key=lambda kv: kv[1])
    sorted_dict = sorted_dict[-top_limit:]

    return create_excel_file(dict(sorted_dict))


print(make_report_about_top3(students_avg_scores))
