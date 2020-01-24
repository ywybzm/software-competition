# TODO 查明为什么其余页面跳转有问题
# TODO 思考是否存在路由多次返回渲染后页面的结果

"""
企业对大数据要求最迫切的前十名招聘职位
大数据职位需求量最高的前10名城市
大数据职位需求量最高的前10大行业（如互联网、金融、电子商务等）
计算机相关专业技能需求前10名。
计算机专业薪水最高的前10名招聘职位
企业对哪类大数据人才需求最为迫切（大数据分析师、大数据架构师等等）
"""
# --coding:utf-8--
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
# import gensim_search
import welf_search
import db_connect
import money_int
import money_least
import money_most
import resume

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
    # print(var)
    if '.html' not in var:
        var += '.html'
    return render_template('/zhuanye/' + var)


@app.route('/xuqiu/<var>', methods=['POST', 'GET'])
def to_xuqiu_page(var):
    if '.html' not in var:
        var += '.html'
    return render_template('/xuqiu/' + var)


@app.route('/salary/<var>', methods=['POST', 'GET'])
def to_salary_page(var):
    if '.html' not in var:
        var += '.html'
    return render_template('/salary/' + var)


@app.route('/<var>', methods=['POST', 'GET'])
def to_new_page(var):
    except_list = ['position.html', 'city.html', 'talents.html', 'welfare.html', 'location.html', 'resume.html']
    if var not in except_list:
        var = 'main.html'
    if var != 'favicon.ico' and '.html' not in var:
        var += '.html'
    return render_template(var)


@app.route('/articles/<var>', methods=['POST', 'GET'])
def to_articles_page(var):
    if '.html' not in var:
        var += '.html'
    return render_template('/articles/' + var)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量、最高薪资，并返回为echarts适合的格式
对应网页内容为计算机专业职位薪水分析，点击默认跳转为/zhuanye/ruanjiankaifa.html
'''


def search_major_data(sql):
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    # 处理数据使其符合echarts要求
    result_list_sorted_by_money = money_int.money_str2int(result_list)
    for i in range(len(result_list_sorted_by_money)):
        data_list.append({'name': result_list_sorted_by_money[i][0],
                          'value': (int(result_list_sorted_by_money[i][1] / 1000 / 12))})
    dbUtil.close_connection()
    return data_list


# 职位名，薪水
@app.route('/zhuanye/ruanjiankaifa', methods=['GET', 'POST'])
def query_major_rk():
    sql = 'SELECT title,COUNT(title),most_money\
        FROM job\
        WHERE info LIKE "%软件开发%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


@app.route('/zhuanye/ruanjianceshi', methods=['GET', 'POST'])
def query_major_rc():
    sql = 'SELECT TITLE,COUNT(TITLE),MOST_MONEY\
        FROM job\
        WHERE info LIKE "%软件测试%"\
        GROUP BY title HAVING COUNT(*) > 0 \
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


@app.route('/zhuanye/wangluoanquan', methods=['GET', 'POST'])
def query_major_wa():
    sql = 'SELECT TITLE,COUNT(TITLE),MOST_MONEY\
        FROM job\
        WHERE info LIKE "%网络安全%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


@app.route('/zhuanye/dianzishangwu', methods=['GET', 'POST'])
def query_major_ds():
    sql = 'SELECT TITLE,COUNT(TITLE),MOST_MONEY\
        FROM job\
        WHERE info LIKE "%电子商务%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


@app.route('/zhuanye/tongxinyuanli', methods=['GET', 'POST'])
def query_major_tx():
    sql = 'SELECT TITLE,COUNT(TITLE),MOST_MONEY\
        FROM job\
        WHERE info LIKE "%通信原理%" and title LIKE "%通信%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


@app.route('/zhuanye/duomeitijishu', methods=['GET', 'POST'])
def query_major_dmt():
    sql = 'SELECT TITLE,COUNT(TITLE),MOST_MONEY\
            FROM job\
            WHERE info LIKE "%多媒体技术%"\
            GROUP BY title HAVING COUNT(*) > 0\
            ORDER BY COUNT(title) DESC\
            LIMIT 10\
            '
    data_list = search_major_data(sql)
    print(jsonify(data_list))
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量，并返回为echarts适合的格式
对应网页内容为计算机相关专业技能分析，点击默认跳转为/xuqiu/ruanjiankaifa.html
'''


