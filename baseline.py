# Created : 2022/4/7 20:46
# Author  : Zhu
# Content : Baseline

import numpy as np
import random
import queue

# 定义Baseline类，共四种基准线模式
class Baseline:
    def __init__(self, mecStatus, requestSequences):
        self.id = id
        self.mecStatus = mecStatus
        self.requestSequences = requestSequences

    # 无缓存替换策略
    def none_strategy(self):
        request = np.array(self.requestSequences)
        request_num = np.shape(request)[0] * np.shape(request)[1]
        count = 0
        # 按照时隙序列对MEC服务器进行请求访问
        for i in range(np.shape(request)[1]):
            for j in request[:, i]:
                if j in self.mecStatus:
                    count += 1
            # 模拟每次时隙序列休眠
            # time.sleep(0.003)
        print('No Cache Replacement Policy Hit Ratio:', '{:.2f}%'.format((count / request_num) * 100))

    # 随机缓存替换策略
    def random_strategy(self):
        request = np.array(self.requestSequences)
        request_num = np.shape(request)[0] * np.shape(request)[1]
        count = 0
        # 按照时隙序列对MEC服务器进行请求访问
        for i in range(np.shape(request)[1]):
            for j in request[:, i]:
                if j in self.mecStatus:
                    count += 1
                else:
                    random_choice = random.choice(self.mecStatus)
                    index = self.mecStatus.index(random_choice)
                    self.mecStatus[index] = j
        print('Random Cache Replacement Policy Hit Ratio:', '{:.2f}%'.format((count / request_num) * 100))

    # 先进先出缓存替换策略
    def fifo_strategy(self):
        request = np.array(self.requestSequences)  # 将request进行numpy格式处理，便于后续操作
        request_num = np.shape(request)[0] * np.shape(request)[1]  # 求得所有的请求次数
        count = 0  # 计数器 用于计算命中次数
        status_queue = queue.Queue()  # FIFO策略所需的队列定义
        '''将mec服务器中的缓存状态依次放入队列中'''
        for i in self.mecStatus:
            status_queue.put(i)
        '''按照时隙序列对MEC服务器进行请求访问'''
        for i in range(np.shape(request)[1]):
            for j in request[:, i]:
                if j in list(status_queue.queue):
                    count += 1
                else:
                    status_queue.get()
                    status_queue.put(j)
        print('FIFO Cache Replacement Policy Hit Ratio:', '{:.2f}%'.format((count / request_num) * 100))

    # 最近最少使用缓存替换策略
    def lru_strategy(self):
        request = np.array(self.requestSequences)  # 将request进行numpy格式处理，便于后续操作
        request_num = np.shape(request)[0] * np.shape(request)[1]  # 求得所有的请求次数
        count = 0  # 计数器 用于计算命中次数
        '''按照时隙序列对MEC服务器进行请求访问'''
        for i in range(np.shape(request)[1]):
            for j in request[:, i]:
                if j in self.mecStatus:
                    count += 1
                    index = self.mecStatus.index(j)
                    del self.mecStatus[index]
                    self.mecStatus.insert(0, j)
                else:
                    self.mecStatus.pop()
                    self.mecStatus.insert(0, j)
        print('LRU Cache Replacement Policy Hit Ratio:', '{:.2f}%'.format((count / request_num) * 100))