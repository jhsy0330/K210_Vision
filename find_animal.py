import sensor, image, lcd, time
import KPU as kpu

labels = ['cat', 'dog']

#初始化
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((128, 128))
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)

lcd.clear()
lcd.draw_string(100,96,"MobileNet Demo")
lcd.draw_string(100,112,"Loading labels...")
f=labels

task = kpu.load(0x300000)
clock = time.clock()
while(True):
    img = sensor.snapshot()
    #img2=img.resize(128,128)
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    a = lcd.display(img, oft=(0,0))
    #lcd.draw_string(0, 224, "%.2f:%s                            "%(pmax, labels[max_index].strip()))
    img.draw_string(0,0, "%.2f : %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
    print(plist)
a = kpu.deinit(task)
