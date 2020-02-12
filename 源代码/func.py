# --coding:utf-8--
"""
企业对大数据要求最迫切的前十名招聘职位
大数据职位需求量最高的前10名城市
大数据职位需求量最高的前10大行业（如互联网、金融、电子商务等）
计算机相关专业技能需求前10名。
计算机专业薪水最高的前10名招聘职位
企业对哪类大数据人才需求最为迫切（大数据分析师、大数据架构师等等）
"""
import logging

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

import re

# import gensim_search
import db_connect
import money_int
import resume
import welf_search

# Format：设置log的显示格式（即在文档中看到的格式）。分别是时间+当前文件名+log输出级别+输出的信息
# Level：输出的log级别，优先级比设置的级别低的将不会被输出保存到log文档中
# 优先级是:NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
logging.basicConfig(filename="./log/" + __name__ + '.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
                    level=logging.INFO, filemode='a+', datefmt='%Y-%m-%d-%I:%M:%S %p')
# 日志输出内容
# ERROR：错误的简短描述，和该错误相关的关键参数，如果有异常，要有该异常的StackTrace。
# WARN：告警的简短描述，和该错误相关的关键参数，如果有异常，要有该异常的StackTrace。
# INFO：言简意赅地信息描述，如果有相关动态关键数据，要一并输出，比如相关ID、名称等。
# DEBUG：简单描述，相关数据，如果有异常，要有该异常的StackTrace。
# 在日志相关数据输出的时要特别注意对敏感信息的保护，比如修改密码时，不能将密码输出到日志中。
# log书写规范
# 函数开始与结束添加log，方便查看程序运行流程。
# 函数传入参数与返回参数使用log打印，方便查看参数是否传递错误。
# log中含义不清晰数据（如：单纯的数字等）可转换为能表达含义的字符串进行打印。
# log格式统一，如大小写，同一数据名称等。
# log分级别打印，方便调试与查看。


app = Flask(__name__)
CORS(app)
dbUtil = db_connect.DbConnect(host='localhost', user='root', passwd='1234', db='51job', port=3306, charset='utf8')
"""
以下5段@app.route和对应路由函数不可注释
"""

# ----------------------------------------------------------------------------------------
'''
以下5个函数是在浏览器中输入url时返回特定页面
起始页localhost:5000/main.html就是基于第四个路由函数返回的main.html
路由的选择规则是如果同时有/<var>和/position.html，则输入/position.html会执行/position.html的路由函数，不会去执行/<var>对应的路由函数
即具体路由优先，带变量的路由次之

下面5个函数是返回具体页面的，所有比如/localhost:5000/main.html和从main.html中点击跳转到的页面，因为href的结尾都是.html，所以跳转到的页面也是通过以下
5个函数生成的；又因为templates里面没有按照jinja2模板书写，所以跳转到的页面和main.html都是静态页面，没有数据

跳转到的页面可以点击按钮发送请求，发送的ajax请求url都不带.html，所以会被下面的例如/zhuanye/ruanjiankaifa绑定的路由函数接收，从而返回json数据，此时页面没有重新加载，而是本身没有数据的echarts获得了数据从而显示了

即本身echarts就显示了，只不过因为数据为空看不见
发送了ajax请求后数据不空了，自然就能看见了
'''


@app.route('/zhuanye/<var>', methods=['POST', 'GET'])
def to_zhuanye_page(var):
    logging.debug("-------------------into /zhuanye/<%s>'s to_zhuanye_page:-------------------" % var)
    if '.html' not in var:
        var += '.html'
    logging.debug("\tto_zhuanye_page(var) render_template('/zhuanye/%s')" % var)
    logging.debug("-------------------exit /zhuanye/<%s>'s to_zhuanye_page:-------------------" % var)
    return render_template('/zhuanye/' + var)


@app.route('/xuqiu/<var>', methods=['POST', 'GET'])
def to_xuqiu_page(var):
    logging.debug("-------------------into /xuqiu/<%s>'s to_xuqiu_page:-------------------" % var)
    if '.html' not in var:
        var += '.html'
    logging.debug("\tto_xuqiu_page(var) render_template('/xuqiu/%s')" % var)
    logging.debug("-------------------exit /xuqiu/<%s>'s to_xuqiu_page:-------------------" % var)
    return render_template('/xuqiu/' + var)


@app.route('/salary/<var>', methods=['POST', 'GET'])
def to_salary_page(var):
    logging.debug("-------------------into /salary/<%s>'s to_salary_page:-------------------" % var)
    if '.html' not in var:
        var += '.html'
    logging.debug("\tto_salary_page(var) render_template('/salary/%s')" % var)
    logging.debug("-------------------exit /salary/<%s>'s to_salary_page:-------------------" % var)
    return render_template('/salary/' + var)


