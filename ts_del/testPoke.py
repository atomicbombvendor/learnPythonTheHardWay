# coding=utf-8


# card_sort_num()函数功能：对给出的牌 进行统计并且排序
# 参数：   classList --字符串的形式(支持遍历)
# return:  sortedClassCount--以元组列表的形式输出，如:[(13, 2), (12, 3),..., (8, 3), (7, 3)]
#                                          元组内第一个参数：牌号，第二个参数：对应的牌的数量
def card_sort_num(pokes):  # 返回元素和出现的次数
    poke_type_num = {}  # {'Key': 'V1', 'Key2': 'V2'} 可以用二维数组的方式访问
    # 1.统计列表中元素出现的次数，并存储在字典classCount中
    for vote in pokes:  # 令A、T、J、Q、K编码到对应的字符范围
        if vote == 'A':
            vote = '1'
        if vote == 'T':
            vote = '10'
        if vote == 'J':
            vote = '11'
        if vote == 'Q':
            vote = '12'
        if vote == 'K':
            vote = '13'
        # dict.get(vote,0) 判断字典中是否有vote，如果有vote对应的值 +1 ，否者创建键vote，并令其值为0.
        poke_type_num[int(vote)] = poke_type_num.get(int(vote), 0) + 1  # 使用int()将字符转化为整数

    # 2.根据字典中的key或者value进行排序
    #  e[0]根据key进行排序，e[1]根据value进行排序；默认为升序排序，reverse=Fault
    #  返回为元组列表的形式 [(b, 3), (a, 2), (c, 1)]
    sorted_poke_type_num = sorted(poke_type_num.items(), key=lambda e: e[0], reverse=True)  # 根据key值进行排序（降）
    return sorted_poke_type_num


#  shun_zi() 顺子检查函数
#  参数：a1----待查找的列表元组元素，格式为a1=[('7', 2), ('6', 3), ('5', 2), ('4', 1), ('3', 1)]
#  return----找到符合的顺子返回（顺子个数,去掉符合顺子的牌的元组列表）
def shun_zi(pokes):  # pokes 被查找顺子的对象，
    type_num = len(pokes)  # 给出字典的长度
    shun_zi_num = 0  # 记录顺子个数的数量
    next_index = 0  # 下一索引位置
    shun_zi_start_index = 0  # 一个顺子开始的位置
    A = {}  # 新建一个字典
    B = {}  # 存储了当前牌的所有最长的顺子情况，{[开始位置, 顺子长度], [开始位置, 顺子长度]}

    for i in range(type_num - 1):
        poke_num = pokes[i][0]  # 当前牌的数量
        next_index = i + 1
        next_poke_num = pokes[next_index][0]
        if (int(poke_num) - int(next_poke_num)) == 1:  # 判断前后是否为顺序关系
            shun_zi_num += 1
            if shun_zi_num == 1:  # 记录顺子开始位置索引
                shun_zi_start_index = i
            if shun_zi_num >= 4:
                B[shun_zi_start_index] = B.get(shun_zi_start_index, 0)  # 用来初始化dict, 第二个参数是默认值，当Key不存在的时候
                B[shun_zi_start_index] = shun_zi_num + 1  # 存储B(顺子首索引 : 顺子个数)--字典
        else:
            shun_zi_start_index = 0
            shun_zi_num = 0

    for i in range(type_num):  # 把pokes中的元素复制到字典A中
        A[int(pokes[i][0])] = A.get(int(pokes[i][0]), pokes[i][1])

    for key, value in B.items():  # 对B进行迭代，对A中的顺子进行处理
        for i in range(type_num):
            if i >= key and i <= (key + value - 1):  # 对某区域内的顺子进行处理
                A[int(pokes[i][0])] -= 1  # 顺子的数量 -1
                if A[int(pokes[i][0])] == 0:  # 如果顺子牌号对应的数量为零，将此牌进行删除
                    del A[int(pokes[i][0])]
    sortedClassCount = sorted(A.items(), key=lambda e: e[0], reverse=True)  # 排序，转化为元组的列表方式（根据key进行降序排列）
    B_num = len(B)  # 顺子的个数
    return B_num, sortedClassCount  # 返回：（顺子的个数，减去顺子后的牌组列表）


