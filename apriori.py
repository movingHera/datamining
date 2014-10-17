#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
min_support = 15
min_confidence = 20
item_num = 11 # 项目数
num = [i for i in range(item_num)] # 记录item
support = [] # 计算support
location = [[i] for i in range(item_num)]
item_name = [] # 项目名
def deal_line(line):
    "根据提取出需要的项"
    return [i.strip() for i in line.split(' ') if i][2:]

def find_item_name(filename):
    "根据第一行抽取item_name"
    with open(filename, 'r') as F:
        for index,line in enumerate(F.readlines()):
            if index == 0:
                item_name = deal_line(line)
                break
    return item_name

item_name = find_item_name('basket.txt')
print item_name

def sut(location):
    """
    输入[[1,2,3],[2,3,4],[1,3,5]...]
    输出每个位置集的support [123,435,234...]
    """
    with open('basket.txt', 'r') as F:
        support = [0] * len(location)
        for index,line in enumerate(F.readlines()):
            if index == 0: continue
            # 提取每行信息
            item_line = deal_line(line)
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
    s = sorted([sorted(i) for i in stack])
    tmp = list(s for s,_ in itertools.groupby(s))
    return tmp

def del_location(support, location,pre_location):
    "清除不满足条件的候选集"
    # 小于最小支持度的剔除
    for index,i in enumerate(support):
        if i < 1000 * min_support / 100:
            support[index] = 0
    # apriori第二条规则,剔除
    for index,j in enumerate(location):
        sub_location = [j[:index_loc] + j[index_loc+1:]for index_loc in range(len(j))]
        flag = 0
        for k in sub_location:
            if k not in pre_location:
                flag = 1
                break
        if flag:
            support[index] = 0
    # 删除没用的位置
    location = [i for i,j in zip(location,support) if j != 0]
    support = [i for i in support if i != 0]

    return support,location

s = 2
pre_support = sut(location)
pre_location = location
pre_num = list(sorted(set([j for i in pre_location for j in i])))
while num and location:
    print '-'*80
    print 'The' ,s - 1,'loop'
    print 'location' , pre_location
    print 'support' , pre_support
    print 'num' , pre_num
    print '-'*80

    # 生成下一级候选集
    location = select(pre_location, num, s)
    support = sut(location)
    support_delete,location_delete = del_location(support,location,pre_location)
    s += 1
    if not location_delete:
        break

    pre_num = list(sorted(set([j for i in location_delete for j in i])))
    pre_location = location_delete
    pre_support = support_delete

def confidenc_sup():
    if sum(pre_support) == 0:
        print 'min_support error'
    else:
        for index_location,each_location in enumerate(pre_location):
            del_num = [each_location[:index] + each_location[index+1:] for index in range(len(each_location))]
            xy = sut(del_num)
            print del_num
            print pre_support[index_location]
            print xy
            if not del_num[0]:
                print 'min_support error'
                break
            for index,i in enumerate(del_num):
                index_support = 0
                if len(pre_support) != 1:
                    index_support = index
                support =  float(pre_support[index_location])/10
                s = [j for index_item,j in enumerate(item_name) if index_item in i]
                if xy[index]:
                    print ','.join(s) , '->>' , item_name[pre_num[index]] , ' min_support: ' , str(support) + '%' , ' min_confidence:' , pre_support[index_location]/float(xy[index])

confidenc_sup()

############################################################################