@app.route('/<var>', methods=['POST', 'GET'])
def to_new_page(var):
    logging.debug("-------------------into /<%s>'s to_new_page:-------------------" % var)
    except_list = ['position.html', 'city.html', 'talents.html', 'welfare.html', 'location.html', 'resume.html']
    if var not in except_list:
        logging.debug('\tto_new_page(var) var=%s not in except_list即不合法的访问url会重新更改为main.html' % var)
        var = 'main.html'
    if var != 'favicon.ico' and '.html' not in var:
        logging.debug("%s != 'favicon.ico' and '.html' not in %s" % (var, var))
        var += '.html'
    logging.debug("\tto_new_page(var) render_template('%s')" % var)
    logging.debug("-------------------exit /<%s>'s to_new_page:-------------------" % var)
    return render_template(var)


@app.route('/articles/<var>', methods=['POST', 'GET'])
def to_articles_page(var):
    logging.debug("-------------------into /articles/<%s>'s to_articles_page:-------------------" % var)
    if '.html' not in var:
        var += '.html'
    logging.debug("\tto_articles_page(var) render_template('/articles/%s')" % var)
    logging.debug("-------------------exit /articles/<%s>'s to_articles_page:-------------------" % var)
    return render_template('/articles/' + var)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量、最高薪资，并返回为echarts适合的格式
对应网页内容为计算机专业职位薪水分析，点击默认跳转为/zhuanye/ruanjiankaifa.html
'''


def search_major_data(sql):
    logging.info("-------------------into search_major_data:-------------------")
    logging.info("\tsearch_major_data(sql) argument sql: %s" % sql)
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))

    # 处理数据使其符合echarts要求
    result_list_sorted_by_money = money_int.money_str2int(result_list)
    for i in range(len(result_list_sorted_by_money)):
        data_list.append({'name': result_list_sorted_by_money[i][0],
                          'value': str(result_list_sorted_by_money[i][1])})
    logging.info("\tsearch_major_data(sql) 查询结果data_list的内容是:%s" % str(data_list))
    logging.info("-------------------exit search_major_data:-------------------")
    return data_list


# TODO 可选 与前端协商修改ajax的请求url从而简化下面的后端代码


# 职位名，薪水
@app.route('/zhuanye/ruanjiankaifa', methods=['GET', 'POST'])
def query_major_rk():
    # TODO 可选 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/ruanjiankaifa's query_major_rk:-------------------")
    sql = "SELECT title, COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE title LIKE('%开发%') AND MATCH (info) AGAINST ('+软件开发' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_rk() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/ruanjiankaifa's query_major_rk:-------------------")
    return jsonify(data_list)


@app.route('/zhuanye/ruanjianceshi', methods=['GET', 'POST'])
def query_major_rc():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/ruanjianceshi's query_major_rc:-------------------")
    sql = "SELECT title,COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE title LIKE('%测试%') AND MATCH (info) AGAINST ('+软件测试' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0 \
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_rc() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/ruanjianceshi's query_major_rc:-------------------")
    return jsonify(data_list)


@app.route('/zhuanye/wangluoanquan', methods=['GET', 'POST'])
def query_major_wa():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/wangluoanquan's query_major_wa:-------------------")
    sql = "SELECT title,COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE MATCH (info) AGAINST ('+网络安全' IN BOOLEAN MODE) OR title LIKE('%网络%')\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_wa() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/wangluoanquan's query_major_wa:-------------------")
    return jsonify(data_list)


@app.route('/zhuanye/dianzishangwu', methods=['GET', 'POST'])
def query_major_ds():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/dianzishangwu's query_major_ds:-------------------")
    sql = "SELECT title,COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE MATCH (info) AGAINST ('+电子商务' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_ds() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/dianzishangwu's query_major_ds:-------------------")
    return jsonify(data_list)


@app.route('/zhuanye/tongxinyuanli', methods=['GET', 'POST'])
def query_major_tx():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/tongxinyuanli's query_major_tx:-------------------")
    sql = "SELECT title,COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE title LIKE('%通信%') OR MATCH (info) AGAINST ('+通信原理' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_tx() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/tongxinyuanli's query_major_tx:-------------------")
    return jsonify(data_list)


@app.route('/zhuanye/duomeitijishu', methods=['GET', 'POST'])
def query_major_dmt():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /zhuanye/duomeitijishu's query_major_dmt:-------------------")
    sql = "SELECT title,COUNT(title), (AVG(least_money) + AVG(most_money)) / 2 as avgsalary\
        FROM job\
        WHERE MATCH (info) AGAINST ('+多媒体技术' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_major_dmt() call search_major_data")
    data_list = search_major_data(sql)
    logging.info("-------------------exit /zhuanye/duomeitijishu's query_major_dmt:-------------------")
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量，并返回为echarts适合的格式
对应网页内容为计算机相关专业技能分析，点击默认跳转为/xuqiu/ruanjiankaifa.html
'''


