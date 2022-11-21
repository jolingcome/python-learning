import requests
import json
import pandas as pd


hostserver="www.sfe.com"


startTime = "2022-06-23 15:00:00"
endTime = "2022-06-23 16:00:00"
refresh = False
imageUrl="/images/temp/20220623/136/f2010b8a93264644b7c5660a348d3161.png" #联想男

headers = {'Content-Type': 'application/json;charset=UTF-8'}
verify = False
Authorization = "Basic emYsMjoxeGU5ZXU="
headers["Authorization"] = Authorization


# file_path=r"distance.xlsx"
# def write_exe(file_path,sheet_name="",data):
#     dataframe=pd.DataFrame(data)
#     dataframe.to_excel(file_name=file_path,sheet_name=sheet_name,header=0)
#
#
# #取出distance,
# def fellows_data(personId):
#     persons_dic={}
#     fellows_post_data = {
#         "personIds": [personId],
#         "deviceIds": [],
#         "startTime": startTime,
#         "endTime": endTime,
#         "refresh": refresh
#     }
#     res_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers, data=json.dumps(fellows_post_data),
#                                 verify=verify).json()
#     if res_fellows["code"] == "0000":
#         fellowsList = res_fellows["data"]["fellows"]
#         fellow_devices=res_fellows["data"]["deviceId"]
#         for items in fellowsList:
#             personId=items["personInfo"]["personId"]
#             distance=items["nearInfo"]["distance"]
#             persons_dic[personId]=personId
#             persons_dic[distance]=persons_dic
#             persons_dic[fellow_devices]=fellow_devices
#             write_exe(file_path)

import jsonschema
json_data =[
{"pm10": 24,"city": "珠海","time": "2016-10-23 13:00:00"},
{"pm10": 24,"city": "深圳","time": "2016-10-21 13:00:00"},
{"pm10": "21","city": "广州","time": "2016-10-23 13:00:00"}
]

jason_scheme={"type": "array","items": {"type": "object","properties": {"pm10": {"type": "number",},"city": {"type": "string","enum": ["珠海", "深圳"]},"time": {"type": "string"}}}}

try:
    jsonschema.validate(json_data,jason_scheme)
except jsonschema.ValidationError as ex:
    msg=ex
    print(ex)

import dictdiffer
first_dict = {
"templates": "11",
"template1": "11",
"data": {
"name": "鸣人",
"age": 22,
"sex": "女",
"title": "六代火影"
    }  # 数据
}

second_dict = {
"templates": "99",
"template2": "t2",
"template3": "t3",
"data": {
"name": "鸣人",
"age": 22,
"sex": "男",
"title": "六代火影"
    }  # 数据
}


for diff in list(dictdiffer.diff(first_dict, second_dict)):
    print(diff)


import grequests
import requests
import time

start=time.time()
res_list=[requests.get("https://github.com") for i in range(100)]
end=time.time()
print(end-start)


start=time.time()
res_list_1=[grequests.get("https://github.com") for i in range(100)]
res_result=grequests.map(res_list_1)
end=time.time()
print(end-start)

