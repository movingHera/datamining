#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
min_support = 5
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
def del_location(support, location):
    "清除不满足条件的候选集"
    # 筛选
    for index,i in enumerate(support):
        if i < 1000 * min_support / 100:
            support[index] = 0
    # 删除没用的位置
    location_delete = [i for i,j in zip(location,support) if j != 0]
    support = [i for i in support if i != 0]
    return support,location_delete

s = 2
last_support = []
pre_support = sut(location)
pre_location = location
pre_support_delete,pre_location_delete = del_location(pre_support,pre_location)
num = []
for i in pre_location:
    num += i
num = list(sorted(set(num)))
pre_num = num
# print pre_num
# print pre_location
# print pre_support
while num and location:
    print '-'*80
    print 'The' ,s - 1,'loop'
    print 'location' , pre_location
    print 'support' , pre_support
    print 'num' , pre_num
    print '-'*80

    # 生成下一级候选集
    location = select(pre_location, num, s)
    s += 1
    support = sut(location)
    support_delete,location_delete = del_location(support,location)
    if not location_delete:
        break
    num = []
    for i in location_delete:
        num += i
    num = list(sorted(set(num)))

    pre_num = num
    pre_location = location_delete
    pre_support = support_delete

def confidenc_sup():
    if sum(pre_support) == 0:
        print 'No min_support'
    else:
        del_num = [pre_num[:index] + pre_num[index+1:] for index,i in enumerate(range(len(pre_num)))]
        xy = sut(del_num)
        print del_num
        print pre_support
        for index,i in enumerate(del_num):
            index_support = 0
            if len(pre_support) != 1:
                index_support = index
            support =  float(pre_support[index_support])/1000
            s = [j for index_item,j in enumerate(item_name) if index_item in i]
            if xy[index]:
                print ','.join(s) , '->>' , item_name[pre_num[index]] , ' min_support: ' , support , ' min_confidence:' , float(xy[index])

confidenc_sup()

# location = select(location_delete, num, 2)
############################################################################
