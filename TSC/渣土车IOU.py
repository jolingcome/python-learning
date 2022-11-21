#矩形点位，计算IOU,IOU是2个矩形的交集/并集

vertices_1=[
    {
        "x": 81,
        "y": 0
    },
    {
        "x": 419,
        "y": 265
    }
]

vertices_2=[
    {
        "x": 75,
        "y": 80
    },
    {
        "x": 329,
        "y": 265
    }
]

# currentRect={"endX":626,"endY":569,"startX":554,"startY":533}
# sourceRect={"endX":854,"endY":490,"startX":792,"startY":458}
currentRect={"endX":626,"endY":569,"startX":554,"startY":533}
sourceRect={"endX":626,"endY":569,"startX":554,"startY":535}


#传入2个矩形框的2个点（目标框），默认是点位是相同的，所以每个目标框对应的场景大图是相同的，故可以用IOU来计算
def rect_IOU(rect1,rect2):
    # print(rect1[0])
    # px1=rect1[0]["x"]
    # py1=rect1[0]["y"]
    # px2=rect1[1]["x"]
    # py2=rect1[1]["y"]
    # gx1=rect2[0]["x"]
    # gy1=rect2[0]["y"]
    # gx2=rect2[1]["x"]
    # gy2=rect2[1]["y"]
    # # px1,py1,px2,py2=rect1
    # # gx1,gy1,gx2,gy2=rect2
    # print(f"矩形框1的坐标是：{px1},{py1},{px2},{py2}")
    # print(f"矩形框2的坐标是：{gx1},{gy1},{gx2},{gy2}")
    px1=rect1["startX"]
    py1=rect1["startY"]
    px2=rect1["endX"]
    py2=rect1["endY"]
    gx1=rect2["startX"]
    gy1=rect2["startY"]
    gx2=rect2["endX"]
    gy2=rect2["endY"]

    #求面积
    parea=(px2-px1)*(py2-py1)
    garea=(gx2-gx1)*(gy2-gy1)
    print(parea)
    print(garea)

    #求相交矩形的左上和右下顶点坐标（x1,y1,x2,y2）
    x1 = max(px1, gx1)  # 得到左上顶点的横坐标
    y1 = min(py1, gy1)  # 得到左上顶点的纵坐标
    x2 = min(px2, gx2)  # 得到右下顶点的横坐标
    y2 = max(py2, gy2)  # 得到右下顶点的纵坐标

    # 利用max()方法处理两个矩形没有交集的情况,当没有交集时,w或者h取0,比较巧妙的处理方法
    # w = max(0, (x2 - x1)) # 相交矩形的长，这里用w来表示
    # h = max(0, (y1 - y2)) # 相交矩形的宽，这里用h来表示
    # print("相交矩形的长是：{}，宽是：{}".format(w, h))
    # 这里也可以考虑引入if判断
    w = x2 - x1
    # h = y1 - y2
    h=y2-y1
    if w <= 0 or h <= 0:
        return 0

    area = w * h  # G∩P的面积
    print("G∩P的面积是：{}".format(area))

    # 并集的面积 = 两个矩形面积 - 交集面积
    IoU = area / (parea + garea - area)

    return IoU



if __name__=="__main__":
    IOU=rect_IOU(sourceRect,currentRect)
    print("IOU是：{}".format(IOU))


