import sensor
import image
import lcd
import time

# setting pi
PI = 3.14159265

# 参数设置,精确度设置
percision=3
# 目标宽度
objectivewitdh=30

# objectivewidth =

# 位置控制
# 距离
def comparewidth(current_width,percision=10,objectivewitdh=10):
    w_max = percision + objectivewitdh
    w_min = objectivewitdh - percision
    if current_width > w_max:
        return 1
    if current_width < w_min:
        return -1
    return 0

lcd.init()
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
# 设置颜色格式
sensor.set_pixformat(sensor.RGB565)
# 设置捕捉格式
sensor.set_framesize(sensor.QVGA)
# 设置增益
sensor.set_gainceiling(8)
# 设置亮度增益 +-2
sensor.set_brightness(1)
# 饱和度
sensor.set_saturation(1)
sensor.run(1)
# 图像大小阈值与误差范围
size_thresholds = [30,40]

#红色阈值[0],绿色阈值[1],蓝色阈值[2]
#(30, 100, 15, 127, 15, 127)
#(17, 32, -54, 22, -24, 14)
rgb_thresholds =[
                (0, 38, 8, 18, -128, 127),
                (0, 80, -70, -10, -0, 30),
                (0, 30, 0, 64, -128, -20)]
purpose = [0,0]
while True:
    # img=sensor.snapshot()
    # 镜头矫正
    img = sensor.snapshot().lens_corr(0.75)
    # 拉普拉斯锐化
    #img.laplacian(1,sharpen=True)
    #寻找色块对象
    blobs = img.find_blobs([rgb_thresholds[0]])
    a=[0,0,0,0,0,0,0,0,0]
    # 找出最大色块
    if blobs:
        for b in blobs:
            a[7]=b.area()
            if a[7]>a[6]:
                    a[6]=a[7]
                    a[0:4]=b.rect()
                    a[4]=b.cx()
                    a[5]=b.cy()
                    a[8]=b.rotation()
                    #获取方块对象的旋转角度，计算倾斜程度后矩形宽度
        img.draw_rectangle(a[0:4])
        img.draw_cross(a[4], a[5])
        # print(a)
            # 通过面积判断矩形面积确定物理距离
            # width=a[2] high=a[3] area=a[7]
        current_width = a[2]
        infer = comparewidth(current_width,percision,objectivewitdh)
        if  infer == -1:
            ## forward method
            print("so far",current_width)
            print("rotation = ",a[8]*180/PI)
        elif infer == 1:
            ## backward method
            print("too close",current_width)
            print("rotation = ",a[8]*180/PI)
        elif infer == 0:
            ## rotate method
            print("ok",current_width)
            print("rotation = ",a[8]*180/PI)
        # control_position(size,size_thresholds)
#   lcd.rotation(2)
    lcd.display(img)
