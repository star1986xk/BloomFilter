import time
import hashlib

class BinarySearch():
    def __init__(self):
        self.container = []  #初始化二分法容器

    def hash(self,url):
        url_hash = hashlib.blake2b(url.encode(), digest_size=8)
        url_hash = url_hash.hexdigest()
        return int(url_hash, 16)

    def exists(self,container, value):
        if len(container) == 0:
            return False
        else:
            midpoint = len(container) // 2
            if container[midpoint] == value:
                return True
            else:
                if value < container[midpoint]:
                    return self.exists(container[:midpoint], value)
                else:
                    return self.exists(container[midpoint + 1:], value)


if __name__ == '__main__':
    start = time.time()

    OBJ = BinarySearch()
    for i in range(0,100000):
        result = OBJ.exists(OBJ.container,i)
        if not result:
            OBJ.container.append(i)
            OBJ.container.sort()

    for i in range(0,100000):
        result = OBJ.exists(OBJ.container,i)
        if not result:
            OBJ.container.append(i)
            OBJ.container.sort()
    print(len(OBJ.container))

    end =  time.time() - start
    print(end)
