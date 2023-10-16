import csv


def get_table():
    with open('data_table.csv', 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        return [[n] + line for n, line in enumerate(file)]


def change_file(file, table):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    for line in table[1:]:
        text = (text.replace(f'*T{line[1]} ', f'*T₽{line[2]} ')
                .replace(f'LT({line[1]})', f'LT(₽{line[2]})'))
    text = text.replace('₽', '')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
