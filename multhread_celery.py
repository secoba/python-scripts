#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:secoba
'''
多线程的停止
celery中任务的停止
    停止子线程时,使用标志位
    停止celery任务时候,使用revoke函数
    但是必须捕获异常设置子线程任务的标志位
'''
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime
import threading

from celery import Celery

app = Celery()
app.conf.update(
    CELERY_IMPORTS=('tasks',),
    BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_REDIS_MAX_CONNECTIONS=5000,
)


# ==========================================
class TEST(threading.Thread):
    '''
    
    '''
    
    def __init__(self, t_name):
        threading.Thread.__init__(self)
        self.t_name = t_name
        self.t_flag = False
    
    def run(self):
        while not self.t_flag:
            time.sleep(2)
            print 'Thread: {0}, time: {1}'.format(self.t_name, datetime.datetime.now())
        
        print '-' * 50
        print 'Thread {0} exiting...'.format(self.t_name)


# ------------------------------------------
@app.task(bind=True)
def check(self, thread_name, thread_num):
    '''
    在celery装饰器中添加了bind=True参数
    这个参数告诉celery发送一个self参数到我的函数
    我能够使用它(self)来记录状态更新
    '''
    threads_pool = []
    
    for tid in range(thread_num):
        test = TEST(thread_name + '_{0}'.format(tid))
        test.setDaemon(True)
        test.start()
        threads_pool.append(test)
    
    # 如果使用celery的revoke
    # 则必须要通过获取异常来进行停止
    while len(threads_pool) > 0:
        try:
            threads_pool = [t.join(99999) for t in threads_pool if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            print "[-] Ctrl-c... Sending kill signal to threads..."
            for t in threads_pool:
                t.t_flag = True
    
    print '-' * 50
    print '[+] Finished...'


if __name__ == '__main__':
    demo = check.delay('demo', 10)
    print demo.id
    print demo.state
    # app.control.revoke(demo.id, terminate=True)
    demo.revoke(terminate=True)
