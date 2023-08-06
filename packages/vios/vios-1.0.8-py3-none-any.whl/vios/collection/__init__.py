"""本模块主要由工具函数构成, 且依赖server
>>> tasks：实验描述
>>> support：兼容层，如与Scanner格式转换
>>> uapi：与前端进行交互，如matplotlib画图、数据库查询、实时画图等，详见各函数说明。
"""
import asyncio
import json
import os
import time
from collections import OrderedDict
from functools import cached_property
from pathlib import Path

from kernel.sched import JupyterProgressBar, Progress
from kernel.sched.task import App
from quark import connect
from waveforms.scan_iter import scan_iters

from .. import startup

try:
    with open(Path(startup.get('site', '')) /'etc/bootstrap.json', 'r') as f:
        cfg = json.loads(f.read())['executor']
except Exception as e:
    print(e)
    cfg = {"host": "127.0.0.1", "port": 2088}

print(cfg)
s = connect('QuarkServer', host=cfg.get('host', '0.0.0.0'), port=cfg.get('port',2088))
vdict = OrderedDict()
LASTID = {'tid': 0, 'index': 0}


class Task(object):
    """适用于大量任务连续提交（如量子云），获取任务状态、结果、进度等。
    Args:
        task (dict): 任务描述
        timeout (float | None, optional):任务最大时长，默认为None，即任务执行完毕结束.

    任务样例见本模块下experiment。使用方法：
    >>> task = Task(s21) # s21 为experiment中字典描述
    >>> task.run()
    >>> task.bar() # 适用于notebook
    """

    handles = {}

    def __init__(self, task: dict | App, timeout: float | None = None) -> None:
        """_summary_

        Args:
            task (dict): _description_
            timeout (float | None, optional): _description_. Defaults to None.
        """
        if isinstance(task, App):
            task = transform(task)
        self.task = task
        self.timeout = timeout

        self.data = {}
        self.meta = {}
        self.index = 0
        self.cmds = {}

        self.progress = Progress()

    @cached_property
    def name(self):
        return self.task['metainfo'].get('name', 'Unknown')

    def run(self):
        self.stime = time.time() # start time
        self.taskid = s.submit(self.task)

    def cancel(self):
        s.cancel(self.taskid)
        self.stop(self.taskid, False)

    def result(self):
        meta = True if not self.meta else False
        res = s.fetch(self.taskid, start=self.index, meta=meta)

        if isinstance(res, str):
            return self.data
        elif isinstance(res, tuple):
            if isinstance(res[0], str):
                return self.data
            data, self.meta = res
        else:
            data = res
        self.index += len(data)
        self.process(data)

        return self.data

    def status(self):
        return s.track(self.taskid)

    def error(self):
        return s.report(self.taskid)

    def step(self, index: int):
        if index not in self.cmds:
            self.cmds[index] = s.review(self.taskid, index)
        return self.cmds[index]

    def process(self, data: list[dict]):
        for dat in data:
            for k, v in dat.items():
                if k in self.data:
                    self.data[k].append(v)
                else:
                    self.data[k] = [v]

    def join(self):
        try:
            self.result()
        except Exception as e:
            print(e)

        try:
            status = self.status()
            self.progress.max = status['size']
        except Exception as e:
            print(e,status)
            self.join()

        if status['status'] in ['Pending']:
            time.sleep(0.5)
            self.join()
        elif status['status'] in ['Failed', 'Canceled']:
            return self.stop(self.taskid, False)
        elif status['status'] in ['Running']:
            self.progress.goto(self.index)
        elif status['status'] in ['Finished', 'Archived']:
            self.progress.goto(self.progress.max)

        # if self.index and self.index == self.progress.max:
            return self.stop(self.taskid)
        
        if isinstance(self.timeout, float):
            if self.timeout > 0 and (time.time() - self.stime > self.timeout):
                msg = f'Timeout: {self.timeout}'
                print(msg)
                raise TimeoutError(msg)
            time.sleep(2)
            self.join()
        else:
            self.handles[self.taskid] = asyncio.get_running_loop().call_later(2, self.join)

    def clear(self):
        for tid, handle in self.handles.items():
            self.stop(tid)

    def stop(self, tid: int, success: bool = True):
        try:
            self.progress.finish(success)
            self.handles[tid].cancel()
        except Exception as e:
            # print(e)
            pass

    def bar(self):
        # self.stop(self.taskid)
        bar = JupyterProgressBar(description=self.name)
        bar.listen(self.progress)
        bar.display()
        self.join()


def transform(app: App):
    """转换继承自App的任务为server可执行任务

    Args:
        app (App): 任务基类

    Returns:
        dict: 任务描述
    """

    steps = list(scan_iters(**app.scan_range()))

    circ = []
    loop = {}
    for step in steps:
        circ.append(step.kwds['circuit'])
        for q in app.qubits:
            loop.setdefault(q, []).append(step.kwds[q])

    index = []
    for k, v in loop.items():
        index.append((k, v, 'au'))

    trigger = s.query('station.triggercmds')[0]

    return dict(metainfo={'name': f'filename:/{app.name}', 'priority': app.task_priority, 'user': 'kernel',
                          'other': {'shots': app.shots, 'signal': app.signal}},

                taskinfo={'STEP': {'main': ['WRITE', ('index',)],
                                   'trigger': ['WRITE', 'trig'],
                                   'READ': ['READ', 'read'],
                                   },
                          'CIRQ': iter(circ),
                          'LOOP': {'index': index,
                                   'trig': [(trigger, 0, 'any')]
                                   }
                          })
