import logging


def money_str2int(result_list):  # [(),()]
    logging.info("-------------------into money_int's money_str2int:-------------------")
    res_list = []

    logging.debug("\tmoney_str2int(result_list) argument result_list=%s" % str(result_list))

    for i in range(len(result_list)):
        res_list.append((result_list[i][0], round(result_list[i][2], 2)))

    logging.info("\tmoney_str2int(result_list) 处理后的未排序的结果res_list为:%s" % str(res_list))
    logging.info("-------------------exit money_int's money_str2int:-------------------")
    return sorted(res_list, key=lambda money: money[1], reverse=True)


def get_least_money(result_list):  # [(),()]
    logging.info("-------------------into money_int's get_least_money:-------------------")
    res_list = []

    logging.debug("\tget_least_money(result_list) argument result_list=%s" % str(result_list))
    for i in range(len(result_list)):
        res_list.append({"地区名": result_list[i][0], "最低工资": '%.1f' % (round(result_list[i][1], 2))})

    logging.info("\tget_least_money(result_list) 处理后的结果res_list为:%s" % str(res_list))
    logging.info("-------------------exit money_int's get_least_money:-------------------")
    return res_list


def get_most_money(result_list):  # [(),()]
    logging.info("-------------------into money_int's get_most_money:-------------------")
    res_list = []

    logging.debug("\tget_most_money(result_list) argument result_list=%s" % str(result_list))
    for i in range(len(result_list)):
        res_list.append({"地区名": result_list[i][0], "最高工资": '%.1f' % (round(result_list[i][2], 2))})

    logging.info("\tget_most_money(result_list) 处理后的结果res_list为:%s" % str(res_list))
    logging.info("-------------------exit money_int's get_most_money:-------------------")
    return res_list
