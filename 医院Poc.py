import requests
import json
import logging
import time
import datetime

requests.packages.urllib3.disable_warnings()

hostserver = "https://www.sfe.com/CONTACT-TRACING-EXTENSION"  # http://10.151.3.203:8634
startTime = "2022-04-06 18:10:00"
endTime = "2022-04-06 18:20:00"
refresh = False
personId = 0
imageUrl = "/images/temp/20220406/105/b05e1bc8df174f129cf91e54c1398ed0.png"
# imageUrl = "/images/temp/20220402/244/d1553317c6b54376a58c9110f0ab334c.png" #小孩 6922  -2312
# imageUrl = "/images/temp/20220406/24/282e73d237d7420cb0f5d9ecfced1e34.png"  #帅哥  7047  -2396

headers = {'Content-Type': 'application/json;charset=UTF-8'}
verify = False
Authorization = "Basic dGVzdCwyOmFzMjQ0cQ=="

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 获取token
# login_post = {
#  "username": "zf",
#   "password": "3ejdAbhiaTmX+QEyB4I35A==",
#   "accountType": "2"
# }
# res_login = requests.post(f"https://{hostserver}/GUNS/mgr/login", headers=headers,json.dumps(login_post) ,verify=False).json()
# if res_login["code"] == "0000":
#     Authorization = f'Basic {res_login['data']}"
# else:
#     print("获取token error")
headers["Authorization"] = Authorization

#


# 1:N 搜索 （流调者）
search_post = {
    "img": imageUrl
}
res_search = requests.post(f"{hostserver}/doc/v1/person/search", headers=headers, data=json.dumps(search_post),
                           verify=False).json()
if res_search['code'] == "0000":
    personId = res_search['data']['personId']
else:
    print(f"1:n fail {res_search['msg']}")

print("=============== 查询信息 ========")
print(f"流掉者: {personId} , http://www.sfe.com/intersense{imageUrl}")
print(f"时间范围：{startTime} 至 {endTime}")
print(f"refresh：{refresh}")
print(f"=================================")

# 未带口罩-异常事件
mask_post_data = {
    "personId": personId,
    "deviceIds": [],
    "maskStatus": [0],
    "startTime": startTime,
    "endTime": endTime,
    "refresh": refresh
}
res_mask = requests.post(f"{hostserver}/doc/v1/person/event/mask", headers=headers, data=json.dumps(mask_post_data),
                         verify=verify).json()
if res_mask['code'] == "0000":
    maskList = res_mask['data']
    print(f"【异常事件total】：{len(maskList)}")
    for item in maskList:
        print(item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime'])
else:
    print(f"口罩时间fail {res_mask['msg']}")

# 行动轨迹
track_post_data = {
    "personId": personId,
    "deviceIds": [],
    "startTime": startTime,
    "endTime": endTime,
    "refresh": refresh
}
res_track = requests.post(f"{hostserver}/doc/v1/person/tracks", headers=headers, data=json.dumps(track_post_data),
                          verify=verify).json()
if res_track['code'] == "0000":
    trackList = res_track['data']
    print(f"【轨迹total】：{len(trackList)}")
    for item in trackList:
        print(item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime'])
else:
    print(f"轨迹fail {res_track['msg']}")

# 密接搜索
fellows_post_data = {
    "personIds": [personId],
    "deviceIds": [],
    "startTime": startTime,
    "endTime": endTime,
    "refresh": refresh
}
res_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers, data=json.dumps(fellows_post_data),
                            verify=verify).json()
fellowsfellows_data = []
if res_fellows["code"] == "0000":
    fellowsList = res_fellows["data"][f"{personId}"]
    print(f"【所有密接人total】：{len(fellowsList)}")
    print(f"fellowList:{fellowsList}")
    fellowsfellows_totals = 0
    for item in fellowsList:
        # 取出密接者的信息，用于次密接查询
        fellows_personId = item["personInfo"]["personId"]
        fellows_person_imgTime = item["snapshotInfo"]["imgTime"]
        fellow_person_bgImg=item["snapshotInfo"]["bgImg"]
        fellow_person_Img=item["personInfo"]["personImg"]
        fellowsfellows_data.append({
            "personId": fellows_personId,
            "imgTime": fellows_person_imgTime,
            "person_bgImg":fellow_person_bgImg,
            "person_Img":fellow_person_Img
        })
#         fellows_fellows_post_data ={
#             "personIds":[fellows_personId],
#             "deviceIds":[],
#             "startTime": fellows_person_imgTime,
#             "endTime": "2022-04-02 00:00:00",
#             "refresh": refresh
#         }
#         res_fellows_fellows = requests.post(f"https://{hostserver}/CONTACT-TRACING-EXTENSION/doc/v1/person/fellows", headers=headers,data = json.dumps(fellows_fellows_post_data) ,verify=False).json()
#         if res_fellows_fellows["code"] == "0000":
#              fellowsfellowsList = res_fellows_fellows["data"][f"{fellows_personId}"]
#              fellowsfellows_totals +=len(fellowsfellowsList)
#              print(f"密接:{fellows_personId}，次密接total：{len(fellowsfellowsList)}")

else:
    print(f"次密接搜索fail {res_fellows['msg']}")

print(f"fellowsfellows_data:{fellowsfellows_data}")

# 查次密接
for fellows in fellowsfellows_data:
    fellows_fellows_post_data = {
        "personIds": [fellows["personId"]],
        "deviceIds": [],
        "startTime": fellows["imgTime"],
        "endTime": "2022-04-07 00:00:00",
        "refresh": refresh
    }
    res_fellows_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers,
                                        data=json.dumps(fellows_fellows_post_data), verify=verify).json()
    if res_fellows_fellows["code"] == "0000":
        fellowsfellowsList = res_fellows_fellows["data"][f"{fellows['personId']}"]
        fellowsfellows_totals += len(fellowsfellowsList)
        print(f"密接:{fellows['personId']}，次密接total：{len(fellowsfellowsList)}")

        fellowpersonidstr = ""
        for item in fellowsfellowsList:
            #             fellowpersonidstr += item['personInfo']['personId'] +","+item['snapshotInfo']['imgTime']+"  ||  "
            fellowpersonidstr += item['personInfo']['personId'] + ","
        print("")
        print(fellowpersonidstr)
        print("-------------------------------------")
    else:
        print(f"次密接搜索fail {res_fellows_fellows['msg']}")
print(f"【所有次密接total】：{fellowsfellows_totals}")