def search_demand_data(sql):
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0
    # 处理数据使其符合echarts要求
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})
    return data_list


# 职位名，需求量百分比
@app.route('/xuqiu/ruanjiankaifa', methods=['GET', 'POST'])
def query_demand_rk():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE info LIKE "%软件开发%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


@app.route('/xuqiu/ruanjianceshi', methods=['GET', 'POST'])
def query_demand_rc():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE title LIKE "%测试%"\
        GROUP BY title HAVING COUNT(*) > 0 \
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


@app.route('/xuqiu/wangluoanquan', methods=['GET', 'POST'])
def query_demand_wa():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE info LIKE "%网络安全%" or title LIKE "%网络"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


@app.route('/xuqiu/dianzishangwu', methods=['GET', 'POST'])
def query_demand_ds():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE info LIKE "%电子商务%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
            '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


@app.route('/xuqiu/tongxinyuanli', methods=['GET', 'POST'])
def query_demand_tx():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE info LIKE "%通信原理%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


@app.route('/xuqiu/duomeitijishu', methods=['GET', 'POST'])
def query_demand_dmt():
    sql = 'SELECT TITLE,COUNT(TITLE)\
        FROM job\
        WHERE info LIKE "%多媒体%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    data_list = search_demand_data(sql)
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作名称、工作数量，并返回为echarts适合的格式
对应网页内容为大数据职位需求量行业分析,对应页面为/position.html
'''


# 职位名，需求量
@app.route('/position', methods=['GET', 'POST'])
def query_position():
    sql = 'SELECT title,COUNT(title) as titlenum\
        FROM job\
        WHERE info LIKE "%大数据%"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
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
    # print(data_dict)
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为大数据职位需求量城市分析，对应页面为/city.html
'''


# 城市名，需求量
@app.route('/city', methods=['GET', 'POST'])
def query_city():
    sql = 'SELECT place_province,COUNT(place_province) as num\
        FROM job\
        WHERE info LIKE "%大数据%"\
        GROUP BY place_province HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})
    # print(data_dict)
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为企业所需数据人才分析，对应页面为/talents.html
'''


# 专业名，需求量
@app.route('/talents', methods=['GET', 'POST'])
def query_talents():
    sql = 'SELECT title,COUNT(title) as titlenum\
        FROM job\
        WHERE info LIKE "%大数据%" and title LIKE "%师"\
        GROUP BY title HAVING COUNT(*) > 0\
        ORDER BY COUNT(title) DESC\
        LIMIT 10\
        '
    global dbUtil
    data_dict = {'names': [], 'values': [], 'extra': []}
    result_list = list(dbUtil.query(sql))
    num = 0
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_dict['names'].append({"name": result_list[i][0]})
        data_dict['extra'].append(result_list[i][0])
    for i in range(len(result_list)):
        data_dict['values'].append(int((result_list[i][1])))
    # print(data_dict)
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询info字段中含有对应专业的工作的工作省份及数量，并返回为echarts适合的格式
对应网页内容为企业所提供福利分析，对应页面为/welfare.html
'''


