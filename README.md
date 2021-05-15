# Автоматическое определение эмоций в текстах сообщений
<img align="right" src="https://www.24forexsecrets.com/wp-content/uploads/2018/01/1-1.jpg">
Программа, подсчитывающая тональность сообщений из чатов Телеграм несколькими способами. В процессе работы над проетом должен быть выделен оптимальный способ.
<a href="https://drive.google.com/drive/folders/1tjKLL1uipkGzhlPssxubjEQUna0osp0d?usp=sharing" download="">Скачать</a>

## Подробное описание

- В итоге должна получиться программа
- Как входные данные программа принимает выгруженный из Телеграма чат (html-файл)
- Программма будет использовать модули re, pymorphy2, csv, statistics
- Используются тональный словарь русского языка (https://github.com/dkulagin/kartaslov/tree/master/dataset/emo_dict), корпуса с размеченной тональностью сообщений RuSentiment (https://github.com/text-machine-lab/rusentiment)

## Критерий завершенного проекта

В завершённом виде программа принимает html-файл с экспортированным из Телеграма чатом, возвращает csv-таблицу с подсчитанной тональностью для каждого сообщения

## Таймлайн проекта

К 9 мая будут сделаны:
- Функции для предобработки html-файла с чатом (разбивка на слова + лемматизация) (готово)
- Несколько алгоритмов для определения тональности сообщений (готово)
- Алгоритмы для определения частотности слова (готово)
- Презентация для предзащиты проекта (готово)

К 15 мая будут сделаны:
- Запись результатов в csv-таблицу (готово)
- Проверка работы кода на нескольких чатах, корпусах RuSentiment (готово)
- Выбор оптимального алгоритма подсчёта тональности (готово)
- Презентация для защиты проекта

## Алгоритмы

1. По значению полярности слова в диапазоне от -1 до 1, считая слова, которых нет в тональном словаре;
2. По значению полярности слова, не считая слова, которых нет в тональном словаре, но считая нейтральные слова (в диапазоне от -0.5 до 0.5);
3. По значению полярности слова, не считая слова, которых нет в тональном словаре, не считая нейтральные слова;
4. По тегу (количество NEUT, POS, NGTV), учитывая нейтральные слова;
5. По тегу, не учитывая нейтральные слова.

## Чего нам не хватает для реализации проекта

- Нейросети

## Распределение обязанностей в команде

- Дарья Проскурякова БКЛ201 - лемматизация, запись результатов в csv-таблицу
- Ангелина Степанова БКЛ201 - алгоритмы для определения тональности по value, определение частотности слов
- София Землянская БКЛ201 - алгоритмы для определения тональности по tag, поиск словарей и корпусов
