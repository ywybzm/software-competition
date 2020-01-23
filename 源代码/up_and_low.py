# coding=utf-8
import re


def to_upper_case(result_url):
    text = ''
    with open(result_url, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(result_url, 'w+', encoding='utf-8') as f:
        f.write(text.upper())