# pai_duizi()函数--对找完顺子后剩余牌进行规则1,2,3,4处理
# 参数：    yu_pai--找完顺子后的牌的元组列表
# return：  剩余牌按规则出完，需要的最小次数
def pai_duizi(yu_pai):  # 四代二（优先带俩个不同的牌），三代一，一一
    num_1 = 0  # 单牌的个数
    num_2 = 0  # 双牌的个数
    num_3 = 0  # 三张同牌的个数
    num_4 = 0  # 四张同牌的个数

    for i in yu_pai:  # 统计 yu_pai 中的各种牌 组合的数量
        if i[1] == 1:
            num_1 += 1
        if i[1] == 2:
            num_2 += 1
        if i[1] == 3:
            num_3 += 1
        if i[1] == 4:
            num_4 += 1
    #  按 规则 进行出牌的情况，并计算出完需要的最少次数
    if num_1 - num_3 >= 0:
        num_1 = num_1 - num_3
        if num_1 >= num_4 * 2:
            num_1 = num_1 - num_4 * 2
            return num_1 + num_2 + num_3 + num_4
        else:
            num_1 = num_1 - (num_1 // 2) * 2
            num_44 = num_4 - (num_1 // 2)
            if num_2 - num_44 >= 0:
                num_2 = num_2 - num_4
                return num_1 + num_2 + num_3 + num_4
            else:
                return num_1 + num_3 + num_4
    else:
        if num_2 - num_4 >= 0:
            num_2 = num_2 - num_4
            return num_2 + num_3 + num_4
        else:
            return num_3 + num_4


# chu_pai() 函数
# 参数：a1--排序好的牌的牌号和数列的元组列表
# return：返回按规则出完牌，所需的最少次数
def chu_pai(a1):
    p_num, yu_pa = shun_zi(a1)
    if p_num > 0:  # 第1次查找顺子，顺子数量 >0
        p_num1, yu_pa1 = shun_zi(yu_pa)
        if p_num1 > 0:  # 第2次查找顺子，顺子数量 >0
            p_num2, yu_pa2 = shun_zi(yu_pa1)
            if p_num2 > 0:  # 第3次查找顺子，顺子数量 >0
                p_num3, yu_pa3 = shun_zi(yu_pa2)
                if p_num3 > 0:  # 第4次查找顺子，顺子数量 >0
                    p_num4, yu_pa4 = shun_zi(yu_pa3)
                    if p_num4 > 0:  # 第5次查找顺子，顺子数量 >0
                        p_num4, yu_pa4 = shun_zi(yu_pa3)
                    else:  # 第5次查找，没有顺子  ---20张牌，顺子最多具有4对
                        return pai_duizi(yu_pa3) + p_num + p_num1 + p_num2 + p_num3
                else:  # 第4次查找，没有顺子
                    return pai_duizi(yu_pa3) + p_num + p_num1 + p_num2
            else:  # 第3次查找，没有顺子
                return pai_duizi(yu_pa2) + p_num + p_num1
        else:  # 第2次查找，没有顺子
            return pai_duizi(yu_pa1) + p_num
    else:  # 第1次查找，没有顺子
        return pai_duizi(yu_pa)


# 8K67A65K27T59K346AK2
# 789TJQK789TJQK789TJQ
# 12345123451234512345
# 12345678912345678912
# 56789567891234523456

# classList = input()                  #  可以手动输入
classList = '789TJQK789TJQK789TJQ'

a1 = card_sort_num(classList)  # a1 根据key值进行排序（降），a0根据value进行排序（降）
print(a1)
print(chu_pai(a1))  # 输出20张牌需要最少得轮数

'''
输出：
[(13, 2), (12, 3), (11, 3), (10, 3), (9, 3), (8, 3), (7, 3)]
3
'''
