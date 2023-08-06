"""任务结束之后对结果进行后处理
"""

import json
import time
from pathlib import Path

import numpy as np
import requests

from .. import startup

try:
    with open(Path(startup.get('site', ''))/'etc/cloud.json', 'r') as f:
        CLOUD = json.loads(f.read())
except Exception as e:
    print(e)
    CLOUD = {}


def postprocess(result: dict):
    """任务执行完后对数据的操作，如存储到自定义路径或回传到云平台等

    Args:
        result (dict): 任务结果，包含数据段和基本描述信息
    """
    def _delete_dict(ret: dict, num: int = 0):
        while num > 0:
            tmp = np.cumsum(list(ret.values()))
            ran_num = np.random.randint(tmp[-1]+1)
            ran_pos = np.searchsorted(tmp, ran_num)
            ret[list(ret.keys())[ran_pos]] -= 1
            if ret[list(ret.keys())[ran_pos]] == 0:
                ret.pop(list(ret.keys())[ran_pos], 0)
            num -= 1

    # print(result.keys(),result['meta'].keys())

    meta = result['meta']
    print('Send result back  to', meta['user'])
    if not meta['user'].startswith('quafu'):
        return
    
    if not CLOUD:
        return
    
    srv = CLOUD[meta['user']]

    task_id = hex(meta['tid'])[2:].upper()
    task_status = 'failed'
    if meta['status'] in ['Finished','Archived']:
        task_status = 'finished'
        try:
            data: list[dict] = result['data']['count']
        except Exception as e:
            print('Failed to process result',e)
            task_status = 'failed'
    
    if task_status == 'finished':
        dres = {}
        for dat in data:
            for k, v in dat.items():
                dres[k] = dres.get(k, 0)+v

        try:
            shots = meta['other']['shots']*len(meta['axis']['repeat']['repeat'])
            _delete_dict(dres, shots - (shots//1000)*1000)
        except Exception as e:
            print('Failed to dropout', e)

        dic_res = {}
        for k, v in dres.items():
            dic_res[''.join((str(i) for i in k))] = v

        rshot = sum(dic_res.values())

        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": str(dic_res).replace("\'", "\""),
                     "res": str(dic_res).replace("\'", "\""),
                     "server": 2}

    elif task_status == 'failed':
        rshot = 0
        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": "",
                     "res": "",
                     "server": 2}
    # print(post_data)
    try:
        resp = requests.post(url=f"http://{srv['server']}/scq_result/",
                             data=post_data,
                             headers={'api_token': srv['token']})
        print(time.strftime('%Y-%m-%d %H:%M:%S'), resp.text, rshot)
    except:
        print('POST ERROR')
