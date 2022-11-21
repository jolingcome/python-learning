import json
import requests
import pandas as pd
from functools import wraps

#获取密接
file_path=r"liudiao"
personIds=["6906"]
save_path=r"2.txt"

# import urllib3.contrib.pyopenssl
# urllib3.contrib.pyopenssl.inject_into_urllib3()

import warnings
warnings.filterwarnings('ignore')


#调接口
base_url="https://www.sfe.com"
headers={"Authorization":"Basic emZ0ZXN0LDI6eXRsc2g0",
         "Content-Type":"application/json"}
body={
    "personIds":personIds,
    "deviceIds":[],
    "startTime":"2022-04-01 13:44:52",
    "endTime":"2022-04-02 00:00:00",
    "refresh":False
}

def get_company_person(body):
    path_url = "/CONTACT-TRACING-EXTENSION/doc/v1/person/fellows"
    url=base_url+path_url
    # print(url)
    # print(body)
    result=requests.post(url=url,headers=headers,data=json.dumps(body),verify=False)
    return result.json()
# result=get_company_person(body)
# print(type(result))


def get_data(personId):
    bgImags=[]
    targetImgs=[]
    personIds={}
    personImgs=[]
    result_total=[]
    try:
        file=get_company_person(body)
        # print(file)
        print(personId)
        # print(file["data"][personId])
        results=file["data"][personId]
        # print(results)
        print(len(results))
        for i in results:
            personInfo = i["personInfo"]
            personId_sub = personInfo["personId"]
            personImg = personInfo["personImg"]
            personImgs.append(personImg)
            result_total.append(personImg)
            data1=i["snapshotInfo"]
            # print(data1)
            imgTime=data1["imgTime"]
            personIds[personId_sub] =imgTime
            # imgTimes.append(imgTime)
            bgImg=data1["bgImg"]
            bgImags.append(bgImg)
            result_total.append(bgImg)
            targetImg=data1["targetImg"]
            targetImgs.append(targetImg)
    except Exception as e:
        print(e)
    return result_total,personIds,len(results)

#写入excel
def write_to_excel(dict,index='密接',coloumns=["time"],save_path=r'C:\yangling2\桌面\test.xlsx'):
    df = pd.DataFrame.from_dict(dict, orient='index', columns=coloumns)
    df = df.reset_index().rename(columns={'index': index})
    df.to_excel(save_path)

#写入密接
for i in personIds:
    # print(i)
    results,personId_all,count=get_data(i)
    print(personId_all)
    # print(count)
    #用dateframe写入到excel中
    write_to_excel(personId_all)


#次密接
# print(personId_all)
# A=pd.DataFrame()
import csv
# for key in personId_all.keys():
#     print(key)
#     personIds[0]=key
#     result_total, personId_1,count1= get_data(key)
#     # print(personId_1)
#     print(count1)
#     # personId_1[key]=count1
#     print(personId_1)
#     with open(r"C:\yangling2\桌面\test1.csv", "a", newline='') as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         header=["密接者id","次密接总人数","次密接personId","次密接时间"]
#         if header is None:
#             writer.writerow(header)
#         for key1, value1 in personId_1.items():
#             writer.writerow([key,count1]+[key1,value1])


# print(A)
# A.to_excel(r'C:\yangling2\桌面\test1.xlsx',columns=["次密接","time"])
# write_to_excel(A,index="次密接",save_path=r'C:\yangling2\桌面\test1.xlsx')

#写入密接的bgImg和personImg
# for result in results:
#     with open(save_path,'a',encoding='utf8') as p:
#         p.write(result+"\n")












    # print(result)



