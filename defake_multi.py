# coding: utf-8


from asyncio import subprocess
import os
from re import T
import requests
import base64
import sys
import pandas as pd 
import numpy as np
import time
from queue import Queue
import threading
from concurrent.futures import ThreadPoolExecutor


times = time.time()
local_time = time.localtime(times)
 
# Y 年 - m 月 - d 日 H 时 - M 分 - S 秒
timestamp = time.strftime("%Y%m%d%H%M%S",local_time)

# defake_url = "http://10.198.21.126/advanced/v2/defake"
defake_url = "http://10.151.3.181/advanced/v2/defake"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_PATH = os.path.join(CURRENT_PATH,f"defake{timestamp}.csv")

dataList = []
id_queue = Queue(1000)
defake_reqeust_fail_count = 0

def video_to_png(videoPath):
    for root,dirs,files in os.walk(videoPath):
        for videoFile in files:
            if videoFile.endswith(("MOV","mov")):
                videoPath = os.path.join(root,videoFile)
                pngFileDir = os.path.join(root,videoFile[0:videoFile.index(".")],"png")
                if os.path.exists(pngFileDir) == False:
                    os.makedirs(pngFileDir)
                if len(os.listdir(pngFileDir)) > 0:
                    print("***************已解帧***************")
                    continue
                else:
                    cmd = f'ffmpeg -i "{videoPath}" "{pngFileDir}/%04d.png"'
                    # print(cmd)
                    os.system(cmd)


def defake_request_multi(videoPath):
    for root,dirs,files in os.walk(videoPath):
        for file in dirs:
            print(file)
            if file in ['png']:
                pngFileDir = os.path.join(root,file)
                picFileList = os.listdir(pngFileDir)
                #一个文件夹下的所有帧用多线程方式
                id_queue.queue.clear()
                for image in picFileList:
                    imagePath = os.path.join(pngFileDir,image)
                    # print(imagePath)
                    id_queue.put(imagePath)
                                   
                print(id_queue.qsize())
                while id_queue.qsize()> 0:
                    if id_queue.qsize() > 30:
                        thread_num = 30
                    else:
                        thread_num = id_queue.qsize()
                    print(f'***********f{thread_num}********')
                    for i in range(0,thread_num):
                        subThread = threading.Thread(target=defake_result_save,args=(i,))
                        # subThread.setDaemon(True)
                        subThread.start()

                    print (id_queue.qsize())


def defake_request_multi_pool(videoPath):
    for root,dirs,files in os.walk(videoPath):
        for file in dirs:
            print(file)
            if file in ['png','pic']:
                pngFileDir = os.path.join(root,file)
                picFileList = os.listdir(pngFileDir)
                #一个文件夹下的所有帧用多线程方式
                id_queue.queue.clear()
                for image in picFileList:
                    imagePath = os.path.join(pngFileDir,image)
                    # print(imagePath)
                    id_queue.put(imagePath)
                                   
                print(id_queue.qsize())
                while id_queue.qsize()> 0:
                    if id_queue.qsize() > 30:
                        thread_num = 30
                    else:
                        thread_num = id_queue.qsize()
                    print(f'***********start********')
                    pool = ThreadPoolExecutor(max_workers=thread_num,thread_name_prefix='defake_reqeust')
                    for i in range(0,thread_num):
                        feature = pool.submit(defake_result_save,i)
                    
                    pool.shutdown(wait=True)
                    print(f'***********end********')
                    print (id_queue.qsize())

    

def defake_result_save(num):
    print(threading.current_thread().name + "defake_result_save=" + str(num))
    imagePath = id_queue.get()
    # print(imagePath)
    # with open(imagePath,'rb') as imageFile:
    #     picBase64 =  base64.b64encode(imageFile.read()).decode("utf-8")
    files = {'file': (imagePath, open(imagePath, 'rb'), 'application/vnd.png', {'Expires': '0'})}
    response = requests.post(defake_url, files=files)
    
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        # responseData = response.json()
    else:
        responseData = None

    if responseData:
        if responseData['code'] == '0000':
            defakeScore = float(responseData['data']['score'][0])
            if defakeScore > 0.95:
                result = {}
                result["picPath"] = imagePath
                result['defake_score'] = defakeScore 
                dataList.append(result)

    return
        

def send_defake(imagePath):
    with open(imagePath,'rb') as imageFile:
        picBase64 =  base64.b64encode(imageFile.read()).decode("utf-8")
    # requests.post( url, files=(('city',(None,'beijing')),('city',(None,'shanghai'))))
    # response = requests.post(defake_url, files=(('data',(None,'picBase64')),))
    #文件方式
    files = {'file': (imagePath, open(imagePath, 'rb'), 'application/vnd.png', {'Expires': '0'})}
    response = requests.post(defake_url, files=files)
    # print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        responseData = response.json()
        if responseData["code"] == "0000":
            return responseData
        else:
            return None

if __name__== '__main__':
    # imagePath = "/Users/liulizhen/work_2022/testData/liveness/defakeData/interactive/png/1663145008675.png"
    imagePath = "/Users/liulizhen/Downloads/0001.png"
    # send_defake(imagePath)
    testPath  = sys.argv[1]
    # print(testPath)
    # video_to_png(testPath)
    # defake_request_multi(testPath)
    # thread = threading.Thread(target=defake_request_multi,args=(testPath,))
    # thread.start()
    defake_request_multi_pool(testPath)
    # time.sleep(60)

    pf2 = pd.DataFrame(dataList)
    pf2.to_csv(OUTPUT_FILE_PATH,encoding = 'utf-8',index = False,header = True)
    print("*********Done***************")
    