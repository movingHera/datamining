#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
min_support = 20
min_confidence = 20
num = [1] * 11
support = []
with open('basket.txt', 'r') as F:
    for index,line in enumerate(F.readlines()):
        if index == 0:
            things = [i.strip() for i in line.split(' ')[2:] if i]
            things = [1] * len(things)
            support = [0] * len(things)
            continue
        things_line = [i.strip() for i in line.split(' ') if i][2:]
        for index_line,i in enumerate(things_line):
            if i == 'T':
                support[index_line] += 1
    print support

# 第一次筛选
for index_next,i in enumerate(support):
    if i < index * min_support / 100:
        support[index_next] = 0
        things[index_next]  = 0

print support
print things

tmp = [index for index,i in enumerate(things) if i == 1]
print tmp
tmp1 = [[i] for i in tmp]
print tmp1
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
    return stack

num = select(tmp1,tmp,2)
tmp = [0] * len(select(tmp1,tmp,2))
# 第二次筛选
with open('basket.txt', 'r') as F:
    for index,line in enumerate(F.readlines()):
        if index ==0:
            continue
        line = [i.strip() for i in line.split(' ') if i][2:]
        for index_num,i in enumerate(num):
            for j in range(len(i)):
                if line[i[j]] != 'T':
                    break
            if j == len(i) - 1:
                tmp[index_num] += 1

print tmp

# for i in data:
#     with open('basket.txt', 'r') as F:
#         for line in F.readlines():






############################################################################
