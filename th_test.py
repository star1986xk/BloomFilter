import timeit
from queue import Queue
from threading import Thread
import time

Q = Queue()

def task1():
    for i in range(10):
        Q.put(1)
def task2():
    for i in range(10):
        Q.get(1)

def thread_pool10():
    task_list = []
    for i in range(0,10):   # 每次开启 thread_count 个线程
        task_list.append(Thread(target=task1))  #创建子线程任务
    [task.start() for task in task_list]
    [task.join() for task in task_list]  # 等待这批线程全部结束
    task_list = []
    for i in range(0,10):   # 每次开启 thread_count 个线程
        task_list.append(Thread(target=task2))  #创建子线程任务
    [task.start() for task in task_list]
    [task.join() for task in task_list]  # 等待这批线程全部结束

def thread_pool100():
    task_list = []
    for i in range(0,100):   # 每次开启 thread_count 个线程
        task_list.append(Thread(target=task1))  #创建子线程任务
    [task.start() for task in task_list]
    [task.join() for task in task_list]  # 等待这批线程全部结束
    task_list = []
    for i in range(0,100):   # 每次开启 thread_count 个线程
        task_list.append(Thread(target=task2))  #创建子线程任务
    [task.start() for task in task_list]
    [task.join() for task in task_list]  # 等待这批线程全部结束



start = time.time()
timeit.timeit(stmt=thread_pool10, number=1)
end = time.time() - start
print(end/10)

start = time.time()
timeit.timeit(stmt=thread_pool100, number=1)
end = time.time() - start
print(end/100)
