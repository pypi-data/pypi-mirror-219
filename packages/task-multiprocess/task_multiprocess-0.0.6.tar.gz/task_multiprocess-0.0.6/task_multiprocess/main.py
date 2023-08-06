import os


class TaskMultiprocess:
    cpu_num = os.cpu_count() // 2

    # 配合多进程使用的队列
    def generate_queue(self, queue_list, num=2, desc='generate_queue'):
        # queue_list 将列表形式的数据存放在队列中，返回队列,队列的大小,进程共享的list
        from multiprocessing import Manager
        from tqdm import tqdm
        lock = Manager().Lock()
        q = Manager().Queue()
        for i in tqdm(queue_list, position=0, desc=desc):
            q.put(str(i))
        q_size = q.qsize()
        return q, q_size, lock, [Manager().list() for i in range(num)]

    # 多进程装饰器
    def multiprocess_decorator(func):
        from multiprocessing import Process
        def wrapper(*args, **kwargs):
            process_list = []
            for _ in range(TaskMultiprocess.cpu_num):  # 开启多个子进程执行func函数
                p = Process(target=func, args=(*args,), kwargs=kwargs)  # 实例化进程对象
                p.start()
                process_list.append(p)
            for p in process_list:
                p.join()

        #         return  # 不需要子进程函数执行结果
        return wrapper

    @multiprocess_decorator
    def common_multiprocess(self, fun, q_num, cpu_num=cpu_num, q=None, q_size=0,
                            lock=None, block=True, timeout=2):
        from tqdm import tqdm
        pbar = tqdm(total=q_size, position=0, desc='')
        try:
            while q.qsize():
                lock.acquire()
                # q_element_list = [q.get(block=block, timeout=timeout) for i in range(q_num)]
                q_element_list = [q.get_nowait() for i in range(q_num)]
                lock.release()
                # print(q_element_list)
                fun(q_element_list)
                pbar.update(q_num * cpu_num)
        except Exception as e:
            print(e)
            pass


"""
sample_list = list(range(10))[:]
q, q_size, lock, public_list = generate_queue(sample_list,num=2)
"""
