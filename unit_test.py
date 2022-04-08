# Created : 2022/4/6 14:49
# Author  : Zhu
# Content : Unit_Test

import numpy as np
import random

# 随机缓存替换策略
def Random_Strategy(mecStatus,requestSequences):
    count = 0
    # 按照时隙序列对MEC服务器进行请求访问
    for i in requestSequences:
        if i in mecStatus:
            count += 1
        else:
            del mecStatus[random.choice(mecStatus)]

        print(mecStatus)
    print(count)

if __name__ == '__main__':
    status = [0,1,2,3,4,5,6,7,8,9]
    request = [7,5,11,32,6,0,25,38,19,52]

    random_test = random.choice(request)
    index = request.index(random_test)
    request[index] = 888
    #Random_Strategy(status,request)

