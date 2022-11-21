# 根据excel 创建device


import pandas as pd
import requests
import json
# 解析excel
# excel_path="D:\\医院项目\\医院生产\\V0.1_0617.xlsx"
# column_names=["点位名称","摄像机IP","流ID/CVR-IP:CVR-PORT/USER:PWD","defaultDensity","innerSpaceEnvInfo","outerSpaceEnvInfo"]

excel_path="D:\\医院项目\\医院生产\\曙光东院监控点位图_标注(筛选)-V0.1_0701.xlsx"
column_names=["点位名称","摄像机IP","流ID/CVR-IP:CVR-PORT/USER:PWD","defaultDensity","innerSpaceEnvInfo","outerSpaceEnvInfo"]
headers = {"Authorization": "Basic eWFuZ3lhbmdfdGVzdCwwOmowbnNhZQ==",
           "Content-Type": "application/json"}

nvr_devie={"3.3.100.5":"1536626720710586370",
           "3.3.100.4":"1536657249258434562",
           "3.3.100.102":"1536642333164171265"}


#读取excel里的值（按需要的列读取）
def read_excel(excel_path,sheet_name="Sheet1",column_names=column_names):
    df=pd.read_excel(excel_path,sheet_name=sheet_name)
    data=df.loc[:,column_names]
    return data

#创建设备
def create_device(location,guid):
    url="https://wwww.sfe.com/DEVICE/device/create"
    create_body={
        "operatePerson": "1",
        "name": "viper"+location,
        "defineNumber": "ST-20000001",
        "deptId": "0",
        "serial": "{{$guid}}", #随机生成
        "tag": "viper-server-1",
        "location": location
    }
    result=requests.post(url=url,headers=headers,data=json.dumps(create_body))
    if result.status_code=="200" and result["msg"]=="success":
        return result["data"]


def update_devie(device_id,RTSP,extraInfo):
    try:
        url="https://www.sfe.com/DEVICE/device/update"
        update_body={
            "id": device_id,
            "uri":RTSP,
            "extraInfo":extraInfo
        }
        result=requests.post(url=url,headers=headers,data=json.dumps(update_body))
        if result.status_code=="200" and result["msg"]=="success":
            return "更新成功"
    except Exception as e:
        print(e)


#NVR信息：{nvrInfo:'bbbb:002550',defaultDensity:0.8,innerSpaceEnvInfo:1,outerSpaceEnvInfo:0}
def nvr_Info(pre_data):
    nvrInfo={}
    # print(pre_data)
    rtsp_list=str(pre_data).split('/')
    flow_id=rtsp_list[0]
    nvr_ip=rtsp_list[1].split(":")[0]
    if nvr_ip in nvr_devie.keys():
        nvr_deviceIp=nvr_devie[nvr_ip]
        nvrInfo_1=f"{nvr_deviceIp}:{flow_id}"
        nvrInfo["nvrInfo"]=nvrInfo_1
    return nvrInfo

def nvr_data(nvr_info:dict,defaultDensity,innerSpaceEnvInfo,outerSpaceEnvInfo):
    nvr_info["defaultDensity"]=defaultDensity
    nvr_info["innerSpaceEnvInfo"]=innerSpaceEnvInfo
    nvr_info["outerSpaceEnvInfo"]=outerSpaceEnvInfo
    return nvr_info



#RTSP流 rtsp://admin:ab123456@3.3.1.175:554
def rtsp_data(ip):
    rtsp="rtsp://admin:ab123456@"+ip+":554"
    return rtsp

#生成随机序列
def getuid():
    pass


data=read_excel(excel_path,sheet_name="40路点位信息",column_names=column_names)
print(data)
for index,row in data.iterrows():
    print(row["点位名称"])
    location=row["点位名称"]
    ip=row["摄像机IP"]
    RTSP=rtsp_data(ip)
    nvr_Info_data=nvr_Info(row["流ID/CVR-IP:CVR-PORT/USER:PWD"])
    extraInfo=nvr_data(nvr_info=nvr_Info_data,defaultDensity=str(row["defaultDensity"]),innerSpaceEnvInfo=str(row["innerSpaceEnvInfo"]),outerSpaceEnvInfo=str(row["outerSpaceEnvInfo"]))
    print(extraInfo)
    guid=getuid()
    device_id=create_device(location,guid)
    update_devie(device_id, RTSP, extraInfo)




