import re
import pymorphy2
import csv
from collections import Counter

message_re = re.compile(r'<div class="text">\n(.*)') # Регулярное выражение для поиска сообщений

morph = pymorphy2.MorphAnalyzer()

def comparing_numbers(a, tag_a, b, tag_b, c, tag_c):
    if a < b:
        if b < c:
            return tag_c
        else:
            return tag_b
    elif a < c:
        return tag_c
    else:
        return tag_a

messages_4_csv = []
def message_extracting(file, out_file): # Извлечение текстов сообщений из html файлов
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        with open(out_file, 'w', encoding='utf-8') as f:
            for message in message_re.findall(text):
                f.write(message + '\n')
                messages_4_csv.append(message)
    return out_file

def preprocessing(file): # Разделение сообщений на слова, лемматизация
    with open(file, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for i in range(len(text)):
            text[i] = re.split(r"<br>|&quot;|\.|,|!|\?|\n|\s", text[i]) # Разделение на слова
            for j in range(len(text[i])):
                text[i][j] = morph.parse(text[i][j])[0].normal_form # Лемматизация
        return text

html_file = input('Введите имя файла: ')
lemmatised_messages = preprocessing(message_extracting(html_file, 'outer.txt'))

with open('emo_dict.csv', encoding='utf-8') as f:
    data_emodict = list(csv.DictReader(f, delimiter=';'))
    for m in range(len(lemmatised_messages)): # Цикл, который идёт по сообщениям
        for w in range(len(lemmatised_messages[m])): # Цикл, который идёт по словам в сообщении
            for i in data_emodict: # Цикл, который идёт по словарю
                if lemmatised_messages[m][w] == i['term']:
                    lemmatised_messages[m][w] = i['tag']
        lemmatised_messages[m] = Counter(lemmatised_messages[m])
        dct = {}
        dct['NEUT'] = lemmatised_messages[m]['NEUT']
        dct['PSTV'] = lemmatised_messages[m]['PSTV']
        dct['NGTV'] = lemmatised_messages[m]['NGTV']
        lemmatised_messages[m] = dct

results_1 = []
results_2 = []

for m in range(len(lemmatised_messages)): # Учитываем нейтральные слова
    results_1.append(comparing_numbers(lemmatised_messages[m]['NEUT'], 'NEUT',
                                               lemmatised_messages[m]['PSTV'], 'PSTV',
                                               lemmatised_messages[m]['NGTV'], 'NGTV'))

for m in range(len(lemmatised_messages)): # Не учитываем нейтральные слова
    results_2.append(comparing_numbers(0, 'NEUT',
                                       lemmatised_messages[m]['PSTV'], 'PSTV',
                                       lemmatised_messages[m]['NGTV'], 'NGTV'))

with open('anylised_messages.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['id', 'messages', 'result_1', 'result_2']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for m in range(len(messages_4_csv)):
        writer.writerow({'id': m, 'messages': messages_4_csv[m], 'result_1': results_1[m], 'result_2': results_2[m]})
