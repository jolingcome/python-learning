#删除大精灵上的任务

import requests,json
from typing import  List

#获取批量task_id
genie_url='http://staging.argus.sensetime.com'
registry_id='argusstaging'
device_id='20b1b4b7b7d1a5867b624fb9230c697e17cbe3272ab3d5a5ccecd2f87024365e'


#查询所有任务
#http://staging.argus.sensetime.com/genie-cloud/api/v1/tasks/config/state/20b1b4b7b7d1a5867b624fb9230c697e17cbe3272ab3d5a5ccecd2f87024365e
def get_taskid():
    base_url = '/genie-cloud/api/v1/tasks/config/state/' + device_id
    task_list=[]
    url=genie_url+base_url
    print(url)
    result=requests.get(url)
    print(result)
    #取出task_id加载到task_list中
    # for sub_task in result[""]:
    #     task_list.append(sub_task)
    return result
task=get_taskid()
print(task)


#查询所有子设备
base_url='/argus-iot/v1/registries/'+registry_id+'/devices/'+device_id+'/sub-devices'
def get_devices(base_url):
    device_list=[]
    url=genie_url+base_url
    # print(url)
    result=requests.get(url).json()
    # print(result)
    # print(result["state_sub_devices"])
    try:
        for sub_device in result["state_sub_devices"]:
            device_list.append(sub_device["device_id"])
    except Exception as e:
        print(e)
    return device_list

# device=get_devices(base_url)
# print(device)



#删除子设备.可以是批量或单个。看传进去的参数:异步的返回成功只是云上的结果。还要边侧进行删除后才返回云端
def del_devices(sub_devices:List):
    try:
        for sub_deive in sub_devices:
            base_url='/argus-iot/v1/registries/'+registry_id+'/devices/'+device_id+'/sub-devices/'+sub_deive
            url=genie_url+base_url
            result=requests.delete(url)
            if result.status_code==200:
                print("删除成功")
            else:
                print(result.json())
    except Exception as e:
        print(e)

# sub_deives=get_devices(base_url)
# print(sub_deives)
# print(len(sub_deives))
# a=del_devices(sub_deives)
# print(a)


#批量删除任务
# def del_task(*args):
#     pass