def search_demand_data(sql):
    logging.info("-------------------into search_demand_data:-------------------")
    logging.info("\tsearch_demand_data(sql) argument sql: %s" % sql)
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0

    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})

    logging.info("\tsearch_demand_data(sql) 查询的结果data_list的内容是:%s" % str(data_list))
    logging.info("-------------------exit search_demand_data:-------------------")
    return data_list


# 职位名，需求量百分比
@app.route('/xuqiu/ruanjiankaifa', methods=['GET', 'POST'])
def query_demand_rk():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/ruanjiankaifa's query_demand_rk:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE title LIKE('%开发%') OR MATCH (info) AGAINST ('+软件开发' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "

    logging.info("\tquery_demand_rk() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/ruanjiankaifa's query_demand_rk:-------------------")
    return jsonify(data_list)


# TODO 可选 根据职能类别将重复的比如"软件测试"和"软件测试工程师"合并成一类
@app.route('/xuqiu/ruanjianceshi', methods=['GET', 'POST'])
def query_demand_rc():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/ruanjianceshi's query_demand_rc:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE title LIKE('%测试%') OR MATCH (info) AGAINST ('+软件测试' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0 \
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_demand_rc() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/ruanjianceshi's query_demand_rc:-------------------")
    return jsonify(data_list)


@app.route('/xuqiu/wangluoanquan', methods=['GET', 'POST'])
def query_demand_wa():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/wangluoanquan's query_demand_wa:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE MATCH (info) AGAINST ('+网络安全' IN BOOLEAN MODE) OR title LIKE ('%网络%')\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_demand_wa() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/wangluoanquan's query_demand_wa:-------------------")
    return jsonify(data_list)


@app.route('/xuqiu/dianzishangwu', methods=['GET', 'POST'])
def query_demand_ds():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/dianzishangwu's query_demand_ds:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE MATCH (info) AGAINST ('+电子商务' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_demand_ds() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/dianzishangwu's query_demand_ds:-------------------")
    return jsonify(data_list)


@app.route('/xuqiu/tongxinyuanli', methods=['GET', 'POST'])
def query_demand_tx():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/tongxinyuanli's query_demand_tx:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE MATCH (info) AGAINST ('+通信原理' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_demand_tx() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/tongxinyuanli's query_demand_tx:-------------------")
    return jsonify(data_list)


@app.route('/xuqiu/duomeitijishu', methods=['GET', 'POST'])
def query_demand_dmt():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /xuqiu/duomeitijishu's query_demand_dmt:-------------------")
    sql = "SELECT title,COUNT(title)\
        FROM job\
        WHERE MATCH (info) AGAINST ('+多媒体' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    logging.info("\tquery_demand_dmt() call search_demand_data")
    data_list = search_demand_data(sql)
    logging.info("-------------------exit /xuqiu/duomeitijishu's query_demand_dmt:-------------------")
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量，并返回为echarts适合的格式
对应网页内容为大数据职位需求量行业分析,对应页面为/position.html
'''


# 职位名，需求量
@app.route('/position', methods=['GET', 'POST'])
def query_position():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /position's query_position:-------------------")
    sql = "SELECT title,COUNT(title) as titlenum\
        FROM job\
        WHERE MATCH (info) AGAINST ('+大数据' IN BOOLEAN MODE)\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    global dbUtil
    data_dict = {'names': [], 'values': []}
    result_list = list(dbUtil.query(sql))
    num = 0

    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_dict['names'].append(result_list[i][0])
    for i in range(len(result_list)):
        data_dict['values'].append(int((result_list[i][1])))

    logging.info("\tquery_position() 查询的结果data_dict的内容是:%s" % str(data_dict))
    logging.info("-------------------exit /position's query_position:-------------------")
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为大数据职位需求量城市分析，对应页面为/city.html
'''


