from multiprocessing import Pool
import os,time,random

def worker(msg,idx):
    t_start = time.time()
    print("%s开始执行,进程号为%d"%(msg,os.getpid()))
    #random.random()随机生成0~1之间的浮点数
    time.sleep(random.random()*2) 
    t_stop = time.time()
    print(msg,"%d 执行完毕，耗时%0.2f"%(idx,t_stop-t_start))
    return idx

result = []
po=Pool(10) #定义一个进程池，最大进程数3
for i in range(0,10):
    result.append(po.apply_async(worker,args = (i,i)))  #如果不用async 直接使用apply, 那么会使用堵塞式,任务一个一个执行

print("----start----")
po.close() #关闭进程池，关闭后po不再接收新的请求
po.join() #等待po中所有子进程执行完成，必须放在close语句之后
print("-----end-----")
output = []
for res in result:
    output.append(res.get())


