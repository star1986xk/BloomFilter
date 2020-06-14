import timeit
from Bloom_Filter import Bloom_Filter


'''
测试存1000条、10000条、1000000条、过滤器的存储速度
'''
def test_1000():
    count = 0
    BF = Bloom_Filter(1000)
    for i in range(1000):
        BF.mark_value(i)
    for i in range(1000,2000):
        if BF.exists(i):
            count +=1
    print(count)

def test_10000():
    count = 0
    BF = Bloom_Filter(1000)
    for i in range(1000):
        BF.mark_value(i)
    for i in range(1000,2000):
        if BF.exists(i):
            count +=1
    print(count)

def test_1000000():
    count = 0
    BF = Bloom_Filter(100000)
    for i in range(1000):
        BF.mark_value(i)
    for i in range(1000,2000):
        if BF.exists(i):
            count +=1
    print(count)

print(timeit.timeit(stmt=test_1000, number=5))
print(timeit.timeit(stmt=test_10000, number=5))
print(timeit.timeit(stmt=test_1000000, number=5))