#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
class Apriori(object):

    def __init__(self, filename):
        self.min_support = 14
        self.min_confidence = 20
        self.item_num = 11 # 项目数

        self.location = [[i] for i in range(self.item_num)]
        self.support = self.sut(self.location)
        self.num = list(sorted(set([j for i in self.location for j in i])))# 记录item
        self.first_support = self.support[:] # 求取confidence

        self.pre_support = [] # 保存前一个support,location,num
        self.pre_location = []
        self.pre_num = []

        self.item_name = [] # 项目名
        self.find_item_name(filename)

    def deal_line(self, line):
        "提取出需要的项"
        return [i.strip() for i in line.split(' ') if i][2:]

    def find_item_name(self, filename):
        "根据第一行抽取item_name"
        with open(filename, 'r') as F:
            for index,line in enumerate(F.readlines()):
                if index == 0:
                    self.item_name = self.deal_line(line)
                    break

    def sut(self, location):
        """
        输入[[1,2,3],[2,3,4],[1,3,5]...]
        输出每个位置集的support [123,435,234...]
        """
        with open('basket.txt', 'r') as F:
            support = [0] * len(location)
            for index,line in enumerate(F.readlines()):
                if index == 0: continue
                # 提取每信息
                item_line = self.deal_line(line)
                for index_num,i in enumerate(location):
                    flag = 0
                    for j in i:
                        if item_line[j] != 'T':
                            flag = 1
                            break
                    if not flag:
                        support[index_num] += 1
        return support

    def select(self, c):
        "返回位置"
        stack = []
        # if self.pre_location:
        #     pre = self.pre_location
        # else:
        #     pre = self.location
        for i in self.location:
            for j in self.num:
                if j in i:
                    if len(i) == c:
                        stack.append(i)
                else:
                    stack.append([j] + i)
        # 多重列表去重
        import itertools
        s = sorted([sorted(i) for i in stack])
        location = list(s for s,_ in itertools.groupby(s))
        return location

    def del_location(self, support, location):
        "清除不满足条件的候选集"
        # 小于最小支持度的剔除
        for index,i in enumerate(support):
            if i < 1000 * self.min_support / 100:
                support[index] = 0
        # apriori第二条规则,剔除
        for index,j in enumerate(location):
            sub_location = [j[:index_loc] + j[index_loc+1:]for index_loc in range(len(j))]
            flag = 0
            for k in sub_location:
                if k not in self.location:
                    flag = 1
                    break
            if flag:
                support[index] = 0
        # 删除没用的位置
        location = [i for i,j in zip(location,support) if j != 0]
        support = [i for i in support if i != 0]
        return support, location

    def loop(self):
        "s级频繁项级的迭代"
        s = 2
        while True:
            print '-'*80
            print 'The' ,s - 1,'loop'
            print 'location' , self.location
            print 'support' , self.support
            print 'num' , self.num
            print '-'*80

            # 生成下一级候选集
            location = self.select(s)
            support = self.sut(location)
            support, location = self.del_location(support, location)
            num = list(sorted(set([j for i in location for j in i])))
            s += 1
            if  location and support and num:
                self.pre_num = self.num
                self.pre_location = self.location
                self.pre_support = self.support

                self.num = num
                self.location = location
                self.support = support
            else:
                break

    def confidence_sup(self):
        "计算confidence"
        if sum(self.pre_support) == 0:
            print 'first min_support error'
        else:
            for index_location,each_location in enumerate(self.location):
                del_num = [each_location[:index] + each_location[index+1:] for index in range(len(each_location))]
                print del_num
                del_num = [i for i in del_num if i in self.pre_location] # 删除不存在上一级频繁项级子集
                del_support = [self.pre_support[self.pre_location.index(i)] for i in del_num if i in self.pre_location]
                print self.support[index_location]
                print del_support
                if not del_num[0]:
                    print 'min_support error'
                    break
                for index,i in enumerate(del_num):
                    index_support = 0
                    if len(self.support) != 1:
                        index_support = index
                    support =  float(self.support[index_location])/10
                    s = [j for index_item,j in enumerate(self.item_name) if index_item in i]
                    if del_support[index]:
                        print ','.join(s) , '->>' , self.item_name[self.num[index]] , ' min_support: ' , str(support) + '%' , ' min_confidence:' , float(self.support[index_location])/del_support[index]

def main():
    c = Apriori('basket.txt')
    c.loop()
    c.confidence_sup()

if __name__ == '__main__':
    main()
############################################################################
