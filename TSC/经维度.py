import random
import math
import pandas as pd
#  参数含义
# base_log：经度基准点，
# base_lat：维度基准点，
# radius：距离基准点的半径
def generate_random_gps(base_log=None, base_lat=None, radius=None):
    # radius_in_degrees = radius / 111300
    radius_in_degrees = radius / 1113 #随机到小数点后面的数字，这样就能撒开地图
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    # 这里是想保留14位小数
    loga = '%.6f' % longitude
    lata = '%.6f' % latitude
    return loga, lata
longitude1 = []
longitude2 = []
for i in range(500):
    # longitude_, latitude_ = generate_random_gps(base_log=121.1747112313, base_lat=25.02654402131123123, radius=100)
    longitude_, latitude_ = generate_random_gps(base_log=114.04397174942468, base_lat=22.594322588123834, radius=100)
    longitude1.append(longitude_)
    longitude2.append(latitude_)


# for i in range(96):
#     print(longitude1[i])
#
#
# for i in range(96):
#     print(longitude2[i])

dt=pd.DataFrame({"经度":longitude1,"维度":longitude2})
filepath=""
dt.to_excel(r"D:\TSC\result.xlsx")

