# ！/usr/bin/env python3
import numpy
import random

'''
@ 先对文本中的数据进行处理，即初始化种群，再计算每个染色体的适应度和选中概率
@ 对已经选择的亲本染色体，再利用轮盘选择-->>交叉-->>变异-->>子代，即要循环的未经初始化的种群
@ 代码结构更加简单，但是算法复杂度高，实际的运行效率更底
@ version: 0.1
@ author: jing
@ data: 2018/08/08
'''

# 下标+元素排序
def index_sort(arr):
    arr_index = [i for i in range(len(arr))]
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] < arr[j]:
                arr_index[i], arr_index[j] = arr_index[j], arr_index[i]
                arr[i], arr[j] = arr[j], arr[i]
    return [arr_index] + [arr]  # 返回的数组0代表下标排序，数组1代表元素大小排序

# 种群初始化
def effect_oder(arr, cnt, num):
    population = []  # 种群重置
    for k in range(num):
        if cnt == 0:
            List = [i for i in range(1, 28)]
            random.shuffle(List)  # 随机生成工艺序列
        else:
            List = arr[k]   # List代表一条染色体
        sum = 0
        original_step = List[0]  # array 的下标
        original_index = 0  # List 的下标  只是为了存放结果
        result = []
        # 在每条染色体里找到一组解
        for i in range(len(List)):
            if i < len(List) - 1:
                now_step = List[i]  # array 的下标if i < len(List) - 1:
                next_step = List[i + 1]
                sum = sum + float(array[now_step][next_step])
                if sum + float(array[next_step][original_step]) > 129 and i != 0:
                    result.append([List[j] for j in range(original_index, i + 1)])
                    original_step = next_step
                    original_index = i + 1
                    sum = 0
            else:
                result.append([List[j] for j in range(original_index, len(List))])
        population.append(result)
    return population


# 计算适应度
def fitness_test(arr):
    result = []
    for i in arr:
        #result.append(round(1 / len(i), 17))
        result.append(1 / len(i))
    return result


# 计算概率
def probability(arr):
    result = []
    sum_1 = 0
    for i in arr:
        sum_1 = sum_1 + i
    for i in arr:
        #result.append(round(i / sum_1, 17))
        result.append(i / sum_1)
    return result


def selection(population, probabi_value):
    # 轮盘赌选择
    probabi_sum = []
    for i in range(len(probabi_value)):
        if i == 0:
            probabi_sum.append(probabi_value[i])
        else:
            probabi_sum.append(probabi_sum[i - 1] + probabi_value[i])

    # 选择新的序列
    result = []
    for i in range(len(probabi_value)):
        rand = numpy.random.uniform(0, 1)
        for j in range(len(probabi_value)):
            if j == 0:
                if 0 <= rand and rand <= probabi_sum[j]:
                    result.append(population[j])
            else:
                if probabi_sum[j - 1] < rand and rand <= probabi_sum[j]:
                    result.append(population[j])
    return result


# 三维数组转二维
def change_list_three_to_two(arr, num):
    result = []
    element = [c for a in arr for b in a for c in b]
    for i in range(len(arr)):
        result.append(element[0 + i * num:num + i * num])
    return result


# 两组数交叉
def cross(parent1, parent2, geneLength, pm_c):
    if numpy.random.uniform(0, 1) <= pm_c:
        index1 = random.randint(0, geneLength - 1)
        index2 = random.randint(index1, geneLength - 1)

        def one_result(arr1, arr2):
            child = [i for i in arr2 if i not in arr1[index1:index2]]
            left = child[:index1]
            right = child[index1:]
            child = left + arr1[index1:index2] + right
            return child

        return [one_result(parent1, parent2)] + [one_result(parent2, parent1)]
    else:
        return [parent1] + [parent2]


# 对所有序列进行交叉
def cross_over(arr, pm):
    result = []  # 存放交叉后的结果
    for i in range((len(arr) // 2)):
        temp = cross(arr[i * 2], arr[i * 2 + 1], 27, pm)
        result.append(temp[0])
        result.append(temp[1])
    return result


# 变异
def mutation(newGene, pm):
    """突变"""
    for i in range(len(newGene)):
        if numpy.random.uniform(0, 1) <= pm:
            # 相当于取得0到self.geneLength - 1之间的一个数，包括0和self.geneLength - 1
            index1 = random.randint(0, len(newGene[i]) - 1)
            index2 = random.randint(0, len(newGene[i]) - 1)
            # 把这两个位置互换
            newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        return newGene


if __name__ == '__main__':

    array = []  # 工艺数据
    max_ovrall_fitness = 0  # 最大适应度
    final_population = []  # 最终种群
    mutat_result = []  # 每次迭代生成的子群
    count = max_fitness = 0
    number = 200  # 种群数量
    fitness_last = [0] * number     # 上个种群中每个染色体的适应度
    population_last = [0] * number  # 上个种群

    with open("data/new_out.csv", "r") as fp:
        for line in fp:
            array.append(line.split()[0].split(","))

    #while max_fitness <= 0.1:  # 寻找最大适应度
    while count < 200:
        population = effect_oder(mutat_result, count, number)

        fitness_list = fitness_test(population)  # 适应度

        # 保证收敛性，即将本次种群与上次种群做比较，选择适应度较高的染色体集合
        fitness_sum = fitness_list + fitness_last
        population_sum = population + population_last
        sort_result = index_sort(fitness_sum)   # 对fitness从大到小排序，同时元素也进行排序
        new_population = []     # 重置种群
        for i in range(number):
            new_population.append(population_sum[sort_result[0][i]])
        population = new_population            # 重置种群
        fitness_list = sort_result[1][:number]   # 重置适应度

        max_fitness = fitness_list[0]

        probability_value = probability(fitness_list)
        # print("概率：", probability_value)

        select_result = selection(population, probability_value)
        # print("选择的结果：", select_result)

        new_result = change_list_three_to_two(select_result, num = len(array[0]) - 1)  # 删去中括号的二维数组
        # print("选择优化：", new_result)

        cross_result = cross_over(new_result, pm=0.75)
        # print("交叉：", cross_result)

        mutat_result = mutation(cross_result, pm=0.02)
        # print("变异：", mutat_value)

        count = count + 1
        population_last = population
        fitness_last = fitness_list

    print("最大适应度：{}".format(max_fitness), "循环次数：{}".format(count), "工艺序列：{}".format(population_last[0]), "人数：{}".format(int(1 / max_fitness)), sep='\n-----------------\n')