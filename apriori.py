#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
min_support = 14
min_confidence = 20
item_num = 11
num = [i for i in range(item_num)]
support = []
location = [[i] for i in range(item_num)]
def sut(location):
    with open('basket.txt', 'r') as F:
        support = [0] * len(location)
        for index,line in enumerate(F.readlines()):
            if index == 0:
                continue
            # 提取每行信息
            item_line = [i.strip() for i in line.split(' ') if i][2:]
            for index_num,i in enumerate(location):
                flag = 0
                for j in i:
                    if item_line[j] != 'T':
                        flag = 1
                        break
                if not flag:
                    support[index_num] += 1
        return support

# # 第一次筛选
# for index,i in enumerate(support):
#     if i < 1000 * min_support / 100:
#         support[index] = 0
#         num = [i for i in num if i not in location[index]]
# # 删除位置
# location_delete = [i for i,j in zip(location,support) if j != 0]

def select(a,b,c):
    "返回位置"
    stack = []
    for i in a:
        for j in b:
            if j in i:
                if len(i) == c:
                    stack.append(i)
            else:
                stack.append([j] + i)
    # 多重列表去重
    import itertools
    s = [sorted(i) for i in stack]
    s.sort()
    tmp = list(s for s,_ in itertools.groupby(s))
    return tmp

s = 2
while num:
    print 'location' , location
    support = sut(location)
    print 'support' , support
    # 筛选
    for index,i in enumerate(support):
        if i < 1000 * min_support / 100:
            support[index] = 0
    # 删除没用的位置
    location_delete = [i for i,j in zip(location,support) if j != 0]
    print 'location_deleted' , location_delete
    num = []
    for i in location_delete:
        num += i
    num = list(set(sorted(num)))
    print 'num' , num
    # 重新选择location
    location = select(location_delete, num, s)
    s += 1

# location = select(location_delete, num, 2)
############################################################################
