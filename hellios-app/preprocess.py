import pandas as pd
import re
from urllib.parse import urlparse
import numpy as np
import json
import pathlib
from datetime import datetime
from datetime import timedelta
import codecs
import matplotlib.pyplot as plt
from itertools import groupby
from typing import List

import pickle
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

def spam_classification(df: pd.DataFrame) -> pd.DataFrame:
    device = 'cuda' if torch.cuda.is_available else 'cpu'

    tokenizer = AutoTokenizer.from_pretrained("lokas/spam-usernames-classifier")
    model = AutoModelForSequenceClassification.from_pretrained("lokas/spam-usernames-classifier").to(device)
    sm = torch.nn.Softmax()

    id2label = {0: 'Спам', 1: 'Не спам'}

    for i, row in tqdm(df.iterrows()):
        text = row['Текст сообщения']
        inputs = tokenizer(text, return_tensors='pt', truncation=True).to(device)
        res = sm(model(**inputs)[0]).view(-1)
        df.loc[i, 'Спам Модель'] = id2label[0 if res[0].item() > 0.8 else 1]
    return df


LIST_OF_ALLOWED_LINKS = [
    'discord.gg',
    'scratch.mit.edu',
    'www.figma.com',
    'replit.com',
    'colab.research.google.com',
    't.me',
    'github.com',
    'www.canva.com'
    ]

INTERVAL = timedelta(minutes=15)

f = codecs.open('obscene_corpus.txt', mode='r', encoding='utf-8')
OBSCENE_WORDS = f.read().replace('\n', ' ').lower()
f.close()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = AutoModelForSequenceClassification.from_pretrained('whatisslove11/labse').to(device)
tokenizer = AutoTokenizer.from_pretrained('whatisslove11/labse')

with open ("preds.pkl", "rb") as f:
    exec_le = pickle.load(f)

def has_obscene_words(a: str) -> int:
    """
    Поиск запрещенных слов на основе загруженного словаря.
    :param a: строка для поиска запрещенных слов
    :return: int/bool, есть ли как минимум одно запрещенное слово в строке (1 - да, 0 - нет)
    """
    for i in str(a).lower().split():
        if f" {i} " in OBSCENE_WORDS:
            return 1
    return 0


def clear_end_lesson(x: str) -> str:
    """
    Очистка формата данных "время" от ненужных символов. Написано только для определеного столбца
    Пример: 2024-03-06T10:53:03.124Z --> 2024-03-06 10:53:03
    :param x: строка для исправления
    :return: str, очищенная строка
    """
    if 'T' in x:
        x = x.replace('T', ' ')
        x = x[:-5]
    return x


def get_length_session(df: pd.DataFrame) -> pd.DataFrame:
    """
    Подсчет продолжительности лекции по последнему комментарию и столбцу "Дата старта урока"
    :param df: исходная таблица данных
    :return: pd.DataFrame, таблица данных с новой колонкой "Продолжительность лекции"
    """
    end_lesson = df.sort_values("Дата сообщения").groupby("ID урока")["Дата сообщения"].last()
    end_lesson = end_lesson.to_dict()
    df['Дата конца урока'] = df['ID урока'].apply(lambda x: end_lesson[x])
    df['Дата старта урока'] = df['Дата старта урока'].astype('datetime64[ns]')
    df['Дата конца урока'] = df['Дата конца урока'].apply(clear_end_lesson)
    df['Дата конца урока'] = df['Дата конца урока'].astype('datetime64[ns]')
    df['Продолжительность лекции'] = df['Дата конца урока'] - df['Дата старта урока']
    return df


def is_allowed_link(x: str) -> str:
    """
    Валидирование найденной ссылки на предмет разрешенного домена (можно ли ссылку данного типа кидать в чат или нет)
    :param x: найденная сслыка
    :return: str, метка одного из 2 классов, разрешена ли ссылка и найдена ли она в принципе
        "Нейтрально" - в приведенной строке ссылки не было/ссылка находится в реестре разрешенных
        "Запрещенка" - ссылка не находится в реестре разрешеннхы доменов
    """
    pattern = r'https?://\S+'
    is_match = re.search(pattern, x)
    if bool(is_match) is False:
        return 'Нейтрально'
    extracted_links = re.findall(pattern, x)
    extracted_domens = [urlparse(el).netloc for el in extracted_links]
    for link in extracted_domens:
        if link not in LIST_OF_ALLOWED_LINKS:
            return 'Запрещенка'
    return 'Нейтрально'