# 城市名，需求量
@app.route('/city', methods=['GET', 'POST'])
def query_city():
    # TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
    logging.info("-------------------into /city's query_city:-------------------")
    sql = "SELECT place_province,COUNT(place_province) as num\
        FROM job\
        WHERE MATCH (info) AGAINST ('+大数据' IN BOOLEAN MODE)\
        GROUP BY place_province HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0

    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})

    logging.info("\tquery_city() 查询的结果data_list的内容是:%s" % str(data_list))
    logging.info("-------------------exit /city's query_city:-------------------")
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为企业所需数据人才分析，对应页面为/talents.html
'''


# TODO 将ORDER BY的COUNT(title)变为COUNT(worktype)，worktype字段由爬取数据时获得的职能类别确认
# 专业名，需求量
@app.route('/talents', methods=['GET', 'POST'])
def query_talents():
    logging.info("-------------------into /talents's query_talents:-------------------")
    sql = "SELECT title,COUNT(title) as titlenum\
        FROM job\
        WHERE MATCH (info) AGAINST ('+大数据' IN BOOLEAN MODE) and title LIKE '%师'\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        "
    global dbUtil
    data_dict = {'names': [], 'values': [], 'extra': []}
    result_list = list(dbUtil.query(sql))
    num = 0

    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_dict['names'].append({"name": result_list[i][0]})
        data_dict['extra'].append(result_list[i][0])
    for i in range(len(result_list)):
        data_dict['values'].append(int((result_list[i][1])))

    logging.info("\tquery_talents() 查询的结果data_dict的内容是:%s" % str(data_dict))
    logging.info("-------------------into /talents's query_talents:-------------------")
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为企业所提供福利分析，对应页面为/welfare.html
'''


# 职位名，百分比
@app.route('/welfare', methods=['GET', 'POST'])
def query_welfare():
    logging.info("-------------------into /welfare's query_welfare:-------------------")
    if request.method == 'POST':
        welfare_num = request.form.get('welfare_num')

    elif request.method == 'GET':
        welfare_num = request.args.get('welfare_num')
    logging.info("\tquery_welfare() welfare_num=%s" % str(welfare_num))

    data_dict = {'data': []}
    logging.info("\tquery_welfare() call welf_search.search_welf(welfare_num)")
    data_dict['data'] = welf_search.search_welf(welfare_num)

    logging.info("\tquery_welfare() 查询的结果data_dict的内容是:%s" % str(data_dict))
    logging.info("-------------------exit /welfare's query_welfare:-------------------")
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询不重复的省和省中工作的数量，并返回为echarts适合的格式
其中网页内容为职位地域分布，对应页面为/location.html
'''


# 省，需求量
@app.route('/location', methods=['GET', 'POST'])
def query_location():
    logging.info("-------------------into /location's query_location:-------------------")
    sql = "SELECT DISTINCT place_province,COUNT(place_province)\
        FROM job\
        GROUP BY place_province HAVING COUNT(*) > 0\
        "
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0

    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})

    logging.info("\tquery_location() 查询的结果data_list的内容是:%s" % str(data_list))
    logging.info("-------------------exit /location's query_location:-------------------")
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询特定省市的工作的工作城市、最低薪资、最高薪资，并返回为echarts适合的格式
对应网页内容为省份工资调查，页面为/salary/XXX.html，其中XXX是城市拼音或拼音缩写
'''


def search_salary(sql):
    logging.info("-------------------into search_salary:-------------------")
    logging.info("\tsearch_salary(sql) argument sql: %s" % sql)
    global dbUtil
    data_dict = {}
    result_list = list(dbUtil.query(sql))

    # 处理数据使其符合echarts要求
    is_not_same = []

    least_money_list = money_int.get_least_money(result_list)
    most_money_list = money_int.get_most_money(result_list)
    least_money_temp_list = []
    most_money_temp_list = []

    for i in least_money_list:
        if i["地区名"] not in is_not_same:
            is_not_same.append(i["地区名"])
            least_money_temp_list.append({"地区名": i["地区名"], "最低工资": i["最低工资"]})

    is_not_same = []

    for i in most_money_list:
        if i["地区名"] not in is_not_same:
            is_not_same.append(i["地区名"])
            most_money_temp_list.append({"地区名": i["地区名"], "最高工资": i["最高工资"]})

    for i in range(len(least_money_temp_list)):
        least_money_temp_list[i]["最高工资"] = most_money_temp_list[i]["最高工资"]

    data_dict['numsh'] = []
    data_dict['numsl'] = []
    data_dict['names'] = []
    for i in range(len(least_money_temp_list)):
        data_dict['numsh'].append(least_money_temp_list[i]['最高工资'])
        data_dict['numsl'].append(least_money_temp_list[i]['最低工资'])
        data_dict['names'].append(least_money_temp_list[i]['地区名'])

    logging.info("\tsearch_salary(sql) 查询的结果data_dict的内容是:%s" % str(data_dict))
    logging.info("-------------------exit search_salary:-------------------")
    return data_dict


