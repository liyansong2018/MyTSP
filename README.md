# MyTSP
这是一个遗传算法的完整实现，未经处理的原始数据和已经保存的数据都存放在data目录下
@ 先对文本中的数据进行处理，即初始化种群，再计算每个染色体的适应度和选中概率
@ 对已经选择的亲本染色体，再利用轮盘选择-->>交叉-->>变异-->>子代，即要循环的未经初始化的种群
@ 代码结构更加简单，但是算法复杂度高，实际的运行效率更底
@ version: 0.1
@ author: jing/li
@ data: 2018/08/08