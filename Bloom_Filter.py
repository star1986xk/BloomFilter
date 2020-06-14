# coding=utf-8
import time

import BitVector
import random
import hashlib
import math


# 随机生成哈希函数类
class SimpleHash():
    def __init__(self, bloom_filter_size,seed):
        '''
        初始化
        :param bloom_filter_size: 布隆过滤器长度
        :param seed:种子
        '''
        self.bloom_filter_size = bloom_filter_size
        self.seed = seed

    def hash(self, string):
        '''
        哈希函数
        :param string:待哈希字符串
        :return:返回布隆过滤器的索引位
        '''
        as_bytes = string.encode()
        blake_hash = hashlib.blake2b(as_bytes, digest_size=8, salt= self.seed.to_bytes(length=2, byteorder='big', signed=True))
        blake_hash = blake_hash.hexdigest()
        return int(blake_hash, 16) % self.bloom_filter_size

class Bloom_Filter():

    def __init__(self, n=100000,p = 0.001):
        '''

        :param n:预计存10W条
        :param p:设计误报率
        '''
        self.bloom_filter_size = int((-1) * n * math.log(p) / (math.log(2) * math.log(2)))  # 计算布隆过滤器长度

        self.hash_count = int(math.log(2) * (self.bloom_filter_size) / (n))  # 计算哈希函数个数

        self.container = BitVector.BitVector(size=int(self.bloom_filter_size))  # 初始化布隆过滤器

        self.hash_seeds = self.get_seed_list(self.hash_count)  # 生成随机种子

        self.hash = []
        for i in range(int(self.hash_count)):  # 生成哈希函数
            self.hash.append(SimpleHash(self.bloom_filter_size, self.hash_seeds[i]))


    def get_seed_list(self,hash_count):
        '''
        生成种子
        :param bloom_filter_size: 布隆过滤器长度
        :param hash_count: 哈希函数个数
        :return: 返回种子列表(数量等于哈希函数个数)
        '''
        seed_list = random.sample(range(0, 100), hash_count)
        return seed_list

    def exists(self, value):
        '''存在返回真，否则返回假'''
        if value == None:
            return False
        for func in self.hash:
            if self.container[func.hash(str(value))] == 0:
                return False
        return True

    def mark_value(self, value):
        '''存入元素'''
        for func in self.hash:
            self.container[func.hash(str(value))] = 1


if __name__ == '__main__':
    start = time.time()

    count = 0
    bf = Bloom_Filter()
    for i in range(100000):
        bf.mark_value(i)

    for i in range(100000,200000):
        if bf.exists(i):
            count +=1

    print(count)

    end =  time.time() - start
    print(end)
