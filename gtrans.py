#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-22 18:41:57
# @Author  : Reynard (rey@pku.edu.cn)
# @Link    : link
# @Version : 1.0.0

import re
from google_trans_new import google_translator
from termcolor import cprint
from time import sleep


def clean_text(text):
    # TODO: 文本清洗
    # print(text)
    text = re.sub('(\[转发自.*\])\n', '', text)
    text = text.replace('\n', '/////')
    text = text.replace('#', ' ')
    text = filter_emoji(text)
    return (text)


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        res = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        res = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return res.sub(restr, desstr)


def big5(text):
    try:
        text.encode('big5hkscs')
        cprint('繁体', 'white', 'on_grey')
        result = True
    except Exception as e:
        cprint('简体' + e, 'white', 'on_grey')
        result = False
    return result


def trans(text, lang='zh-CN', detect=1):
    text = clean_text(text)
    tr = google_translator()
    if lang == 'en':
        result = get_trans(text, lang_tgt='en')
    elif lang == 'zh':
        result = get_trans(text, lang_tgt='zh-CN')
    elif lang == 'ru':
        result = get_trans(text, lang_tgt='ru')
    elif lang == 'ja':
        result = get_trans(text, lang_tgt='ja')
    elif lang == 'vi':
        result = get_trans(text, lang_tgt='vi')
    elif lang == 'pt':
        result = get_trans(text, lang_tgt='pt')
    else:
        if get_lang(text)[0] == 'zh-CN':
            result = get_trans(text, lang_tgt='zh-CN') + '\n' \
                     + get_trans(text, lang_tgt='en')
        else:
            result = get_trans(text, lang_tgt='zh-CN') + '\n' \
                     + text
    return result


def trans_auto(text):
    global resultNow
    text = clean_text(text)
    tr = google_translator()
    if get_lang(text)[0] == 'zh-CN':
        resultNow = get_trans(text, lang_tgt='en')
    elif get_lang(text)[0] == 'en':
        resultNow = get_trans(text, lang_tgt='zh-CN')
    else:
        zh = get_trans(text, lang_tgt='zh-CN')
        en = get_trans(text, lang_tgt='en')
        if zh == text:
            resultNow = get_trans(text, lang_tgt='en')
            print("resultNow1;" + resultNow)
        if en == text:
            resultNow = get_trans(text, lang_tgt='zh-CN')
            print("resultNow2;" + resultNow)
    return resultNow


def get_lang(text):
    translator = google_translator()
    lang = None
    while lang == None:
        try:
            lang = translator.detect(text)
        except:
            translator = Translator()
            sleep(0.1)
            pass
    return lang


# result = get_lang('hello')


def get_trans(text, **kwargs):
    translator = google_translator()
    result = None
    while result == None:
        try:
            result = translator.translate(text, **kwargs)
        except Exception as e:
            cprint('API Error' + str(e), 'white', 'on_yellow')
            translator = google_translator()
            sleep(0.1)
            pass
    return result


# result = get_trans('hello',lang_tgt='ja')

if __name__ == "__main__":
    print('Please run main.py instead of me!')
    pass
