# -*- coding: utf-8 -*-

import requests
import os

# key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
key = 'trnsl.1.1.20180802T194247Z.521749684a2bfa84.f1babf41d9e5828c83324c0c5e7c257623ed46d3'
detect_url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
translate_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
file_extension = 'txt'
target_dir_name = 'Translated'
case_sensitive = False


def file_read(file_name):
    with open(file_name, encoding='utf-8', mode='r') as fn:
        return fn.read()


def file_write(file_name, file_data):
    with open(file_name, encoding='utf-8', mode='w') as fn:
        fn.write(file_data)


def detect_language(text_data):
    detect_params = {
        'key': key,
        # 'hint': 'en,fr,es',
        'text': text_data,
    }
    response = requests.get(detect_url, params=detect_params).json()
    language = 'en'
    if response['code'] == 200:
        language = response['lang']
    return language


def translate_text(text_data, translate_from, translate_into):
    translate_params = {
            'key': key,
            'lang': f'{translate_from}-{translate_into}',
            'text': text_data,
        }
    response = requests.get(translate_url, params=translate_params).json()
    translated_text = ' '.join(response.get('text', []))
    return translated_text


def translate_it(translate_into='ru'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(current_dir)

    target_path = os.path.join(current_dir, target_dir_name)
    if not os.path.isdir(target_path):
        os.mkdir(target_path)
        print(f'Создана папка {target_path}')

    for file in file_list:
        if not case_sensitive:
            file = file.lower()
        if file.endswith(f'.{file_extension}'):
            file_contents = file_read(os.path.join(current_dir, file))
            translate_from = detect_language(file_contents)
            if translate_from == translate_into:
                continue
            new_text = translate_text(file_contents, translate_from, translate_into)
            target_file_name = f'{translate_from}-{translate_into}.txt'
            new_file = os.path.join(target_path, target_file_name)
            file_write(new_file, new_text)
            print(f'Перевод файла {file} записан в {target_file_name}.')


# translate_it('fr')
translate_it()