# 地区，最低，最高，
@app.route('/salary/beijing', methods=['GET', 'POST'])
def query_salary_bj():
    logging.info("-------------------into /salary/beijing's query_salary_bj:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='北京' AND place_city!='北京'\
        "

    logging.info("\tquery_salary_bj() call search_salary")
    data_dict = search_salary(sql)
    data_dict['names'].remove('昌平区')
    del data_dict['numsh'][5]
    del data_dict['numsl'][5]
    logging.info("-------------------exit /salary/beijing's query_salary_bj:-------------------")
    return jsonify(data_dict)


@app.route('/salary/chongqing', methods=['GET', 'POST'])
def query_salary_cq():
    logging.info("-------------------into /salary/chongqing's query_salary_cq:-------------------")
    sql = "SELECT DISTINCT place_city,least_money,most_money\
         FROM job\
         WHERE place_province='重庆' AND place_city!='重庆'\
         "
    logging.info("\tquery_salary_cq() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/chongqing's query_salary_cq:-------------------")
    return jsonify(data_dict)


@app.route('/salary/fujian', methods=['GET', 'POST'])
def query_salary_fj():
    logging.info("-------------------into /salary/fujian's query_salary_fj:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='福建' AND place_city!='福建'\
        "
    logging.info("\tquery_salary_fj() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/fujian's query_salary_fj:-------------------")
    return jsonify(data_dict)


@app.route('/salary/hebei', methods=['GET', 'POST'])
def query_salary_hb():
    logging.info("-------------------into /salary/hebei's query_salary_hb:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='河北' AND place_city!='河北'\
        "
    logging.info("\tquery_salary_hb() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/hebei's query_salary_hb:-------------------")
    return jsonify(data_dict)


# 没数据
@app.route('/salary/hunan', methods=['GET', 'POST'])
def query_salary_hn():
    logging.info("-------------------into /salary/hunan's query_salary_hn:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='湖南' AND place_city!='湖南'\
        "
    logging.info("\tquery_salary_hn() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/hunan's query_salary_hn:-------------------")
    return jsonify(data_dict)


# 没数据
@app.route('/salary/jiangsu', methods=['GET', 'POST'])
def query_salary_js():
    logging.info("-------------------into /salary/jiangsu's query_salary_js:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='江苏' AND place_city!='江苏'\
        "
    logging.info("\tquery_salary_js() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/jiangsu's query_salary_js:-------------------")
    return jsonify(data_dict)


# ？
@app.route('/salary/shandong', methods=['GET', 'POST'])
def query_salary_sd():
    logging.info("-------------------into /salary/shandong's query_salary_sd:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='山东' AND place_city!='山东'\
        "
    logging.info("\tquery_salary_sd() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/shandong's query_salary_sd:-------------------")
    return jsonify(data_dict)


# ？
@app.route('/salary/shanghai', methods=['GET', 'POST'])
def query_salary_sh():
    logging.info("-------------------into /salary/shanghai's query_salary_sh:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='上海' AND place_city!='上海'\
        "
    logging.info("\tquery_salary_sh() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/shanghai's query_salary_sh:-------------------")
    return jsonify(data_dict)


# ？
@app.route('/salary/zhejiang', methods=['GET', 'POST'])
def query_salary_zj():
    logging.info("-------------------into /salary/zhejiang's query_salary_zj:-------------------")
    sql = "SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province='浙江' AND place_city!='浙江'\
        "
    logging.info("\tquery_salary_zj() call search_salary")
    data_dict = search_salary(sql)
    logging.info("-------------------exit /salary/zhejiang's query_salary_zj:-------------------")
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询符合用户输入的内容的工作，并返回为echarts适合的格式
其中对应网页内容为简历分析，对应页面为/resume.html
'''


# 职业名&具体信息，匹配度
@app.route('/resume/', methods=['GET', 'POST'])
def query_keyword():
    logging.info("-------------------into /resume/'s query_keyword:-------------------")
    if request.method == 'POST':
        place = request.form.get('select1')
        major = request.form.get('select2')
        text = request.form.get('textArea1')

    elif request.method == 'GET':
        place = request.args.get('select1')
        major = request.args.get('select2')
        text = request.args.get('textArea1')

    logging.info("\tquery_keyword() call resume")
    res = resume.resume(place, major, text, dbUtil)
    logging.info("-------------------exit /resume/'s query_keyword:-------------------")
    return jsonify(res)


# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