def get_count_comments_session(df: pd.DataFrame) -> pd.DataFrame:
    """
    Подсчет общего количества комментариев за прошедший урок
    :param df: исходная таблица данных
    :return: pd.DataFrame, таблица данных с новой колонкой "Количество комментариев"
    """
    count_of_classes = df.groupby(["ID урока"]).agg(['count'])['Дата старта урока']
    df['Количество комментариев'] = df['ID урока'].apply(lambda x: count_of_classes.loc[x, 'count'])

    return df


def get_difference_between_begin_first_comment_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Подсчет пройденного времени с начала урока до первого оставленного комментария в чате
    Может свидетельствовать о проблемах с чатом (считаем как тех. неполадка) или о низкой активности студентов
    :param df: исходная таблица данных
    :return: pd.DataFrame, таблица данных с новой колонкой "Разницу между началом и первым комментарием"

    Название этой функции писал Александр Калинин. Я оставил это чисто как мем.
    В случае проблем с кодом читайте вслух название этой функции как мантру.
    """
    id_difference = {}

    for i in df['ID урока'].unique():
        first_comment = df[df['ID урока'] == i].sort_values(by='Дата сообщения',
                                                            ascending=True).reset_index(drop=True)
        if not first_comment.empty:
            first_comment_date = datetime.strptime(str(first_comment.loc[0, 'Дата сообщения']),
                                                   '%Y-%m-%d %H:%M:%S')
            beginning_date = datetime.strptime(str(first_comment.loc[0, 'Дата старта урока']),
                                               '%Y-%m-%d %H:%M:%S')
            timestamp = first_comment_date - beginning_date
            id_difference[i] = timestamp

    # почему название этой колонки такое кривое? Нет, его писал не Александр Калинин. ЕГО ПИСАЛ ЕГОР.
    df['Разницу между началом и первым комментарием'] = df['ID урока'].apply(lambda id: id_difference[id])
    return df


def get_technical_errors_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Поиск ссылки в чате на платформу для проведения трансляций в последние Х% минут лекции
    Переход на платформу по типу дискорда и конец комментариев в чате могут свидетельствовать о технической неполадке.
    :param df: исходная таблица данных
    :return: pd.DataFrame, таблица данных с новой колонкой "Техническое перемещение"
    """
    is_technical_error = {}
    pattern = r'https://discord.gg'
    for el in df['ID урока'].unique():
        group = df[df['ID урока'] == el]
        last_20_percent_messanges = group.tail(int(0.2 * len(group)))
        is_link_discord = False
        for msg in last_20_percent_messanges['Текст сообщения']:
            is_match = re.search(pattern, msg)
            if is_match:
                is_link_discord = True
        is_technical_error[el] = is_link_discord
    df['Техническое перемещение'] = df['ID урока'].apply(lambda x: is_technical_error[x])
    return df

id2label = {
    '0': 'Very bad activity',
    '1': 'Bad activity',
    '2': 'Below average activity',
    '3': 'Average activity',
    '4': 'High activity',
    '5': 'Very high activity'
}

def check_activity(
        sliding_window_arr: List[int],
        overall_comments: int,
        user_overall_tr: int = 20
) -> str:
    activity_level = 3 # of 5
    if 0 in sliding_window_arr:
        max_seqs = max([len(list(seqs)) for n, seqs in groupby(sliding_window_arr) if n == 0])
    else:
        max_seqs = 0
    if max_seqs == 0:
        activity_level += 2
    elif max_seqs == 1:
        activity_level += 1
    elif max_seqs == 2:
        pass
    else:
        activity_level -= 1
    if overall_comments < user_overall_tr:
        activity_level -= 2
    elif user_overall_tr <= overall_comments < 1.7 * user_overall_tr:
        pass
    elif overall_comments >= 1.7 * user_overall_tr:
        activity_level += 1
    act2label = min(5, max(0, activity_level)) 
    return id2label[str(act2label)]

