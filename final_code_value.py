import re
import pymorphy2
import csv
from statistics import mean

message_re = re.compile(r'<div class="text">\n(.*)') # Регулярное выражение для поиска сообщений

morph = pymorphy2.MorphAnalyzer()

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

with open('emo_dict.csv', 'r', encoding='utf-8') as f:
    data_emodict = list(csv.DictReader(f, delimiter=';'))
    for m in range(len(lemmatised_messages)): # Цикл, который идёт по сообщениям
        for w in range(len(lemmatised_messages[m])): # Цикл, который идёт по словам в сообщении
            for i in data_emodict:  # Цикл, который идёт по словарю
                if lemmatised_messages[m][w] == i['term']:
                    lemmatised_messages[m][w] = float(i['value'])
            if type(lemmatised_messages[m][w]) == str and lemmatised_messages[m][w] != ' ':
                lemmatised_messages[m][w] = 0.0
        while ' ' in lemmatised_messages[m]:
            lemmatised_messages[m].remove(' ')

results_1 = []
results_2 = []
results_3 = []

for m in range(len(lemmatised_messages)):
    results_1.append(mean(lemmatised_messages[m])) # Тональность сообщений с учётом нулевых значений

for m in range(len(lemmatised_messages)):
    while 0.0 in lemmatised_messages[m]:
        lemmatised_messages[m].remove(0.0)
    if lemmatised_messages[m]:
        results_2.append(mean(lemmatised_messages[m])) # Тональность собщений без учёта нулевых значений, но с учётом нейтральных
    else:
        results_2.append(0.0)

    message = []
    for w in range(len(lemmatised_messages[m])):
        if lemmatised_messages[m][w] >= 0.55 or lemmatised_messages[m][w] <= -0.5:
            message.append(lemmatised_messages[m][w])
    if message != []:
        results_3.append(mean(message))
    else:
        results_3.append(0.0)

with open('anylised_messages.csv', 'w', encoding='utf-8') as f:
    fieldnames = ['id', 'messages', 'result_1', 'result_2', 'result_3']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for m in range(len(messages_4_csv)):
        writer.writerow({'id': m, 'messages': messages_4_csv[m], 'result_1': results_1[m], 'result_2': results_2[m], 'result_3': results_3[m]})
