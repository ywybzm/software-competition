# coding=utf-8
import logging
import jieba
import re
import json
from collections import Counter


# [ [分词1],[分词2] ]
# def welf_divide(welf_list):
#     jieba.load_userdict('welf_word.txt')
#     result_list = []
#
#     for i in welf_list:
#         i = re.sub('五险一金补充|五险|一金', '五险一金', i)
#         result_list.append(jieba.cut(i))
#     return result_list


# [ (词,词频),(词,词频) ]
def count_num(welf_list, welfare_num):
    jieba.load_userdict('welf_word.txt')
    text = ''

    for i in welf_list:
        text = text + i
    text = re.sub('五险一金补充|五险|一金', '五险一金', text)
    result_list = jieba.cut(text)

    return Counter(result_list).most_common(int(welfare_num))


def divide():
    with open('./福利.json', 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub('},{', '}-!-!-{', text)
    with open('./福利.json', 'w+', encoding='utf-8') as f:
        f.write(text)

    result_list = re.findall('{.*}', text)[0].split('-!-!-')
    welf_list = []
    for i in result_list:
        try:
            data = json.loads(i)
            welf_list.append(data['公司待遇特色'])
        except:
            pass
    return welf_list


def welf_re(welfare_num):
    welf_list = divide()
    result_list = count_num(welf_list, welfare_num)

    return result_list


def search_welf(welfare_num):
    logging.info("-------------------into search_welf(welfare_num):-------------------")
    num = 0
    data_list = []
    result_list = welf_re(welfare_num)

    for i in result_list:
        num += i[1]

    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})
    # print(data_list)
    logging.info("\tsearch_welf(welfare_num)查询结果为%s" % str(data_list))
    logging.info("-------------------exit search_welf(welfare_num):-------------------")
    return data_list
