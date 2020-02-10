def money_str2int(result_list):  # [(),()]
    res = []
    for i in range(len(result_list)):
        res.append((result_list[i][0], result_list[i][2]))

    return sorted(res, key=lambda money: money[1], reverse=True)


def get_least_money(result_list):  # [(),()]
    # print(result_list)
    res = []
    for i in range(len(result_list)):
        res.append({"地区名": result_list[i][0], "最低工资": '%.1f' % (int(result_list[i][1]) / 12 / 1000)})

    return res


def get_most_money(result_list):  # [(),()]
    res = []
    for i in range(len(result_list)):
        res.append({"地区名": result_list[i][0], "最高工资": '%.1f' % (int(result_list[i][2]) / 12 / 1000)})

    return res
