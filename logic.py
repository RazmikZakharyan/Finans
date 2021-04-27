import sqlite3
from itertools import combinations, filterfalse, product

arguments = {
    'total': 0,
    'quantity': 0,
    'step': 0,
    'min_amount': 0,
    'percent min': 0,
    'percent max': 0,
    'duration min': 0,
    'duration max': 0
}

securities = []

while True:
    try:
        for arg in iter(arguments):
            if not('percent' in arg or 'duration' in arg):
                if arguments[arg] == 0:
                    arguments[arg] = int(input(f'enter the {arg}: '))
            else:
                if arguments[arg] == 0:
                    arguments[arg] = float(input(f'enter the {arg}: '))
        break
    except ValueError:
        print("Error! This is not a number. Try again.")


def possible_amounts(amount):
    return list(range(arguments['min_amount'], int(amount + arguments['step']), arguments['step']))


def average_percent(amounts, index, s):
    sum_percent = 0
    for j, i in enumerate(amounts):
        sum_percent += i * securities[index[j]]['percent']
    p = sum_percent / s
    if arguments['percent min'] < p < arguments['percent max']:
        return True, p
    return False, None


def average_duration(amounts, index, s):
    sum_duration = 0
    for j, i in enumerate(amounts):
        sum_duration += i * securities[index[j]]['duration']
    d = sum_duration / s
    if arguments['duration min'] < d < arguments['duration max']:
        return True, d
    return False, None


def main():
    amount_list = []
    for item in securities:
        if item['amount'] >= arguments['min_amount']:
            amount_list.append(item['amount'])
        else:
            amount_list.append(0)

    securities_com = combinations(
        zip(
            filterfalse(lambda x: x == 0, amount_list),
            filterfalse(
                lambda x: amount_list[x] == 0,
                range(0, len(amount_list))
            )
        ), arguments['quantity'])

    # finish_list = []
    count = 0
    for item in securities_com:
        possible_amounts_list = []
        index = []
        for amount, i in item:
            possible_amounts_list.append(possible_amounts(amount))
            index.append(i)
        for amounts in product(*possible_amounts_list):
            s = sum(amounts)
            if s == arguments['total']:
                result = average_percent(amounts, index, s)
                if result[0]:
                    p = result[1]
                    result = average_duration(amounts, index, s)
                    if result[0]:
                        portfolio = list(zip(amounts, index))
                        portfolio.append((p, result[1]))
                        # finish_list.append(portfolio)
                        print('{}: percent: {} duration: {}'.format(count, portfolio[-1][0], portfolio[-1][1]))
                        portfolio.pop()
                        for elem in portfolio:
                            print('\tname: {} \n\tamount: {}'.format(securities[elem[1]]['name'], elem[0]))
                        print()
                        count += 1
    # return finish_list


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('bonds.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''
            CREATE TABLE IF NOT EXISTS bonds(id integer primary key, title text,
             amount real, percent_value real, duration real)
            ''')
        self.conn.commit()

    def insert_data(self, title, amount, percent, duration):
        self.c.execute('''INSERT INTO bonds(title, amount, percent_value, duration) VALUES (?, ?, ?, ?)''',
                       (title, amount, percent, duration))
        self.conn.commit()


if __name__ == "__main__":
    db = DB()
    for item in db.c.execute('''SELECT * FROM bonds'''):
        securities.append({['id', 'name', 'amount', 'percent', 'duration'][i]: j for i, j in enumerate(item)})

    main()
    #
    # for i, item in enumerate(portfolios):
    #     print('{}: percent: {} duration: {}'.format(i, item[-1][0], item[-1][1]))
    #     item.pop()
    #     for elem in item:
    #         print('\tname: {} \n\tamount: {}'.format(securities[elem[1]]['name'], elem[0]))