# 职位名，百分比
@app.route('/welfare', methods=['GET', 'POST'])
def query_welfare():
    if request.method == 'POST':
        welfare_num = request.form.get('welfare_num')

    elif request.method == 'GET':
        welfare_num = request.args.get('welfare_num')
    # print(jsonify(welf_search.Welf_Search(welfare_num)))
    data_dict = {'data': (welf_search.search_welf(welfare_num))}
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询不重复的省和省中工作的数量，并返回为echarts适合的格式
其中网页内容为职位地域分布，对应页面为/location.html
'''


# 省，需求量
@app.route('/location', methods=['GET', 'POST'])
def query_location():
    sql = 'SELECT DISTINCT place_province,COUNT(place_province)\
        FROM job\
        GROUP BY place_province HAVING COUNT(*) > 0\
        '
    global dbUtil
    data_list = []
    result_list = list(dbUtil.query(sql))
    num = 0
    for i in range(len(result_list)):
        num += result_list[i][1]
    for i in range(len(result_list)):
        data_list.append({'name': result_list[i][0], 'value': int((result_list[i][1]))})
    # print(data_dict)
    return jsonify(data_list)


# ----------------------------------------------------------------------------------------
'''
查询特定省市的工作的工作城市、最低薪资、最高薪资，并返回为echarts适合的格式
对应网页内容为省份工资调查，页面为/salary/XXX.html，其中XXX是城市拼音或拼音缩写
'''


def search_salary(sql):
    global dbUtil
    data_dict = {}
    result_list = list(dbUtil.query(sql))
    is_not_same = []

    res_sorted_by_least = money_least.get_least_money(result_list)
    res_sorted_by_most = money_most.get_money_most(result_list)

    res_fi1 = []
    res_fi2 = []

    for i in res_sorted_by_least:
        if i["地区名"] not in is_not_same:
            is_not_same.append(i["地区名"])
            res_fi1.append({"地区名": i["地区名"], "最低工资": i["最低工资"]})
    is_not_same = []
    for i in res_sorted_by_most:
        if i["地区名"] not in is_not_same:
            is_not_same.append(i["地区名"])
            res_fi2.append({"地区名": i["地区名"], "最高工资": i["最高工资"]})

    for i in range(len(res_fi1)):
        res_fi1[i]["最高工资"] = res_fi2[i]["最高工资"]

    data_dict['numsh'] = []
    data_dict['numsl'] = []
    data_dict['names'] = []
    for i in range(len(res_fi1)):
        data_dict['numsh'].append(res_fi1[i]['最高工资'])
        data_dict['numsl'].append(res_fi1[i]['最低工资'])
        data_dict['names'].append(res_fi1[i]['地区名'])
    return data_dict


# 地区，最低，最高，
@app.route('/salary/beijing', methods=['GET', 'POST'])
def query_salary_bj():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="北京" AND place_city!="北京"\
        '

    data_dict = search_salary(sql)
    data_dict['names'].remove('昌平区')
    del data_dict['numsh'][5]
    del data_dict['numsl'][5]
    # print(data_dict)
    return jsonify(data_dict)


@app.route('/salary/chongqing', methods=['GET', 'POST'])
def query_salary_cq():
    sql = 'SELECT DISTINCT place_city,least_money,most_money\
         FROM job\
         WHERE place_province="重庆" AND place_city!="重庆"\
         '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


@app.route('/salary/fujian', methods=['GET', 'POST'])
def query_salary_fj():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="福建" AND place_city!="福建"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


@app.route('/salary/hebei', methods=['GET', 'POST'])
def query_salary_hb():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="河北" AND place_city!="河北"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# 没数据
@app.route('/salary/hunan', methods=['GET', 'POST'])
def query_salary_hn():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="湖南" AND place_city!="湖南"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# 没数据
@app.route('/salary/jiangsu', methods=['GET', 'POST'])
def query_salary_js():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="江苏" AND place_city!="江苏"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# ？
@app.route('/salary/shandong', methods=['GET', 'POST'])
def query_salary_sd():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="山东" AND place_city!="山东"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# ？
@app.route('/salary/shanghai', methods=['GET', 'POST'])
def query_salary_sh():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="上海" AND place_city!="上海"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# ？
@app.route('/salary/zhejiang', methods=['GET', 'POST'])
def query_salary_zj():
    sql = 'SELECT  place_city,least_money,most_money\
        FROM job\
        WHERE place_province="浙江" AND place_city!="浙江"\
        '
    data_dict = search_salary(sql)
    return jsonify(data_dict)


# ----------------------------------------------------------------------------------------
'''
查询符合用户输入的内容的工作，并返回为echarts适合的格式
其中对应网页内容为简历分析，对应页面为/resume.html
'''


# 职业名&具体信息，匹配度
@app.route('/resume/', methods=['GET', 'POST'])
def query_keyword():
    if request.method == 'POST':
        select1 = request.form.get('select1')
        select2 = request.form.get('select2')
        testarea1 = request.form.get('textArea1')

    elif request.method == 'GET':
        select1 = request.args.get('select1')
        select2 = request.args.get('select2')
        testarea1 = request.args.get('textArea1')
    print(select1, select2, testarea1)
    res = resume.resume(select1, select2, testarea1, dbUtil)

    return jsonify(res)


# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
