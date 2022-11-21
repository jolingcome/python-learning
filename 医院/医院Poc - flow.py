import requests
import json
import logging
import time
import datetime

requests.packages.urllib3.disable_warnings()

hostserver = "https://www.sfe.com/CONTACT-TRACING-EXTENSION"  # http://10.151.3.203:8634
startTime = "2022-06-23 22:00:00"
endTime = "2022-06-23 23:00:00"
refresh = False
# imageUrl = "/images/temp/20220623/80/72729523f08847a6abca52a92daf49cd.png"
# imageUrl = "/images/temp/20220402/244/d1553317c6b54376a58c9110f0ab334c.png" #小孩 6922  -2312
imageUrl = "/images/temp/20220704/80/6700bd3ec87547fba51de196b6acb69b.png"  #帅哥  414
# imageUrl="/images/temp/20220623/136/f2010b8a93264644b7c5660a348d3161.png" #联想男

headers = {'Content-Type': 'application/json;charset=UTF-8'}
verify = False
Authorization = "Basic emYsMjpoZXgyYjk="

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
headers["Authorization"] = Authorization


filepath= r'../a.txt'
def write_txt(filepath=filepath,str=""):
    with open(filepath,'a+',encoding='utf8') as f:
        f.writelines(str+'\n')


# 1:N 搜索 （流调者）
def search_N():
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
    str="流掉者: {} , http://www.sfe.com/intersense{}".format(personId,imageUrl)
    write_txt(str=str)
    write_txt(str="时间范围：{} 至 {}".format(startTime,endTime))
    write_txt(str="refresh：{}".format(refresh))
    write_txt(str="=================================")
    # print(f"流掉者: {personId} , http://www.sfe.com/intersense{imageUrl}")
    # print(f"时间范围：{startTime} 至 {endTime}")
    # print(f"refresh：{refresh}")
    # print(f"=================================")
    return personId


