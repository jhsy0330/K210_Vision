import sensor
import image
import lcd
import time

# 位置控制
# 距离
def control_position(size,size_thresholds_min,size_thresholds_max)

    if size > size_thresholds_min and size < size_thresholds_max:
        print('ok',size)
    # 比例大于阈值，远离目标
    elif size > size_thresholds_max:
        print('up close',size)
    # 比例小于阈值，靠近目标
    elif size < size_thresholds_min:
        print('so far',size)
# 方向
def hori_control_orientation(current_x,target_x = 0,precision = 20)
    target=[target_x+precision,target_x-precision]
    if current_x < target[0] and current_x > target[1]:
        pass
    if current_x < target[1]:
        pass
    if current_x > target[0]:
        pass


lcd.init()
sensor.reset(freq=24000000, set_regs=True, dual_buff=True)
# 设置颜色格式
sensor.set_pixformat(sensor.RGB565)
# 设置捕捉格式
sensor.set_framesize(sensor.QQVGA)
# 设置亮度增益 +-2
# sensor.set_brightness(1)
# 饱和度
# sensor.set_saturation(1)
sensor.run(1)
# 图像大小阈值与误差范围
size_thresholds = [30,40]

#红色阈值[0],绿色阈值[1],蓝色阈值[2]
rgb_thresholds =[
                (30, 100, 15, 127, 15, 127),
                (0, 80, -70, -10, -0, 30),
                (0, 30, 0, 64, -128, -20)]
purpose = [0,0]
while True:
    # img=sensor.snapshot()
    # 镜头矫正
    img = sensor.snapshot().lens_corr(1.9)
    #寻找色块对象
    blobs = img.find_blobs([rgb_thresholds[1]])
    a=[0,0,0,0,0,0,0,0]
    if blobs:
        for b in blobs:
            a[7]=b.area()
            if a[7]>a[6]:
                    a[6]=a[7]
                    a[0:4]=b.rect()
                    a[4]=b.cx()
                    a[5]=b.cy()
        img.draw_rectangle(a[0:4])
        img.draw_cross(a[4], a[5])
        # print(a)
            # 通过面积判断矩形面积确定物理距离
            # width=a[2] high=a[3] area=a[7]
        size = a[2]
        control_position(size,size_thresholds)
#   lcd.rotation(2)
    lcd.display(img)
