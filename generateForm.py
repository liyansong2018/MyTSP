# ！/usr/bin/env python3

# 计算表格中的数据，生成最终的序列

arr = []
add = [20.4, 27.34, 20.46, 8.4, 22.02, 46, 22.46, 18.16, 18.86, 46, 32.18, 44, 47.08, 43.48, 12.96, 17.94, 26.32, 39.68, 12.98, 16.2, 20.18, 20.18, 34.5, 35.82, 38.25, 41.6, 41.08]
with open("data/out.txt", "r") as fp, open("data/new_out.csv", "w") as fout:
    for line in fp:
        arr.append(line.split()[0].split(','))
    print(arr)
    for i in range(1, len(arr)):
        for j in range(1, len(arr[i])):
            arr[i][j] = float(arr[i][j]) + add[i - 1]

    for line in arr:
        fout.write(",".join(map(str, line)))
        fout.write("\n")