import argparse
import json

import tabulate

from exceptions import EmptyList


FLOAT_ACCURACY = 3
ENCODING = 'utf-8'
TABLEFMT = 'pipe'
KEYS_IN_LOG = (
    'url',
    'response_time',
)
HEADER_TABULATE = ('handler', 'total', 'avg_response_time')


def check_key_availability(data_dict: dict, key: str, num: int):
    """Проверка наличия ключа в словаре."""
    get_url = data_dict.get(key)
    if get_url is None:
        raise KeyError(f'Отсутствует {key} в строке {num}')


def calc_avg(filename, temp_dict):
    """
    Функция для вычисления общего количества запросов к endpoint и
    среднее время ответа.

    Значения общего количества и среднее время хранятся в словаре.
    Ключом словаря является endpoint.
    """
    avg_dict = temp_dict
    for num, line in enumerate(filename, 1):
        data = json.loads(line)
        for key in KEYS_IN_LOG:
            check_key_availability(data, key, num)
        if data['url'] in avg_dict:
            avg_dict[data['url']]['total'] += 1
            avg_dict[data['url']]['avg_time'] += data[
                'response_time'
            ]
        else:
            avg_dict[data['url']] = {
                'total': 1, 'avg_time': data['response_time']
            }
    for key, value in avg_dict.items():
        avg_dict[key]['avg_time'] = round(
            value['avg_time'] / value['total'],
            FLOAT_ACCURACY
        )
    return avg_dict


def main(filenames: list, report_name: str):
    """
    Функция для распределения аргументов.

    В зависимости от аргумента вызывается та или иная функция.
    """
    if not filenames:
        raise EmptyList(
            'Список аргументов отсутствует Необходимо передать названия файлов'
        )
    result_dict = {}
    for filename in filenames:
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                if report_name == 'average':
                    result_dict.update(calc_avg(file, result_dict))
        except FileNotFoundError:
            print('Такого файла не существует.')
    return result_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', action='extend', nargs='+')
    parser.add_argument('-r', '--report', default='average')
    args = parser.parse_args()
    files = args.file
    report = args.report

    result = main(files, report)

    values = [(name, *inner.values()) for name, inner in result.items()]
    values.sort(key=lambda x: x[1], reverse=True)
    print(
        tabulate.tabulate(
            values,
            headers=HEADER_TABULATE,
            tablefmt=TABLEFMT,
            showindex=True,
        )
    )