def predict(model, tokenizer, text_to_predict):
    model.to(device)

    encoding = tokenizer.encode_plus(
        text_to_predict,
        add_special_tokens=True,
        max_length=512,
        return_token_type_ids=False,
        truncation=True,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt'
    )

    out = {
        'text': text_to_predict,
        'input_ids': encoding['input_ids'].flatten(),
        'attention_mask': encoding['attention_mask'].flatten()
    }

    input_ids = out["input_ids"].to(device)
    attention_mask = out["attention_mask"].to(device)

    outputs = model(
        input_ids=input_ids.unsqueeze(0),
        attention_mask=attention_mask.unsqueeze(0)
    )

    prediction = torch.argmax(outputs.logits, dim=1).cpu().numpy()[0]
    label = exec_le.inverse_transform([prediction])

    tmp = {'tech_lose': 1, 'not_tech_lose': 0}
    
    return tmp[label[0]]  # not cat, numerical


def get_person_activities_feature(df: pd.DataFrame, id_lesson: int):
    """
    Подсчет количества комментариев в интервалах от k до k + INTERVAL минут.
    Пример: от 0 до 15 минут, от 15 до 30 минут и так до конца урока.

    Дополнительно создает json файл для построения диаграм.
    Исходя из количества комментариев в окне продолжительностью INTERVAL, можно анализировать пиковые моменты лекции.
    :param df: исходная таблица данных
    :return: None

    Если вы видите в конце названия функции слово feature - ЭТО ПИСАЛ АЛЕКСАНДР КАЛИНИН.
    """
    data = {}
    overall_stop_words = 0
    overall_banned_links = 0
    overall_tech_errors = 0
    activity_v2 = {}
    for el in df['ID урока'].unique():
        group = df[df['ID урока'] == el]
        group.set_index(pd.Index(np.arange(len(group))), inplace=True)
        list_times = []
        list_counts = []
        current_time = group.loc[0, 'Дата старта урока']
        while current_time <= group.loc[0, 'Дата конца урока']:
            list_times.append(str(current_time))
            list_counts.append(len(group[((group['Дата сообщения'] > current_time) & (
                    group['Дата сообщения'] <= current_time + INTERVAL))]))
            current_time += INTERVAL
        activity_v2[el] = check_activity(list_counts, sum(list_counts))
        stop_words_timestamps = []
        invalid_link_timestamps = []
        spam_count = 0
        for _, row in group.iterrows():
            if row['Наличие грубых слов'] == 1:
                stop_words_timestamps.append(str(row['Дата сообщения']))
                overall_stop_words += 1
            if row['Ссылки'] == 'Запрещенка':
                invalid_link_timestamps.append(str(row['Дата сообщения']))
                overall_banned_links += 1
            if row['Спам Модель'] == 'Спам':
                spam_count += 1
        overall_tech_errors += group.loc[0, 'Техническое перемещение']
        data[str(el)] = {
            'sliding_window_timestamps': list_times,
            'sliding_window_comments':list_counts,
            'stop_words_timestamps':stop_words_timestamps,
            'invalid_link_timestamps': invalid_link_timestamps,
            'validation_check_on_end_of_lesson': str(group.loc[0, 'Техническое перемещение']),
            'student_activity': activity_v2[el],
            'count_spam': spam_count
            # 'tech_losses_from_student': group.loc[0, 'Технические проблемы'],
            }
        if el == id_lesson:
            plt.bar(list_times, list_counts)
            plt.xticks(rotation=30, ha='right')
            plt.suptitle('Активность пользователей, распределенная по времени')
            plt.savefig('foo.png',dpi=400)
        
    df['Активность'] = df['ID урока'].apply(lambda x: activity_v2[x])

    with open('data.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return df, '\n'.join(['Количество стоп слов: ' + str(overall_stop_words), 'Количество забаненных ссылок: ' + str(overall_banned_links), 'Количество технических поломок: ' + str(overall_tech_errors)])


def data_processing(file: str, obscene_words: str='', allowed_links: str='', interval: int=15, id_lesson: int=321813) -> pd.DataFrame:
    """
    Просто запускает все ранее написанные функции и периодически кастует регулярки (и не только регулярки).
    :param file: путь до файла с данными
    :param obscene_words: путь до дополнительных грубых слов
    :param allowed_links: путь до дополнительных доступных ссылок
    :param interval: интервал для анализа активности пользователей во время урока
    :return: ps.DataFrame, файл с новыми колонками и очищенными данными
    """
    global INTERVAL, OBSCENE_WORDS, LIST_OF_ALLOWED_LINKS
    INTERVAL = timedelta(minutes=interval)
    if len(obscene_words) > 0:
        with open(obscene_words, mode='r') as file:
            new_words = file.readlines()
            new_words = ' '.join([el.replace('\n', '') for el in new_words])
        OBSCENE_WORDS += new_words

    if len(allowed_links) > 0:
        with open(allowed_links, mode='r') as file:
            new_links = file.readlines()
            new_links = [el.replace('\n', '') for el in new_links]
        LIST_OF_ALLOWED_LINKS.extend(new_links)
    
    file_ext = pathlib.Path(file).suffix
    if file_ext == '.xlsx':
        df = pd.read_excel(file)
    elif file_ext == '.csv':
        df = pd.read_csv(file)
    df = df.dropna(how='all')
    df = df.drop(columns=['Разметка', 'Роль пользователя', 'Unnamed: 6'])
    df = df.dropna()
    df['ID урока'] = df['ID урока'].astype('int')

    df = get_length_session(df)
    df['Текст сообщения'] = df['Текст сообщения'].apply(
        lambda x: re.sub('(; |)\d+\-\d+\-\d+T\d+\:\d+\:\d+\.\d+Z', ' ', x)
    )
    df['Ссылки'] = df['Текст сообщения'].apply(is_allowed_link)
    df['Дата сообщения'] = df['Дата сообщения'].apply(clear_end_lesson)
    df['Дата сообщения'] = df['Дата сообщения'].astype('datetime64[ns]')

    sorted_df = df.groupby('ID урока').apply(lambda x: x.sort_values('Дата сообщения')).reset_index(drop=True)
    sorted_df['Продолжительность урока в минутах'] = sorted_df['Продолжительность лекции'].apply(
        lambda x: round(x.seconds / 60, 2)
    )

    sorted_df = get_difference_between_begin_first_comment_feature(sorted_df)
    sorted_df['Наличие грубых слов'] = sorted_df['Текст сообщения'].apply(has_obscene_words)
    sorted_df = get_count_comments_session(sorted_df)
    sorted_df = get_technical_errors_feature(sorted_df)
    sorted_df = sorted_df.drop(columns=['Продолжительность лекции', 'Разницу между началом и первым комментарием'])
    sorted_df = spam_classification(sorted_df)
    # sorted_df['Технические проблемы'] = sorted_df['Текст сообщения'].apply(lambda x: predict(model, tokenizer, x))
    # count_of_problems = sorted_df.groupby(["ID урока"])['Технические проблемы'].sum().to_dict()
    # sorted_df['Технические проблемы'] = sorted_df['ID урока'].apply(lambda x: 0 if count_of_problems[x] < 2 else 1)
    # print(len(sorted_df[sorted_df['Технические проблемы'] == 1]))
    sorted_df, additional = get_person_activities_feature(sorted_df, id_lesson)
    sorted_df['Дата сообщения'] = sorted_df['Дата сообщения'].astype('str')
    sorted_df['Дата старта урока'] = sorted_df['Дата старта урока'].astype('str')
    sorted_df['Дата конца урока'] = sorted_df['Дата конца урока'].astype('str')
    return sorted_df, additional


if __name__ == "__main__":
    print(data_processing('train_GB_short_short.xlsx'))