# 未带口罩-异常事件
def mask_data(personId):
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
        write_txt(str="【异常事件total】：{}".format(len(maskList)))
        # print(f"【异常事件total】：{len(maskList)}")
        for item in maskList:
            write_txt(str=item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime'])
            # print(item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime'])
    else:
        print(f"口罩时间fail {res_mask['msg']}")

# print(mask_data())

# 行动轨迹
def track_data(personId):
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
        # print(len(trackList)
        write_txt("【轨迹total】：{}".format(len(trackList)))
        print(f"【轨迹total】：{len(trackList)}")
        for item in trackList:
            write_txt(str=item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime']+"  ||  "+item['snapshotInfo']['targetImg'])
            # print(item['deviceInfo']['deviceName'] + "  ||  " + item['snapshotInfo']['imgTime']+"  ||  "+item['snapshotInfo']['targetImg'])
    else:
        print(f"轨迹fail {res_track['msg']}")
# print(track_data(personId))

# 密接搜索
def fellows_data(personId):
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
    fellows_personId_total=[]
    if res_fellows["code"] == "0000":
        fellowsList = res_fellows["data"][f"{personId}"]
        write_txt("【所有密接人total】：{}".format(len(fellowsList)))
        print(f"【所有密接人total】：{len(fellowsList)}")
        # print(f"fellowList:{fellowsList}")
        for item in fellowsList:
            # 取出密接者的信息，用于次密接查询
            fellows_personId = item["personInfo"]["personId"]
            fellows_personId_total.append(fellows_personId)
            fellows_person_imgTime = item["snapshotInfo"]["imgTime"]
            fellow_person_bgImg=item["snapshotInfo"]["bgImg"]
            fellow_person_Img=item["personInfo"]["personImg"]
            fellowsfellows_data.append({
                "personId": fellows_personId,
                "imgTime": fellows_person_imgTime,
                "person_bgImg":fellow_person_bgImg,
                "person_Img":fellow_person_Img
            })
    else:
        print(f"次密接搜索fail {res_fellows['msg']}")

    # print(f"fellowsfellows_data:{fellowsfellows_data}")
    return fellowsfellows_data,fellows_personId_total


# 查次密接
def fellows_fellows_data(fellowsfellows_data):
    fellowsfellows_totals = 0
    fellows_personIds=[]
    for fellows in fellowsfellows_data:
        fellows_fellows_post_data = {
            "personIds": [fellows["personId"]],
            "deviceIds": [],
            "startTime": fellows["imgTime"],
            "endTime": "2022-06-23 23:00:00",
            "refresh": refresh
        }
        res_fellows_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers,
                                            data=json.dumps(fellows_fellows_post_data), verify=verify).json()
        if res_fellows_fellows["code"] == "0000":
            fellowsfellowsList = res_fellows_fellows["data"][f"{fellows['personId']}"]
            fellowsfellows_totals += len(fellowsfellowsList)
            fellows_personIds.append(fellows['personId'])
            write_txt(str="密接:{fellows['personId']}，次密接total：{len(fellowsfellowsList)}")
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
    write_txt("【所有次密接total】：{fellowsfellows_totals}")
    return fellowsfellows_totals,fellows_personIds

# 查次密接，每次5-10个personId
def fellows_fellows_data1(fellowsPersonId_totals,step=5):
    fellowsfellows_totals = 0
    for i in range(0,len(fellowsPersonId_totals),step):
        # print(fellowsPersonId_totals[i:i+step])
        fellowsfellows_personIds=fellowsPersonId_totals[i:i+step]
        write_txt(str="fellowsfellows_personIds:{}".format(fellowsfellows_personIds))
        print(f"fellowsfellows_personIds:{fellowsfellows_personIds}")
        fellows_fellows_post_data = {
            "personIds": fellowsfellows_personIds,
            "deviceIds": [],
            "startTime": startTime,
            "endTime": endTime,
            "refresh": refresh
        }
        res_fellows_fellows = requests.post(f"{hostserver}/doc/v1/person/fellows", headers=headers,
                                            data=json.dumps(fellows_fellows_post_data), verify=verify).json()
        if res_fellows_fellows["code"] == "0000":
            # print(res_fellows_fellows)
            for person in fellowsfellows_personIds:
                fellowsfellowsList = res_fellows_fellows["data"][f"{person}"]
                fellowsfellows_totals += len(fellowsfellowsList)
                # print(f"fellowsfellowsList:{fellowsfellowsList}")
                write_txt(str="密接:{}，次密接total：{}".format(person,len(fellowsfellowsList)))
                print(f"密接:{person}，次密接total：{len(fellowsfellowsList)}")

                fellowpersonidstr = ""
                for item in fellowsfellowsList:
        #             #             fellowpersonidstr += item['personInfo']['personId'] +","+item['snapshotInfo']['imgTime']+"  ||  "
                    fellowpersonidstr += item['personInfo']['personId'] + ","
        #         print("")
                write_txt(str=fellowpersonidstr)
                write_txt(str="-------------------------------------")
                print(fellowpersonidstr)
                print("-------------------------------------")
        else:
            print(f"次密接搜索fail {res_fellows_fellows['msg']}")
    write_txt(str="【所有次密接total】：{}".format({fellowsfellows_totals}))
    print(f"【所有次密接total】：{fellowsfellows_totals}")
# return fellowsfellows_totals,fellows_personIds



#查次密接的轨迹
def fellowsfellows_track(fellows_personIds):
    for person in fellows_personIds:
        track_data(person)




if __name__=='__main__':
    start=time.time()
    personId = search_N() #1:N搜索
    mask_data=mask_data(personId) #未戴口罩异常数据
    track_data=track_data(personId) #行动轨迹
    fellowsfellows_data,fellowsPersonId_totals = fellows_data(personId) #密接
    print(f"fellowsfellows_data:{fellowsfellows_data}")
    print(f"fellowsPersonId_totals:{fellowsPersonId_totals}")
    # fellowfellow_totals,fellows_personIds=fellows_fellows_data(fellowsfellows_data) #次密接
    # fellowsfellows_track(fellows_personIds) #次密接轨迹
    fellowfellow_totals, fellows_personIds = fellows_fellows_data1(fellowsPersonId_totals)  # 次密接
    end=time.time()
    total_time=end-start
    write_txt(str="【总耗时】：{}".format(total_time))














