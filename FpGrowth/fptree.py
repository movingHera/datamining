#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
def first_support(min_support):
    "第一次遍历生成字典"
    dict_item = {}
    with open('data.txt', 'r') as F:
        for line in F.readlines():
            item = [i.strip() for i in line.split(' ') if i]
            for i in item:
                if dict_item.has_key(i):
                    dict_item[i] += 1
                else:
                    dict_item[i] = 1
    dict_item = sorted(dict_item.iteritems(), key=lambda d:d[1], reverse = True)
    print dict_item

first_support(2)

############################################################################
