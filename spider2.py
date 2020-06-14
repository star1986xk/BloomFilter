import time
import requests
from threading import Thread,Lock,Event
from queue import Queue
from settings import *
from BinarySearch import BinarySearch
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


class spider():
    def __init__(self):
        self.Binary_Search = BinarySearch()  # 实例一个二分法过滤器
        self.Queue = Queue(100000)          # 实例一个队列
        self.thread_count = 10              # 线程数
        self.lock = Lock()                  # 线程锁
        self.event = Event()
    def requstGET(self,url):
        '''
        请求函数
        :param url: url
        :return: text
        '''
        try:
            response = requests.get(url,headers=headers,timeout=3,verify=False)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                return response.text
        except Exception as e:
            return None



    def parser(self,url):
        '''
        解析网页，取得url保存至队列
        :param url:
        :return:
        '''
        url_hash = self.Binary_Search.hash(url)
        self.lock.acquire()                                                          # 线程锁
        if self.Binary_Search.exists(self.Binary_Search.container,url_hash):         # 判断url是否在布隆过滤器中
            self.lock.release()                                                      # 解锁
            return None                                                              # 在过滤器中直接结束函数
        self.Binary_Search.container.append(url_hash)                                # 不在过滤器中，添加到过滤器中
        self.Binary_Search.container.sort()
        self.lock.release()                  # 解锁
        print(url)
        text = self.requstGET(url)           # 请求url
        if text:
            soup = BeautifulSoup(text, 'html.parser')    # 解析url
            for link in soup.find_all('a'):
                self.Queue.put_nowait(link.get('href'))  # 取得新url保存到队列
        self.event.wait()

    def thread_pool(self):
        '''
        线程池,从队列中取出url，循环开启子线程
        :return:
        '''

        while True:
            task_list = []
            for i in range(0,self.thread_count):   # 每次开启 thread_count 个线程
                try:
                    task_list.append(Thread(target=self.parser, args=(self.Queue.get_nowait(),)))  #创建子线程任务
                except Exception as e:
                    print(e)
            for task in task_list:  # 开启线程任务
                time.sleep(0.5)
                task.start()
            # [task.join() for task in task_list]  # 等待这批线程全部结束
            time.sleep(5)
            self.event.set()
            print(self.Queue.qsize())

if __name__ == '__main__':
    url = 'https://www.sohu.com/a/256408522_697896'
    spiderOBJ =spider()
    spiderOBJ.Queue.put(url)
    spiderOBJ.thread_pool()