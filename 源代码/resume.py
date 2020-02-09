import jieba
import re
from gensim import corpora, models, similarities
from db_connect import DbConnect

size0 = 200
size1 = 100
size2 = 50
yy = 200
yy1 = 250

"""
    1.分词，去除停用词
    2.统计总体词频与文档词频，计算tf-idf权值，设定阈值，阈值过低的不视为关键词
    3.1阈值需要固定步长去试探，评判标准可以是机器学习中的查准率，查全率和F值
    3.2对所有阈值选择使用matplotlib绘制点线图查看拐点，对应阈值就是效果最好的阈值
    4.将关键词写入数据库与文件中
    5.生成词云
    
    实际工作流程是:
    1.对target进行分词，去除停用词
    2.对target中包含的诸如省市，工资范围，福利待遇之类的其他属性字段进行数据库筛选 √
    3.使用随机抽样的方法选取特定数量的样本，将每条记录的关键词字段转换为词向量，与target记录关键词字段转换为的词向量进行余弦相似度计算，若在此期间无满足阈值的记录出现，则重复该步骤
    4.返回余弦相似度最高的前5条记录，后5条记录作为可能感兴趣的工作返回工作名称，公司名称，职能类别，工作省市，工资范围

    """


def resume(place, major, text, db_util: DbConnect):
    if text != '':
        # TODO 使用随机抽样的方法选取特定数量的样本,确定合适的常数k
        k = 100  # 暂定
        # TODO 阈值需要固定步长去试探，评判标准可以是机器学习中的查准率，查全率和F值；对所有阈值选择使用matplotlib绘制点线图查看拐点，对应阈值就是效果最好的阈值
        threshold = 0.005
        sql = "select distinct title,company,least_money,most_money,keyword,info from job where keyword like '%" \
              + major + "%' or info like '%" + major + "%' or title like '%" + major + "%'  and place_province like '%" \
              + place + "%' or place_city like '%" + place + "%' limit " + str(k)  # 增加随机抽样的部分-即等距离选择特定数量样本

        data = db_util.query(sql)

        doc_test = text
        all_doc_chara = []
        all_doc = []
        try:
            for i in data:
                # all_doc存储的是对应字段内容是工作名称、公司名称、最低薪资、最高薪资、关键词、详细信息
                all_doc.append(i[0] + '-!-!-' + i[1] + '-!-!-' + i[2] + '-!-!-' + i[3] + '-!-!-' + i[4].split(' ')[5])
                # all_doc_chara是工作名称和详细信息拼接成的字符串的列表，若出现英文字符变为大写的方便统一，也是作为下面生成该工作关键词的来源
                all_doc_chara.append(
                    "".join(re.sub(r'[,，!?]', '', i[0].upper())) + "".join(re.sub(r'[,，!? ]', ' ', i[5].upper())))
            # TODO 生成词云
        except Exception as e:
            print(e)

        all_doc_list = []
        for doc in all_doc_chara:
            # TODO 去除停用词，使用自定义词典或者语料库优化切词效果
            # 对每一个工作名称和详细信息拼接成的字符串进行jieba.cut()切词
            doc_list = [word for word in jieba.cut(doc)]  # doc_list格式是['X','X','X']，X是切的词
            all_doc_list.append(doc_list)  # all_doc_list是所有记录切词的列表集合，格式是[ ['X','X'], ['X','X'], ['X','X'] ]

        # print(all_doc_list)#原文本的分词列表
        # TODO 去除停用词
        doc_test_list = [word for word in jieba.cut(doc_test)]  # doc_test_list是用户输入的信息切词的结果列表，格式是['X','X']

        # print(doc_test_list)  # 测试文本的分词列表
        dictionary = corpora.Dictionary(all_doc_list)
        # print(dictionary.keys())  # 原文本的字典键
        # print(dictionary.token2id)  # 原文本键键名对应
        corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]  # corpus是已有数据的切词结果生成的列表生成的句向量的列表
        # print(corpus)  # 原文本键和出现次数[[(),()],[(),()]]
        doc_test_vec = dictionary.doc2bow(doc_test_list) # 和上述corpus的生成方法是一致的，只不过文本只有很少一部分所以作为doc_test_vec
        # print(doc_test_vec)
        tfidf = models.TfidfModel(corpus)  # 不同的转化需要不同的参数，在TF-IDF转化中，训练的过程就是简单的遍历训练语料库(corpus)，然后计算文档中每个特征的频率。
        # 找到有特征性的词作为区分的标准，tf计算是局部的，idf计算是全局的
        # tf-idf算法是创建在这样一个假设之上的：对区别文档最有意义的词语应该是那些在文档中出现频率高，而在整个文档集合的其他文档中出现频率少的词语
        # 但是在本质上idf是一种试图抑制噪声的加权，并且单纯地认为文本频率小的单词就越重要，文本频率大的单词就越无用，显然这并不是完全正确的。idf的简单结构并不能有效地反映单词的重要程度和特征词的分布情况，使其无法很好地完成对权值调整的功能，所以tf-idf法的精度并不是很高。
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))

        sim = index[tfidf[doc_test_vec]]
        # print(sim)
        res = sorted(enumerate(sim), key=lambda item: -item[1])
        res_list = []
        child_res_dict = {'node': [], 'link': []}
        print(res)

        # 处理数据使其符合echarts要求

        cou_num = 1
        if len(res) <= 5:
            loop_num = len(res)
        else:
            loop_num = 8

        for i in range(0, loop_num):

            if res[i][1] > threshold:
                node_dict1 = {'name': '序号:' + str(i) + ',公司名:' + all_doc[res[i][0]].split('-!-!-')[1],
                              'value': '%.2f' % (res[i][1] * 1000), 'x': (cou_num + 1) * 10, 'y': 200,
                              'symbolSize': size1,
                              'label': {'normal': {'position': 'inside', 'fontSize': 10, 'color': '#FF6633'}},
                              "draggable": "true"}

                node_dict2 = {'name': '序号:' + str(i) + ',职位名:' + all_doc[res[i][0]].split('-!-!-')[0] + ',工资区间:' + \
                                      all_doc[res[i][0]].split('-!-!-')[2] + '-' + \
                                      all_doc[res[i][0]].split('-!-!-')[3],
                              'value': '%.2f' % (res[i][1] * 1000), 'x': (cou_num + 1) * 10, 'y': 200,
                              'symbolSize': size2,
                              'label': {'normal': {'position': 'inside', 'fontSize': 10, 'color': '#FF6633'}},
                              "draggable": "true"}
                if loop_num <= 5:
                    pass
                else:
                    node_dict3 = {'name': '序号:' + str(i) + ',关键词:' + all_doc[res[i][0]].split('-!-!-')[4],
                                  'value': '%.2f' % (res[i][1] * 1000), 'x': (cou_num + 1) * 10, 'y': 200,
                                  'symbolSize': size2,
                                  'label': {'normal': {'position': 'inside', 'fontSize': 10, 'color': '#FF6633'}},
                                  "draggable": "true"}
                cou_num += 3

                child_res_dict['node'].append(node_dict1)
                child_res_dict['node'].append(node_dict2)

                if loop_num <= 5:
                    pass
                else:
                    child_res_dict['node'].append(node_dict3)

                link_dict1 = {'source': '序号:' + str(i) + ',公司名:' + all_doc[res[i][0]].split('-!-!-')[1],
                              'target': '序号:' + str(i) + ',公司名:' + all_doc[res[i][0]].split('-!-!-')[1],
                              'name': '', 'value': '', 'label': '',
                              'lineStyle': {"normal": {"width": 2.0, "curveness": 0.2, "color": '#FF6633'}}}
                link_dict2 = {'source': '序号:' + str(i) + ',职位名:' + all_doc[res[i][0]].split('-!-!-')[0] + ',工资区间:' + \
                                        all_doc[res[i][0]].split('-!-!-')[2] + '-' + \
                                        all_doc[res[i][0]].split('-!-!-')[3],
                              'target': '序号:' + str(i) + ',公司名:' + all_doc[res[i][0]].split('-!-!-')[1],
                              'name': '', 'value': '', 'label': '',
                              'lineStyle': {"normal": {"width": 2.0, "curveness": 0.2, "color": '#FF6633'}}}

                if loop_num <= 5:
                    pass
                else:
                    link_dict3 = {'source': '序号:' + str(i) + ',关键词:' + all_doc[res[i][0]].split('-!-!-')[4],
                                  'target': '序号:' + str(i) + ',公司名:' + all_doc[res[i][0]].split('-!-!-')[1],
                                  'name': '', 'value': '', 'label': '',
                                  'lineStyle': {"normal": {"width": 2.0, "curveness": 0.2, "color": '#FF6633'}}}

                child_res_dict['link'].append(link_dict1)
                child_res_dict['link'].append(link_dict2)

                if loop_num <= 5:
                    pass
                else:
                    child_res_dict['link'].append(link_dict3)

        child_res_dict['node'].append({'name': '分析结果', 'value': '', 'x': 10, 'y': 200, 'symbolSize': size0,
                                       'label': {
                                           'normal': {'position': 'inside', 'fontSize': 14, 'color': '#FF6633'}},
                                       "draggable": "true"})
        copy_list = child_res_dict['link'].copy()
        for j in range(0, len(copy_list), 3):
            child_res_dict['link'].append({'source': copy_list[j]['source'],
                                           'target': child_res_dict['node'][len(child_res_dict['node']) - 1][
                                               'name'],
                                           'name': '', 'value': '', 'label': '', 'lineStyle': {
                    "normal": {"width": 2.0, "curveness": 0.2, "color": '#FF6633'}}})
        res_list.append(child_res_dict)
        return res_list

    else:
        return []
