# -*- coding: utf-8 -*-

import requests
import os


def translate_it(source_file_path, target_file_path, translate_from, translate_into='ru'):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param
        source_file_path: <str> path to file to translate from.
        target_file_path: <str> path to file to translate into.
        translate_from: <str> lang to translate from.
        translate_into: <str> lang to translate into (default ru lang).
    :return: None.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    if not os.path.isdir(target_file_path):
        print('Target directory is not exist.')
        return

    with open(os.path.join(source_file_path, '{}.txt'.format(translate_from)),
              encoding='utf-8', mode='r') as sf:
        file_text = sf.read()

    params = {
        'key': key,
        'lang': '{}-{}'.format(translate_from, translate_into),
        'text': file_text,
    }

    response = requests.get(url, params=params).json()
    print(response['code'])
    translated_text = ' '.join(response.get('text', []))

    with open(os.path.join(target_file_path, '{}-{}.txt'.format(translate_from.upper(), translate_into.upper())),
              encoding='utf-8', mode='w') as tf:
        tf.write(translated_text)


translate_it('C:\\Dev\\Netology\\HW\\dz3.1', 'C:\\Dev\\Netology\\HW\\dz3.1\\Translated', 'de')
