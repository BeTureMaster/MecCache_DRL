import numpy as np
from itertools import product

def Zipf(a, max1, size=None):
    """
    截断法生成zipf分布的数列
    """
    if min == 0:
        raise ZeroDivisionError("")
    content = []
    x = list(range(1, max1 + 1))
    v = np.array(x)
    p = 1.0 / np.power(v, a)
    p /= np.sum(p)  # normalized
    for i in range(0, max1):
        content.append(Content(i + 1, p[i]))
    c = np.random.choice(v, size=size, replace=True, p=p)
    return c, content


class Content:
    def __init__(self, id, population):
        self.id = id
        self.size = np.random.uniform(5, 15)
        self.population = population

    def get_population(self, id):
        if id is self.id:
            return self.population

    def get_size(self, id):
        if id is self.id:
            return self.size


class Env:
    def __init__(self, C_size, cache_id, BS_size, F_size, RQ):
        self.BS_id = cache_id  # 当前BS的编号
        self.C_size = C_size  # 缓存容量
        self.BS_size = BS_size  # 基站的数量
        self.F_size = F_size  # 内容的数量
        cache_state, other_cache_state = self.get_all_cache_state()  # 缓存状态
        self.cache_state, self.other_cache_state = cache_state, other_cache_state
        self.action = [0, 0]  # 系统动作 代表缓存由谁处理,以及缓存策略
        self.state = np.array([0 for x in range(C_size + 1)])  # 系统状态
        self.reward = 0.0  # 系统奖励
        self.RQ_size = RQ
        self.request, self.content = Zipf(1.2, self.F_size, self.RQ_size)
        a = list(product(list(range(0, self.BS_size + 1)), list(range(1, self.F_size + 1))))
        self.action_space = a

    def get_all_cache_state(self):  # 得到缓存状态

        all = [[0, 0, 0, 0, 0, 0, 0, 0]]
        state = []
        for i in range(1, self.BS_size + 1):
            s = self.get_cache_state(i)
            #print("get_all_cache_state", s)
            all.append(s)
            if i == self.BS_id:
                state = s
        return state, all

    def get_cache_state(self, id):  # 根据BS的id得到缓存状态
        if id in range(1, self.BS_size + 1):
            x = list(range(1, self.F_size + 1))
            v = np.array(x)
           # print("C_size",self.C_size)
            return np.random.choice(v, size=self.C_size, replace=False)

    def search_help(self, content_id):  # 判断内容在哪里有
        all = []  # 接受所有id
        #print("content_id", content_id)
        # print("other_state",self.other_cache_state)
        for index, id in enumerate(self.other_cache_state):
            if content_id in id:
                # print("sother", id)
                # print("index", index)
                # print("id",id)
                all.append(index)
        if len(all) == 0:
            return [-1]
        return all

    def get_available_action(self, state):  # state是状态
        action = []
       # print("get_available_action_state", state)
       # print(state[self.C_size-1])
        id = self.search_help(state[self.C_size])
       # print("get_rq",state[self.C_size])
        # print("qwqwe>>>>>>>>>>>>>>>>>>>>>>",self.other_cache_state)

        # print("action_space", env.action_space.__len__())
        # print("id", id)
        if id != [-1]:
            for id in id:#缓存有请求内容的基站包括本地的动作
                for i in range(self.C_size - 1):
                    action.append(self.action_space[id*self.F_size + state[i] - 1])
                #
                    # print("self.action_space[id * self.F_size]",self.action_space[id * self.F_size+state[self.C_size] - 1])
                    # action.append(self.action_space[id * self.F_size])
        # print("gaction",action)
        for i in range(self.C_size - 1): #请求云端缓存到本地的动作
            action.append(self.action_space[state[i] - 1])
        # print("ALL_action", action)
        # print(state)
        # print(action)
        return action

    def get_available_action1(self, state):  # state是状态
        action = []
        # print("get_available_action_state", state)
        # print(state[self.C_size-1])
        id = self.search_help(state[self.C_size])
        # print("get_rq",state[self.C_size])
        # print("qwqwe>>>>>>>>>>>>>>>>>>>>>>",self.other_cache_state)

        # print("action_space", env.action_space.__len__())
        # print("id", id)
        if id != [-1]:
            for id in id:  # 缓存有请求内容的基站包括本地的动作
                for i in range(self.C_size - 1):
                    action.append(id * self.F_size + state[i] - 1)
                #
                # print("self.action_space[id * self.F_size]",self.action_space[id * self.F_size+state[self.C_size] - 1])
                # action.append(self.action_space[id * self.F_size])
        # print("gaction",action)
        for i in range(self.C_size - 1):  # 请求云端缓存到本地的动作
            action.append(state[i] - 1)
        # print("ALL_action", action)
        # print(state)
        # print(action)
        return action
    def step(self, a, i):
        if i >= self.RQ_size - 1:
            done = True
            return 0, 0, done
        else:
            done = False
            rq = self.request[i]
            #print("Srq",rq)
            self.state = np.hstack((self.cache_state, rq))
            # print("s", self.state)
            if a[0] is self.BS_id:

                if a[1] not in self.cache_state or (rq in self.cache_state and a[1] != rq):
                    reward = -10000
                else:
                    # print("s", self.state)
                    # print("action", a)
                    reward = 90 * self.content[rq - 1].population  # 代表本地处理的延迟
                    self.cache_state[np.where(self.cache_state == a[1])] = rq
                    # print("r", reward)
                    self.state = np.hstack((self.cache_state, self.request[i+1]))
                    # print("s_", self.state)

            elif a[0] == 0:
                self.cache_state[np.where(self.cache_state == a[1])] = rq
                self.state = np.hstack((self.cache_state, self.request[i+1]))

                reward = 0.09 * self.content[rq-1].population  # 代表BS协作的延迟
            else:
                if a[0] not in self.search_help(rq):
                    #print("Steprq", rq)
                    # print("search_help", self.search_help(rq))
                    # print("oter>>>>>>>>>>>>>>>>>>>>>>>>>",self.other_cache_state)
                    # for i in self.search_help(rq):
                    #      print(i, self.other_cache_state[i])
                    reward = -10000
                else:
                    self.cache_state[np.where(self.cache_state == a[1])] = rq
                    self.state = np.hstack((self.cache_state, self.request[i+1]))
                    reward = 9 * self.content[rq - 1].population  # 代表从云端的延迟
            if reward == -10000 and a[0] is not self.BS_id:
                # print("other", self.other_cache_state[a[0]])
                # print("esaction", a)
                print("reward", reward)
            return self.state, reward, done

    def print(self):
        print("测试")
        for i in range(0, 20):
            print(i, self.content[i].id, self.request[i])

enva = Env(8, 1, 2, 20, 100)
enva.print()