import requests
import argparse
from queue import Queue
import sys
import threading
from agent_proxy import user_agent_list
from agent_proxy import ip_proxy
import re

class DirScan(threading.Thread):

    def __init__(self,queue,isRandomProxy,proxy):
        threading.Thread.__init__(self)
        self._queue = queue
        self.isRandomProxy = isRandomProxy
        self.proxy = proxy

    def run(self):

        while not self._queue.empty():
            url = self._queue.get()
            # print(url)
            # print(user_agent_list.get_user_agent())

            try:
                if self.isRandomProxy and self.proxy==0 :
                    req = requests.get(url=url,headers= user_agent_list.get_user_agent(),timeout=8,proxies=ip_proxy.get_ip_proxy())
                elif self.proxy :
                    req = requests.get(url=url,headers= user_agent_list.get_user_agent(),timeout=8,proxies=self.proxy)
                else:
                    req = requests.get(url=url, headers=user_agent_list.get_user_agent(), timeout=8)
                # print(url)

                if req.status_code == 200:
                    print(f"[*] {url}")
            except Exception as e :
                print(e)
                pass
    

# ext 字典名称
def start(url, ext, count,isRandomProxy,proxy):
    queue = Queue()


    f = open("./ dicts/%s.txt"%ext,'r')

    for i in f:
        queue.put(url+i.rstrip('\n'))
        # print(url+i.rstrip('\n'))

    threads = []
    thread_count = int(count)

    for i in range(thread_count):
        threads.append(DirScan(queue,isRandomProxy,proxy))

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

    
#format : http://192.168.1.1:8080
def proxy_handle(proxy):
    pattern = r'(http?|https)://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})'
    match = re.match(pattern,proxy)

    if match:
        protocol = match.group(1)
        ip = match.group(2)
        port = match.group(3)

        return f'{{"{protocol}": "{protocol}://{ip}:{port}"}}'

    else:
        return "Invalid proxy format."




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
    parser.add_argument("-random_proxy",dest="isRandomProxy",type=bool,default=0,help="use random proxy, use for True, not for False",required=False)
    parser.add_argument("-proxy",dest="proxy",default=0,help="set your own proxy, format is http://192.168.1.1:8080",required=False)

    args = parser.parse_args()

    if args.url and args.ext:
        proxy = args.proxy
        handle_proxy = 0
        if proxy != 0:
            handle_proxy = proxy_handle(proxy)
            if handle_proxy == "Invalid proxy format.":
                print("Invalid proxy format.")
                exit(0)

        start(args.url,args.ext,args.count,args.isRandomProxy,handle_proxy)
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)