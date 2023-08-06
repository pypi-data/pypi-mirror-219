import owncloud

import pkg_resources
from threading import Thread
import datetime

def run():
    oc = owncloud.Client("http://192.168.10.13")
    oc.login("test_dep1", "oa123456!")
    print(f"{datetime.datetime.now()} Success")

if __name__ == '__main__':
    print(pkg_resources.get_distribution('gtocclient').version)
    threads = []
    while True:
        for i in range(100):
            thread = Thread(target=run)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        
    # oc.put_directory("/gean/", "/Users/yebk/git/gtocclient/dist", chunked=True)