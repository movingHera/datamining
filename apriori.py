#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
min_support = 14
min_confidence = 20
item_num = 11
num = [i for i in range(item_num)] # 记录item
support = [] # 计算support
location = [[i] for i in range(item_num)]
item_name = [] # 项目名
with open('basket.txt', 'r') as F:
    for index,line in enumerate(F.readlines()):
        if index == 0:
            item_name = [i for i in line.split(' ') if i][2:]
print item_name
def sut(location): # [[1,2,3],[2,3,4],[1,3,5]...]
    "支持度"
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
last_support = []
while num and location:
    print '-'*80
    print 'location' , location
    support = sut(location)
    # 筛选
    for index,i in enumerate(support):
        if i < 1000 * min_support / 100:
            support[index] = 0
    # 删除没用的位置
    location_delete = [i for i,j in zip(location,support) if j != 0]
    print 'location_deleted' , location_delete
    if not location_delete:
        print '-'*80
        break
    support = [i for i in support if i != 0]
    print 'support' , support
    last_support = support

    num = []
    for i in location_delete:
        num += i
    num = list(set(sorted(num)))
    print 'num' , num
    # 重新选择location
    location = select(location_delete, num, s)
    s += 1
    print '-'*80

def confidenc_sup():
    del_num = [num[:index] + num[index+1:] for index,i in enumerate(range(len(num)))]
    xy = sut(del_num)
    support_l =  float(last_support[0])/1000
    for index,i in enumerate(del_num):
        s = [j for index_item,j in enumerate(item_name) if index_item in i]
        print ','.join(s) , '->>' , item_name[num[index]] , ' min_support: ' , support_l , ' min_confidence:' , last_support[0]/float(xy[index])

confidenc_sup()

# location = select(location_delete, num, 2)
############################################################################
