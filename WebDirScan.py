import requests
import argparse
from queue import Queue
import sys
import threading
from agent_proxy import user_agent_list
from agent_proxy import ip_proxy

class DirScan(threading.Thread):

    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
    

    def run(self):

        while not self._queue.empty():
            url = self._queue.get()
            # print(url)
            # print(user_agent_list.get_user_agent())

            try:
                req = requests.get(url=url,headers= user_agent_list.get_user_agent(),timeout=8,proxies=ip_proxy.get_ip_proxy())
                # print(url)

                if req.status_code == 200:
                    print(f"[*] {url}")
            except Exception as e :
                print(e)
                pass
    

# ext 字典名称
def start(url, ext, count):
    queue = Queue()


    f = open("./ dicts/%s.txt"%ext,'r')

    for i in f:
        queue.put(url+i.rstrip('\n'))
        # print(url+i.rstrip('\n'))

    threads = []
    thread_count = int(count)

    for i in range(thread_count):
        threads.append(DirScan(queue))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    f.close()
    

# if __name__ == '__main__':
#     if len(sys.argv) !=4:
#         print('arg err')
#         sys.exit(-1)
#     else:
#         # print(sys.argv[1], sys.argv[2], sys.argv[3])
#         start(sys.argv[1],sys.argv[2],sys.argv[3])



if __name__ == "__main__":
    print("""
__        __   _     ____  _      ____                  
\ \      / /__| |__ |  _ \(_)_ __/ ___|  ___ __ _ _ __  
 \ \ /\ / / _ \ '_ \| | | | | '__\___ \ / __/ _` | '_ \ 
  \ V  V /  __/ |_) | |_| | | |   ___) | (_| (_| | | | |
   \_/\_/ \___|_.__/|____/|_|_|  |____/ \___\__,_|_| |_|
""")


    parser = argparse.ArgumentParser(description="Web Directory Scanner")

    parser.add_argument("-u", "--url", dest="url", help="set target url", required=True)
    parser.add_argument("-f", "--file", dest="ext", help="target url ext", required=True)
    parser.add_argument("-t", "--thread", dest="count", type=int, default=2, help="set scan thread count")


    args = parser.parse_args()

    if args.url and args.ext:
        start(args.url,args.ext,args.count)
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)