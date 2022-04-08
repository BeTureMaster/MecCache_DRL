# Created : 2022/4/5 20:17
# Author  : Zhu
# Content : SingleAgent_Env

import copy
import numpy as np
from scipy.special import zeta

from baseline import Baseline

'''
Parameter_list:
Cloud Server : 1
MEC_server : 1(SingleAgent)
User_id : [1,20]
MEC_cache_capacity M_max : 8000M bit(160 Cache Units)
Content_size : 50M bit(Fixed value)
Content_id : [1,2,...,500]
Content_population ~ Zipf(a,size)
Time_slot_sequence T : [1,2,...,100](5 minutes)
Req<User_id,Time t> : content_id

Markov_space:
State   :   { Server cache status AND Request sequences at time t }
Action  :   { Hit , Cache_replace top 20% , Cache_replace top 40% , Cache_replace top 60% , Cache_replace top 80% , Cache_replace top 100% }
Reward  :   { +10 , +8 , +6 , +4 , +2 , +1 }
'''

# 内容流行度服从Zipf分布
def zipf(alpha, content_num):
    x = list(range(1, content_num + 1))
    x_array = np.array(x)
    population_trend = (x_array**-alpha)/zeta(alpha)
    count = 0
    for i in range(len(population_trend)):
        count += population_trend[i]
    for i in range(len(population_trend)):
        population_trend[i] /= count
    return population_trend

# 定义云服务器类（编号:默认为0即有且仅有一个，容量极大，内容集合即包含所有的内容）
class CloudServer:
    def __init__(self, id, capacity, contentSet):
        self.id = id
        self.capacity = capacity
        self.contentSet = contentSet

    def get_capacity(self, id):
        if id is self.id:
            return self.capacity

    def get_contentSet(self,id):
        if id is self.id:
            return self.contentSet

# 定义边缘服务器类（边缘服务器编号，每个服务器缓存容量，当前服务器初始存储状态）
class MecServer:
    def __init__(self, id, capacity, ini_status):
        self.id = id
        self.capacity = capacity
        self.ini_status = ini_status

    def get_capacity(self, id):
        if id is self.id:
            return self.capacity

    def get_status(self,id):
        if id is self.id:
            return self.ini_status

class Env:
    def __init__(self):

# 生成时间槽(持续时间，步长)
def generate_time_solt(duration, step):
    TimeSolt_MaxValue = int(duration/step)
    TimeSolt = []
    for i in range(TimeSolt_MaxValue):
        TimeSolt.append(i)
    return TimeSolt

# 生成请求序列并用二维数组存储(用户数量，时间，赋予内容流行度之后的内容集)
def generate_request_sequences(user_id, time_slot, alpha, content_num):
    request_list = [[0 for _ in range(len(time_slot))] for _ in range(len(user_id))]
    # 从Zipf分布中随机抽取100个以内容流行度为基准的内容编号
    probability = []
    for i in zipf(alpha, content_num):
        probability.append(i)

    for i in range(len(user_id)):
        content = np.random.choice(len(probability), len(time_slot), replace=False, p=probability)
        for j in range(len(time_slot)):
            request_list[i][j] = content[j]
    return request_list

# 生成MEC服务器中初始随机缓存状态（内容数量，MEC服务器容量[单位为M bit]，一个内容的大小[单位为M bit]）
def ini_status(content_num, MEC_Capacity, content_size):
    cache_capacity = int(MEC_Capacity/content_size)
    status = np.random.choice(content_num, cache_capacity, replace=False, p=None)
    return status

# test
if __name__ == '__main__':
    user = range(20)
    time_slot = generate_time_solt(300,3)
    request_sequences = copy.deepcopy(generate_request_sequences(user, time_slot, 0.56, 500))
    request_user0 = request_sequences[0]
    status = copy.deepcopy(ini_status(500,8000,50))
    status = list(status)

    baseline = Baseline(status,request_sequences)
    baseline.none_strategy()
    baseline.random_strategy()
    baseline.fifo_strategy()
    baseline.lru_strategy()