import requests
import json
import logging
import time
import random

requests.packages.urllib3.disable_warnings()

hostserver = "https://www.sfe.com/CONTACT-TRACING-EXTENSION"  # http://10.151.3.203:8634
startTime = "2022-04-06 18:10:00"
endTime = "2022-04-06 18:20:00"
refresh = False
personId = 0
runcount = 2  # 随机次数
# imageUrl = "/images/temp/20220406/24/5f9cfd5a06e84a98866b360a4567c548.png"  #帅哥 1602
imageUrl = "/images/temp/20220407/244/1711c49680cf4c23804cd7f3854fc949.png"
# imageUrl = "/images/temp/20220402/244/d1553317c6b54376a58c9110f0ab334c.png" #小孩 6922  -2312
# imageUrl = "/images/temp/20220406/24/282e73d237d7420cb0f5d9ecfced1e34.png"  #帅哥  7047  -2396

headers = {'Content-Type': 'application/json;charset=UTF-8'}
verify = False
Authorization = "Basic emYsMjp4c2NlZGs="

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

for k in range(runcount):
    refresh = random.choice([True, False])
    #     refresh = False

    print(f"----------------------------------------------------------------------------")
    print(f"refresh：{refresh}")

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
    #     for item in maskList:
    #         print(item['deviceInfo']['deviceName']+ "  ||  "+ item['snapshotInfo']['imgTime'])
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
    #     for item in trackList:
    #         print(item['deviceInfo']['deviceName']+ "  ||  "+ item['snapshotInfo']['imgTime'])
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
    res_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers,
                                data=json.dumps(fellows_post_data), verify=verify).json()
    fellows_data = []
    fellow_personIds = []
    fellows_tracks_total = 0
    if res_fellows["code"] == "0000":
        fellowsList = res_fellows["data"][f"{personId}"]
        for item in fellowsList:
            fellows_personId = item["personInfo"]["personId"]
            fellows_person_imgTime = item["snapshotInfo"]["imgTime"]
            # 密接轨迹查询
            fellow_track_post_data = {
                "personId": fellows_personId,
                "deviceIds": [],
                "startTime": startTime,
                "endTime": endTime,
                "refresh": refresh
            }
            #         res_fellows_track = requests.post(f"{hostserver}/doc/v1/person/tracks", headers=headers,data = json.dumps(fellow_track_post_data) ,verify=verify).json()
            #         if res_fellows_track['code'] == "0000":
            #             fellows_tracks_total +=len(res_fellows_track['data'])

            # 得到次密接查询条件
            fellows_data.append({
                "personId": fellows_personId,
                "imgTime": fellows_person_imgTime
            })
            fellow_personIds.append(fellows_personId)

        # 接人接触事件
        fellow_event_post_data = {
            "personId": personId,
            "fellowIds": fellow_personIds,
            "startTime": startTime,
            "endTime": endTime,
            "refresh": refresh
        }
        #     res_fellows_events = requests.post(f"{hostserver}/doc/v1/person/fellow/events", headers=headers,data = json.dumps(fellow_event_post_data) ,verify=verify).json()
        #     if res_fellows_events['code'] == "0000":
        #         print("")

        print(f"【密接人total】：{len(fellowsList)} ")
    else:
        print(f"次密接搜索fail {res_fellows['msg']}")

    # 通过密接  查次密接
    fellowsfellows_totals = 0
    fellows_fellows_tracks_total = 0
    for fellows in fellows_data:
        fellows_fellows_post_data = {
            "personIds": [fellows["personId"]],
            "deviceIds": [],
            "startTime": fellows["imgTime"],
            "endTime": "2022-04-07 00:00:00",
            "refresh": refresh
        }
        res_simple_fellows_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers,
                                                   data=json.dumps(fellows_fellows_post_data), verify=verify).json()
        if res_simple_fellows_fellows["code"] == "0000":
            fellowsfellowsList = res_simple_fellows_fellows["data"][f"{fellows['personId']}"]
            fellowsfellows_totals += len(fellowsfellowsList)  # 统计 累计次密接
            simple_fellows_fellows_track_total = 0
            fellowpersonidstr = ""
            for item in fellowsfellowsList:
                fellowpersonidstr += item['personInfo']['personId'] + ","
                if item['personInfo']['personId'] == "1630":
                    print(item['snapshotInfo']['imgTime'])

            print(f"密接:{fellows['personId']}，次密接total：{len(fellowsfellowsList)} ")
            print(fellowpersonidstr)
            print("--------------------------------------")

        # else:
            # print(f"次密接搜索fail {res_fellows_fellows['msg']}")

    print(f"【所有次密接total】：{fellowsfellows_totals}")

time.sleep(1)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



