"""
    data_clean流程:
        1.将原数据库数据读入至csv
        2.使用pandas读取csv，对数据进行清洗
        3.重新保存为新csv并将新csv加载至数据库中
"""

import pandas as pd
import db_connect
import re

db_util = db_connect.DbConnect(host='localhost', user='root', passwd='1234', db='51job', port=3306, charset='utf8')
total_num = 0

# 列名与数据对其显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 显示所有列
pd.set_option('display.max_columns', None)

# 显示所有行
pd.set_option('display.max_rows', None)

# 自定义每行最大长度
pd.set_option('max_colwidth', 600)

"""
    将数据写入csv
"""


def data2csv(data, file_name):
    print('data2csv:' + file_name)
    # 注释掉的是另一种写法
    # import csv
    # with open(file_name, 'w', newline='', encoding='utf-8') as t_file:
    #     csv_writer = csv.writer(t_file)
    #     csv_writer.writerow(['title', 'company', 'place_province', 'place_city', 'least_money', 'most_money',
    #                          'info', 'keyword'])
    #
    #     for i in data:
    #         csv_writer.writerow(i)
    data.to_csv(file_name, sep=',', index=False)


"""
    将数据写入数据库
"""


# TODO data2db函数会遇到The used command is not allowed with this MySQL version错误，但是直接把sql语句放在navicate里面能正常执行
#       所以转换思路，将所有要执行的load data语句按行写入文件中然后使用navicate的导入查询按行执行
def data2db(clean_csv_name, table_name):
    print('data2db')
    global db_util
    # print(clean_csv_name)
    update_sql = r"LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES" % (
        clean_csv_name, table_name)
    # print(update_sql)
    db_util.update(update_sql)


"""
    从数据库中读取数据
"""


def data_load(query_sql):
    global db_util
    return db_util.query(query_sql)


"""
    清洗数据
"""


# TODO 将清洗后数据放入列表中然后赋值给一个dataFrame对象，之后就可以调用方法写入csv和写入数据库
#      确定''在DataFrame中是否被标记为nan
def data_clean(dirty_csv_name):
    print('data_clean')
    # df.iloc()按下标搜索，df.loc()按行名列名搜索
    df = pd.read_csv(dirty_csv_name, sep=',', header=0)
    # 因为空值在招聘工作来看很少出现，选择直接删除的方式，下行表示只要某一行的某个列属性有空值就删除，并且在原数据集上操作
    df.dropna(axis=0, how='any', inplace=True)
    # 去重，只保留第一条，且在原有数据上修改
    df.drop_duplicates(keep='first', inplace=True)

    # 将字段内的英文,变为中文,防止读取csv时的格式混乱
    df['title'] = df['title'].str.replace(r',', '，', regex=True)
    # 将出现的多个* - # + 。 、变为一个空格
    df['title'] = df['title'].str.replace(r'[\*\-\#/\+。、]+', ' ', regex=True)
    # 左右中文括号变为英文括号
    df['title'] = df['title'].str.replace(r'（', '(')
    df['title'] = df['title'].str.replace(r'）', ')')
    # 把不配对左括号( （删除
    df['title'] = df['title'].str.replace(r'[\(（].*(?![\)）])', '', regex=True)
    # 删除连接的大段空白字符
    df['title'] = df['title'].str.replace(r'\s+', '', regex=True)
    # 针对cleanData0.csv而言出现过，NET->.NET
    df['title'] = df['title'].str.replace(r'，(?=N)', '.', regex=True)
    # 将后面不出现汉字英文字母数字小中大括号的多余前缀,，。.、?/-+!删除
    df['title'] = df['title'].str.replace(r'[,，\.。、\?/\-\+\!](?![\u4e00-\u9fa5a-zA-Z1-90\(\)（）【】\[\]\{\}])', '', regex=True)
    # title字段为空字符就设置为空好方便直接dropna
    df.loc[df['title'] == '', 'title'] = None
    df.dropna(axis=0, how='any', inplace=True)

    df['company'] = df['company'].str.replace(r',', '，', regex=True)

    # 将字段内的英文,变为中文,防止读取csv时的格式混乱
    df['info'] = df['info'].str.replace(r',', '，', regex=True)
    # 删除连接的大段空白字符
    df['info'] = df['info'].str.replace(r'\s+', '', regex=True)
    # 将出现的多个* - # + 。 、变为一个空格
    df['info'] = df['info'].str.replace(r'[\*\-\#/\+。、]+', ' ', regex=True)

    # print(df['keyword'])
    # place_province字段取值一律省略省，直辖市省略市，直辖区省略区
    normal_province = ['黑龙江', '吉林', '辽宁', '江苏', '山东', '安徽', '河北', '河南', '湖北', '湖南', '江西', '陕西', '山西', '四川', '青海',
                       '海南', '广东', '贵州', '浙江', '福建', '台湾', '甘肃', '云南']
    special_city = ['北京', '天津', '上海', '重庆']
    special_zone = ['内蒙古', '宁夏', '新疆', '西藏', '广西', '香港', '澳门']

    df.loc[df['place_province'].isin([i + '省' for i in normal_province] + special_zone), 'place_province'] = \
        df.loc[df['place_province'].isin(normal_province), 'place_province'].str.replace(r'省|(回族|维吾尔|壮族)?自治区', '',
                                                                                         regex=True)
    df.loc[df['place_province'].isin([i for i in special_city]), 'place_province'] = \
        df.loc[df['place_province'].isin(special_city), 'place_province'].str.replace(r'市', '', regex=True)

    # place_city非空，字段取值一律省略市;对于直辖市和直辖区来说，不统一所属区县;对于普通城市来说，统一区县至市
    df.loc[df['place_city'].isin(special_city), 'place_province'] = \
        df.loc[df['place_city'].isin(special_city), 'place_province'].str.replace(r'市', '', regex=True)

    # 以下是根据select place_province from job group by place_province发现的结果进行对应处理替换
    df.loc[df['place_city'] == '西昌', 'place_province'] = df.loc[df['place_city'] == '西昌', 'place_province'].str.replace(
        r'西昌', '四川', regex=True)
    df.loc[df['place_city'] == '北仓区', 'place_city'] = df.loc[df['place_city'] == '北仓区', 'place_city'].str.replace(
        r'北仓区', '宁波', regex=True)
    df.loc[df['place_city'] == '宁波', 'place_province'] = df.loc[df['place_city'] == '宁波', 'place_province'].str.replace(
        r'宁波', '浙江', regex=True)

    def money_process(money_str):
        # 将least_money和most_money的单位统一为千/月
        def strings2numbers(argument):
            switcher = {
                '万/年': '1 / 12 * 10',
                '万以下/年': '1 / 12 * 10',
                '万以上/月': '10',
                '万/月': '10',
                '千/月': '1',
                '千以下/月': '1',
                '元/天': '30 / 1000',
                '元/小时': '24 * 30 / 1000'
            }
            # 都没有时返回0
            return switcher.get(argument, '0')

        # 根据已有数据得到的结果有:
        # 万/年 万以下/年 万以上/月 万/月 千/月 千以下/月 元/天 元/小时
        unit_list = ['万/年', '万以下/年', '万以上/月', '万/月', '千/月', '千以下/月', '元/天', '元/小时']
        for i in unit_list:
            if money_str.find(i) != -1:
                money_str = re.sub(i, '', money_str)
                # print(money_str + '*' + strings2numbers(i), i)
                return round(float(eval(money_str + ' * ' + strings2numbers(i))), 2)
        return None

    # least_money和most_money非空，对df的两个money字段所有属性都统一单位至XX千/月
    df['least_money'] = df['least_money'].apply(lambda x: money_process(x))
    df['most_money'] = df['most_money'].apply(lambda x: money_process(x))

    # keyword非空；字段取值以“，”分隔，以“XX，XX，XX，XX”的形式存储关键词
    df['keyword'] = df['keyword'].apply(lambda x: re.sub(r'\s', '，', (re.sub(r'\s+', ' ', x))).strip('，'))
    # print(df.shape[0]) # 打印行数
    # print('------------------------------------------------------------------------------------------------------------')

    df.dropna(axis=0, how='any', inplace=True)
    clean_data_df = df
    # print(clean_data_df)
    return clean_data_df


