import requests
import json
import threading
import time
from gevent import monkey
# monkey.patch_all()
import gevent
import sys, io
# 解决console显示乱码的编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


requests.packages.urllib3.disable_warnings()

hostserver = "https://www.sfe.com/CONTACT-TRACING-EXTENSION"  # http://10.151.3.203:8634
startTime = "2022-04-06 18:10:00"
endTime = "2022-04-06 18:20:00"
refresh = False
imageUrl = "/images/temp/20220406/105/b05e1bc8df174f129cf91e54c1398ed0.png"
# imageUrl = "/images/temp/20220402/244/d1553317c6b54376a58c9110f0ab334c.png" #小孩 6922  -2312
# imageUrl = "/images/temp/20220406/24/282e73d237d7420cb0f5d9ecfced1e34.png"  #帅哥  7047  -2396

headers = {'Content-Type': 'application/json;charset=UTF-8'}
verify = False
Authorization = "Basic dGVzdCwyOmpmdWE5Yg=="

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
headers["Authorization"] = Authorization


class Douban(object):
    # def runtime(func):
    #     def wrapper(*args, **kwargs):
    #         start_time = time.time()
    #         res = func(*args, **kwargs)
    #         end_time = time.time()
    #         print(func.__name__ + " running time is %.6f s" % (end_time - start_time))
    #         return res
    #     return wrapper



    # 1:N 搜索 （流调者）
    def search_N(self):
        personId=0
        search_post = {
            "img": imageUrl
        }
        try:
            res_search = requests.post(f"{hostserver}/doc/v1/person/search", headers=headers, data=json.dumps(search_post),
                                       verify=False).json()
            if res_search['code'] == "0000":
                personId = res_search['data']['personId']
        except Exception as e:
            print(e)
        return personId


    # 未带口罩-异常事件
    def mask_data(self,personId):
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
            return res_mask
        else:
            print(f"口罩时间fail {res_mask['msg']}")

    # print(mask_data())

    # 行动轨迹
    def track_data(self,personId):
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
            return res_track
        # else:
        #     print(f"轨迹fail {res_track['msg']}")

    # 密接搜索
    def fellows_data(self,personId):
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
            # print(f"【所有密接人total】：{len(fellowsList)}")
            # print(f"fellowList:{fellowsList}")
            for item in fellowsList:
                # 取出密接者的信息，用于次密接查询
                fellows_personId = item["personInfo"]["personId"]
                fellows_person_imgTime = item["snapshotInfo"]["imgTime"]
                # fellow_person_bgImg=item["snapshotInfo"]["bgImg"]
                # fellow_person_Img=item["personInfo"]["personImg"]
                fellowsfellows_data.append({
                    "personId": fellows_personId,
                    "imgTime": fellows_person_imgTime,
                })
        # else:
        #     print(f"次密接搜索fail {res_fellows['msg']}")

        # print(f"fellowsfellows_data:{fellowsfellows_data}")
        return fellowsfellows_data


    # 查次密接
    def fellows_fellows_data(self,fellowsfellows_data):
        fellowsfellows_totals = 0
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
                # print(f"密接:{fellows['personId']}，次密接total：{len(fellowsfellowsList)}")

            #     fellowpersonidstr = ""
            #     for item in fellowsfellowsList:
            #         #             fellowpersonidstr += item['personInfo']['personId'] +","+item['snapshotInfo']['imgTime']+"  ||  "
            #         fellowpersonidstr += item['personInfo']['personId'] + ","
            #     print("")
            #     print(fellowpersonidstr)
            #     print("-------------------------------------")
            # else:
            #     print(f"次密接搜索fail {res_fellows_fellows['msg']}")
        print(f"【所有次密接total】：{fellowsfellows_totals}")
        return fellowsfellows_totals

    def run_flow(self):
        personId = self.search_N() #1:N搜索
        mask_data=self.mask_data(personId) #未戴口罩异常数据
        track_data=self.track_data(personId) #行动轨迹
        fellowsfellows_data = self.fellows_data(personId) #密接
        fellows_fellows_data=self.fellows_fellows_data(fellowsfellows_data) #次密接

if __name__ == '__main__':
    test = Douban()
    threads = []
    start=time.time()
    for i in range(2):
        thread = gevent.spawn(test.run_flow())
    threads.append(thread)
    gevent.joinall(threads)
    end=time.time()
    print(end-start)



















