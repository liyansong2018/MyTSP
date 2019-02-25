# ！/usr/bin/env python3

# 填充原始表格

array = []
with open("data/sources.txt", "r") as fp, open("data/out.txt", "w") as fo:
    for line in fp:
        array.append(line.split())
    print(array)
    for i in range(len(array)):
        for j in range(i, len(array[i])):
            if array[i][j] == "X":
                sum = 0
                for k in range(j - i):
                    sum = sum + float(array[i + k][i + k + 1])
                array[i][j] = array[j][i] = sum
    print(array)
    for line in array:
        fo.write(",".join(map(str, line)))
        fo.write("\n")