"""
    按照写入原始数据至csv
        数据处理
        写入清洗后数据至csv
        写入数据库为方式调用各函数
    需注意的地方是，若一次性将所有数据读入dataframe会导致响应时间过长，故采取小碎步的思路，每选取2000条记录就写入一个csv中
"""


def data_process(start_num, step):
    dirty_csv_name = 'dirtyData'
    clean_csv_name = 'cleanData'
    absolute_csv_dir = r'D:/study/Pycharm/pycharm/QRdev/dataClean/clean/'
    table_name = 'job_copy'
    query_sql = 'SELECT * FROM job LIMIT ' + str(start_num) + ',' + str(step) + ';'

    dirty_data = data_load(query_sql)
    dirty_data_df = pd.DataFrame(columns=['title', 'company', 'place_province', 'place_city', 'least_money',
                                          'most_money', 'info', 'keyword'])
    print('select over')
    # 将记录写入dataframe
    for i in range(len(dirty_data)):
        dirty_data_df = dirty_data_df.append(pd.DataFrame({'title': [dirty_data[i][0]],
                                                           'company': dirty_data[i][1],
                                                           'place_province': dirty_data[i][2],
                                                           'place_city': dirty_data[i][3],
                                                           'least_money': dirty_data[i][4],
                                                           'most_money': dirty_data[i][5],
                                                           'info': dirty_data[i][6],
                                                           'keyword': dirty_data[i][7]}))
    global total_num
    print('todf over')
    data2csv(dirty_data_df, r'./dirty/' + dirty_csv_name + str(total_num) + '.csv')
    clean_data_df = data_clean(r'./dirty/' + dirty_csv_name + str(total_num) + '.csv')
    data2csv(clean_data_df, r'./clean/' + clean_csv_name + str(total_num) + '.csv')
    data2db(absolute_csv_dir + clean_csv_name + str(total_num) + '.csv', table_name)

    print('%sfinish' % start_num)
    total_num += 1
    print('----------------------------------------------------------------------------------')


if __name__ == "__main__":
    start_num = 0
    # 原始数据库总共记录数
    stop_num = 437852
    # 步长
    step = 2000
    # query_num = 10
    for i in range(1, 219):
        data_process(start_num, step)
        start_num += step


    def sql2file():
        with open(r'./test.sql', 'w', encoding='utf-8')  as f:
            for i in range(218):
                f.write(r"LOAD DATA LOCAL INFILE 'D:/study/Pycharm/pycharm/QRdev/dataClean/clean/cleanData"
                        + str(
                    i) + r".csv' INTO TABLE jobnew FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;" + '\n')


    # 生成需要导入navicate的sql语句文件
    sql2file()
    # 之后在navicate中新建查询-载入-选择相应文件-运行即可将数据库加载【前提是已经有了原始数据库的表】
