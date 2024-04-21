import requests
from queue import Queue
import sys
import threading
from agent_proxy import user_agent_list
from optparse import OptionParser
# from agent_proxy import ip_proxy

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
                req = requests.get(url=url,headers= user_agent_list.get_user_agent(),timeout=8)
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

    parser = OptionParser()

    parser.add_option("-u","--url",dest="url",help="set target url")
    parser.add_option("-f","--file",dest="ext",help="target url ext")
    parser.add_option("-t","--thread",dest="count",type="int",default=2,help="set scan thread_count")


    (options, args) = parser.parse_args()

    # print(options)

    if options.url and options.ext:
        start(options.url,options.ext,options.count)
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)