# coding=utf-8
from db_connect import DbConnect
import re


class ExtractKeyword:

    def __init__(self, query_num):
        self.dirty_data_list = []
        self.clean_data_list = []
        self.file_db_util = self.FileIOAndSQL(query_num)

    class FileIOAndSQL:
        def __init__(self, query_num):
            self.file_name = ""
            self.file_mode = ""
            self.file_encoding = ""
            self.db_util = DbConnect(host='localhost', user='root', passwd='1234', db='51job', port=3306,
                                     charset='utf8')
            self.query_num = query_num
            self.query_sql = "SELECT info FROM job LIMIT " + str(query_num) + ";"
            self.query_data = []

        def get_data(self):
            """
                执行查询并将结果赋值给成员变量
                """
            self.query_data = self.db_util.query(self.query_sql)
            return self.query_data

        def data2file(self, file_name, file_mode, file_encoding, data=[]):
            """
                使用filemode模式打开编码为fileencoding的filename文件，然后
                    若data非空，则写入data
                    若data空且self.query_data非空，则写入query_data
                """
            allow_mode = ['w', 'w+', "a", "a+"]
            if file_mode not in allow_mode:
                raise ModeErrorException()

            self.file_name = file_name
            self.file_mode = file_mode
            self.file_encoding = file_encoding

            with open(file=self.file_name, mode=self.file_mode, encoding=self.file_encoding) as f:
                if data:
                    for i in data:
                        try:
                            f.write(str(i) + '\n')
                        except:
                            raise IOError

                if not self.query_data:
                    self.get_data()

                for i in self.query_data:
                    try:
                        f.write(str(i) + '\n')
                    except:
                        raise IOError

        # TODO 分词后结果写入csv
        def data2csv(self):
            pass

    def clean_data(self, dirty_file_name, clean_file_name, file_mode, file_encoding="utf-8"):
        """
            去重和正则去除不相关符号，机械压缩去重在工作信息中不需要
            :param
                dirty_file_name:未清洗数据保存的文件名
                clean_file_name:清洗后数据保存的文件名
                file_mode:文件写入方式
                file_encoding:文件编码,默认utf-8
            """
        # 获取查询数据
        self.dirty_data_list = self.file_db_util.get_data()
        # 此处调用的data2file()是写入的查询数据，保存为dirty_file_name的文件
        self.file_db_util.data2file(dirty_file_name, file_mode, file_encoding)

        class TxtItem(object):
            """
                TxtItem是包含在clean_data中的一个内部类，旨在方便更好地使用set()去重
                TxtItem是ExtractKeyword对象的dirty_data列表的一条数据
                快速去重的思路是用切片代替整体比较
                """

            def __init__(self, record):
                self.record = record

            def __eq__(self, target):
                return self.record[:50] == target.record[:50]

        s = set()
        for record in self.dirty_data_list:
            try:
                s.add(record)
            except:
                pass

        unique_data_list = list(s)

        # 因为同一个文档中不会出现大量重复内容，因此无需机械压缩去词
        compressed_data_list = unique_data_list

        # 正则去除不相关符号和空白字符
        re_data_list = []
        for record in compressed_data_list:
            re_record = record
            try:
                # TODO 需要考虑是否需要(*)都去除
                re_record = re.sub(r"\(|\)|\s", "", record)
            except:
                pass
            re_data_list.append(re_record)
        self.clean_data_list = re_data_list

        # 将清洗后数据写入到clean_file_name的文件中，是调用的多一个data参数的data2file重载方法
        self.file_db_util.data2file(clean_file_name, file_mode, file_encoding, self.clean_data_list)
        pass

    # TODO 模型准备，暂时考虑LDA，可以使用百度api
    def model_prepare(self):
        pass

    # TODO jieba分词，定义词性，词频统计，自定义词库，tf-idf计算
    def jieba_cut_word(self):
        """
            分词又包括自定义词库，定义词性，词频统计，tf-idf权值计算
            最后得到的是jieba分词且通过tf-idf认为足够重要的关键词并写入数据库的keyword部分
            """
        # 流程是:1.读取cleanDevData.txt并提取每一条记录的info信息
        # 2.分词，去除停用词
        # 3.统计总体词频与文档词频，计算tf-idf权值，设定阈值，阈值过低的不视为关键词
        # 4.将关键词写入数据库与文件中
        # 5.生成词云
        pass

    # TODO 将jieba分词结果转为词向量
    def word2vec(self):
        """
            调用word2vec的方法将jieba分词后的关键词形成词向量
            """

        def similarity_calculation(self, target):
            """
                传入的词向量与本句的词向量计算余弦相似度进而判断两句话内容是否相似
                """
            # 流程是:1.对target进行分词，去除停用词
            # 2.对target中包含的诸如省市，工资范围，福利待遇之类的其他属性字段进行数据库筛选
            # 3.使用随机抽样的方法选取特定数量的样本，将每条记录的关键词字段转换为词向量，与target记录关键词字段转换为的词向量进行余弦相似度计算，若在此期间无满足阈值的记录出现，则重复该步骤
            # 4.返回余弦相似度最高的前5条记录，后5条记录作为可能感兴趣的工作返回工作名称，公司名称，职能类别，工作省市，工资范围
            pass

        pass

    # TODO 训练模型
    def model_training(self):
        # 通过模型训练聚类发现隐藏在不同工作之中的规律，同时帮助更好地计算余弦相似度(从广谱搜索->在类内搜索相似度最高的前5项)
        pass

    # TODO 整合至func中


class ModeErrorException(Exception):

    def __init__(self):
        self.data = "您选择的文件写入模式不在许可列表['w', 'w+', 'a','a+']内，" \
                    "请重新调用ExtractKeyword.data2file(self, filename, filemode, fileencoding)方法并传入正确的filemode参数"

    def __str__(self):
        print(self.data)


if __name__ == "__main__":
    total_num = 437852
    keyword_util = ExtractKeyword(20)

    dirty_file_name = r"./dirtyDevData.txt"
    clean_file_name = r"./cleanDevData.txt"
    file_mode = "w+"
    file_encoding = "utf-8"

    # clean_data就包括了写入文件和清洗文件的两个功能
    # 又因为f.write会额外写入()，所以提取时去除左右括号就是实际内容
    keyword_util.clean_data(dirty_file_name, clean_file_name, file_mode, file_encoding)
