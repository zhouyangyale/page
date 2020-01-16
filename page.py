# Untitled - By: Administrator - 周四 11月 28 2019

import lvgl as lv
import lvgl_helper as lv_h
import lcd
import sensor
import time
import uos
import image
from machine import Timer
from machine import I2C
#import touchscreen as ts

import network
import utime
from Maix import GPIO
from fpioa_manager import *


#iomap at MaixDuino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

# get ADC0 ADC1 ADC2
adc = nic.adc( (0,1,2) )

count = 0
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
#ts.init(i2c)
lcd.init()
lv.init()

#fm.register(board_info.JTAG_TCK, fm.fpioa.GPIO0)
#key_1=GPIO(GPIO.GPIO0,GPIO.IN,GPIO.PULL_UP)
#fm.register(board_info.JTAG_TDI, fm.fpioa.GPIO1)
#key_2=GPIO(GPIO.GPIO1,GPIO.IN,GPIO.PULL_UP)
#fm.register(21, fm.fpioa.GPIO2)
#key_3=GPIO(GPIO.GPIO2,GPIO.IN,GPIO.PULL_UP)
#fm.register(22, fm.fpioa.GPIO3)
#key_4=GPIO(GPIO.GPIO3,GPIO.IN,GPIO.PULL_UP)

fm.register(10, fm.fpioa.GPIO4)
key_5=GPIO(GPIO.GPIO4,GPIO.IN,GPIO.PULL_DOWN)

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1,None,len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
disp_drv.hor_res = 320
disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)
#选中并来到新界面
style = lv.style_t()
lv.style_copy(style, lv.style_plain)
style.line.width = 10                          # 10 px thick arc
style.line.color = lv.color_hex3(0x258)        # Blueish arc color

style.body.border.color = lv.color_hex3(0xBBB) # Gray background color
style.body.border.width = 10
style.body.padding.left = 0

#page
style_sb = lv.style_t()
lv.style_copy(style_sb, lv.style_plain)
style_sb.body.main_color = lv.color_make(0,0,0)
style_sb.body.grad_color = lv.color_make(0,0,0)
style_sb.body.border.color = lv.color_make(0xff,0xff,0xff)
style_sb.body.border.width = 1
style_sb.body.border.opa = lv.OPA._70
style_sb.body.radius = 800 # large enough to make a circle
style_sb.body.opa = lv.OPA._60
style_sb.body.padding.right = 3
style_sb.body.padding.bottom = 3
style_sb.body.padding.inner = 8
page = lv.page(lv.scr_act())
page.set_size(150, 200)
page.align(None, lv.ALIGN.CENTER, 0, 0)
page.set_style(lv.page.STYLE.SB, style_sb)

#tab标签未选中状态的style
tab_style_rel = lv.style_t()
lv.style_copy(tab_style_rel,lv.style_plain)
tab_style_rel.body.main_color = lv.color_hex(0xc0c0c0)
tab_style_rel.body.grad_color = lv.color_hex(0xc0c0c0)
tab_style_rel.body.border.color = lv.color_hex(0xffffff)
tab_style_rel.body.border.width = 1

#tab标签选中状态的style
tab_style_pr = lv.style_t()
lv.style_copy(tab_style_pr,lv.style_plain)
tab_style_pr.body.main_color = lv.color_hex(0xffc0c0)
tab_style_pr.body.grad_color = lv.color_hex(0xffc0c0)
tab_style_pr.body.border.color = lv.color_hex(0xffffff)
tab_style_pr.body.border.width = 1

#top_state_btn_style  顶部状态栏的style
top_state_btn_style = lv.style_t()
lv.style_copy(top_state_btn_style,lv.style_plain)
top_state_btn_style.body.main_color = lv.color_hex(0xFFFFFF)
top_state_btn_style.body.grad_color = lv.color_hex(0xFFFFFF)
top_state_btn_style.body.border.color = lv.color_hex(0xffffff)
top_state_btn_style.body.border.width = 1
#sub_btn_style  顶部状态栏的style
sub_btn_style = lv.style_t()
lv.style_copy(top_state_btn_style,lv.style_plain)
top_state_btn_style.body.main_color = lv.color_hex(0xFFFFFF)
top_state_btn_style.body.grad_color = lv.color_hex(0xFFFFFF)
top_state_btn_style.body.border.color = lv.color_hex(0xffffff)
top_state_btn_style.body.border.width = 1
#swich 按钮关闭时的style
sw_off_style = lv.style_t()
lv.style_copy(sw_off_style,lv.style_pretty)
sw_off_style.body.radius = 800
sw_off_style.body.shadow.width = 4
sw_off_style.body.shadow.type = lv.SHADOW.BOTTOM

#swich 按钮打开时的style
sw_on_style = lv.style_t()
lv.style_copy(sw_on_style,lv.style_pretty)
sw_on_style.body.radius = 800
sw_on_style.body.shadow.width = 4
sw_on_style.body.shadow.type = lv.SHADOW.BOTTOM
sw_on_style.body.main_color = lv.color_hex(0x00ff00)
sw_on_style.body.grad_color = lv.color_hex(0x00ff00)

#list 未选中状态的style
ls_style_rel = lv.style_t()
lv.style_copy(ls_style_rel,lv.style_plain)
ls_style_rel.body.padding.top = 10
ls_style_rel.body.padding.bottom = 10
ls_style_rel.body.padding.left = 20
#list 选中时的style
ls_style_pr = lv.style_t()
lv.style_copy(ls_style_pr,lv.style_plain)
ls_style_pr.body.border.color = lv.color_hex(0xff0000)
ls_style_pr.body.main_color = lv.color_hex(0x00ff00)
ls_style_pr.body.padding.top = 10
ls_style_pr.body.padding.bottom = 10
ls_style_pr.body.padding.left = 20

#标签尺寸
TAB_WIDTH =100
TAB_HEIGHT = 100
#顶部状态栏尺寸
TOP_STATE_BTN_WIDTH = 320
TOP_STATE_BTN_HEIGHT = 30
#状态栏小标签尺寸
TOOLS_WIDTH = 30
TOOLS_HEIGHT = 20
#电池sign位置
battery_h_pos = 280
battery_v_pos = 5
#蓝牙，wifi,电池状态flag
battery_flag = 0
LAN_flag = 1

mute_plus_state = 0
cur_scr = lv.obj()
mute_flag = 0
mute_plus_state = 0
mute_minus_state = 0
mute_plus_flag = 1
mute_minus_flag = 0
mute_state = 0

#按键控制变量
key_flag = 0
cmd = 0
time0 = 0

#mute light information
class ML_tools():
    def __init__(self):
        self.flag = 0
        self.cm_flag = 0
        self.bar_value = 20
        self.chart = None

#wifi bluetooth information
class WB_tools():
    def __init__(self):
        self.flag = 0
        self.sw_flag = 0
        self.state = 0
        self.toggle_flag = 0
        self.cont_flag = 0
        self.index = 0
        self.preloading = 0
        self.ls = []

#language information  flag = 0,english  flag = 1,chinese
class Language():
    def __init__(self):
        self.flag = 0
        self.toggle_flag = 0
        self.index = 0
        self.names = ["English","Chinese"]
class Power():
    def __init__(self):
        self.flag = 0
class Info():
    def __init__(self):
        self.page_flag = 0
class Program():
    def __init__(self):
        self.btn_state = lv.btn.STATE.REL
        self.index = 0
class App():
    def __init__(self):
        self.btn_state = lv.btn.STATE.REL
        self.index = 0
class Setting():
    def __init__(self):
        self.btn_state = lv.btn.STATE.REL
        self.index = 1
class Dir():
    def __init__(self):
        self.btn_state = lv.btn.STATE.REL
        self.index = 0

class Control_bar():
    def __init__(self):
        self.value = 0
        self.pbtn_state = lv.btn.STATE.REL
        self.plus_state = lv.btn.STATE.REL
        self.minus_state = lv.btn.STATE.REL

#press key after a period time,clear the state value,recover init value
def key_init():
    global key_flag
    global cmd
    key_flag = 0
    cmd = 0

#create a btn in the top of screen ,which is uesed to place wifi,bluetooth,battery sign
def create_top_state_btn(parent):
    top_state_btn = lv.btn(parent)
    top_state_btn.set_layout(lv.LAYOUT.OFF)
    top_state_btn.set_size(TOP_STATE_BTN_WIDTH,TOP_STATE_BTN_HEIGHT)
    top_state_btn.set_style(0,top_state_btn_style)
    return top_state_btn


'''
*****************************************************************************
create a btn with img of bluetooth sign at location h_pos,v_pos
parameter    parent is the bluetooth btn's parent btn's name
*****************************************************************************
'''
def create_bluetooth_sign(parent,h_pos,v_pos):
    if buth.flag == 1:
        bluetooth_btn = lv.btn(parent)
        bluetooth_btn.set_size(TOOLS_WIDTH,TOOLS_HEIGHT)
        bluetooth_btn.align(None,lv.ALIGN.IN_TOP_LEFT,h_pos,v_pos)
        bluetooth_img = lv.img(bluetooth_btn)
        bluetooth_img.set_src(lv.SYMBOL.BLUETOOTH)
        return True
    else:
        return False

'''
*****************************************************************************
create a btn with img of wifi sign at location h_pos,v_pos
parameter    parent is the wifi btn's parents' btn's name
*****************************************************************************
'''
def create_wifi_sign(parent,h_pos,v_pos):
    if wifi.flag == 1:
        wifi_btn = lv.btn(parent)
        wifi_btn.align(None,lv.ALIGN.IN_TOP_LEFT,h_pos,v_pos)
        wifi_btn.set_size(TOOLS_WIDTH,TOOLS_HEIGHT)
        wifi_img = lv.img(wifi_btn)
        wifi_img.set_src(lv.SYMBOL.WIFI)
        return True
    else:
        return False
'''
*****************************************************************************
create a btn with img of battery sign at location h_pos,v_pos
parameter    parent is the battery btn's parents' btn's name
*****************************************************************************
'''
def create_battery_sign(parent,h_pos,v_pos,battery_flag):
    battery_btn = lv.btn(parent)
    battery_btn.align(None,lv.ALIGN.IN_TOP_LEFT,h_pos,v_pos)
    battery_btn.set_size(TOOLS_WIDTH,TOOLS_HEIGHT)
    battery_img = lv.img(battery_btn)
    if battery_flag == 0:
        battery_img.set_src(lv.SYMBOL.BATTERY_EMPTY)
    elif battery_flag == 1:
        battery_img.set_src(lv.SYMBOL.BATTERY_1)
    elif battery_flag == 2:
        battery_img.set_src(lv.SYMBOL.BATTERY_2)
    elif battery_flag == 3:
        battery_img.set_src(lv.SYMBOL.BATTERY_3)
    else:
        battery_img.set_src(lv.SYMBOL.BATTERY_FULL)

'''
*****************************************************************************
create a btn
parameter    parent is the battery btn's parents' btn's name
             width  width of the button
             height height od the button
             style_rel tht style of the rel state default is lv.btn.STYLE.REL
             style_pr tht style of the pr state default is lv.btn.STYLE.PR
             layout_flag control the layout state of the button ,default is lv.LAYOUT.ON
*****************************************************************************
'''
def create_btn(parent,width=100,height=100,style_rel=lv.style_btn_rel,style_pr=lv.style_btn_pr,layout_flag=lv.LAYOUT.CENTER):
    name = lv.btn(parent)
    name.set_size(width,height)
    name.set_style(0,style_rel)
    name.set_style(1,style_pr)
    name.set_layout(layout_flag)
    return name

'''
*****************************************************************************
set symbol for obj
parameter    parent   parent  obj
             symbol   symbol type of the obj(lv.SYMBOL.)
*****************************************************************************
'''
def set_symbol_for_obj(parent,symbol):
    img = lv.img(parent)
    img.set_src(symbol)
    return img

'''
*****************************************************************************
set label for obj
parameter    parent   parent  obj
             labelname   the string of the label
*****************************************************************************
'''
def open_sensor():
    global key_flag
    global cmd
    global time0

    lcd.init()
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    while 1:
        key_detect()
        if cmd:
            key_flag = 1
            taketime = time.ticks_ms() - time0
        img = sensor.snapshot()
        lcd.display(img)
        if cmd == "back" and taketime > 250:
            key_init()
            print("-----------------ok------------------")
            sensor.shutdown(1)
            time.sleep_ms(1000)
            return True
        elif cmd == "left":
            key_init()
        elif cmd == "right":
            key_init()
        elif cmd == "ok":
            key_init()

#set text label for btn obj,labelname is a string
def set_label_for_obj(parent,labelname):
    label = lv.label(parent)
    label.set_text(labelname)
    label.align(None,lv.ALIGN.CENTER,0,0)
    return label

#create a lvgl.sw ,not used in current
def create_swich_btn(parent,off_style,on_style):
    sw = lv.sw(parent)
    sw.align(None,lv.ALIGN.CENTER,0,0)
    sw.set_style(lv.sw.STYLE.KNOB_OFF,off_style)
    sw.set_style(lv.sw.STYLE.KNOB_ON,on_style)
    return sw

#create a lvgl.list,with a list show a series similar content
def create_list(parent,namels,index):
    ls_width = 320
    ls_height = 240
    ls = lv.list(parent)
    ls.set_size(ls_width,ls_height)
    ls.set_style(lv.list.STYLE.BTN_REL,ls_style_rel)
    ls.set_style(lv.list.STYLE.BTN_PR,ls_style_pr)
    ls.set_sb_mode(lv.SB_MODE.AUTO)
    ls.align(None,lv.ALIGN.IN_TOP_MID,0,70)
    btn_num = len(namels)
    if btn_num == 0:
        set_label_for_obj(ls,"not find")
    else:
        name = []
        for i in range(btn_num):
            name.append("btn"+str(i))
        for i in range(btn_num):
            name[i] = ls.add_btn(lv.SYMBOL.SAVE,namels[i])
        if index != 0:
            ls.set_btn_selected(name[index-1])
    lv.list.focus(ls.get_btn_selected(),lv.ANIM.OFF)
    return ls


def select_box(scr,parent,name,state,sw_flag,ls,index):
    pwidth = 320
    pheight = 50
    swidth = 40
    sheight = 40
    pbtn = create_btn(parent,pwidth,pheight,layout_flag = lv.LAYOUT.OFF)
    pbtn.align(None,lv.ALIGN.IN_TOP_MID,0,0)
    sbtn = create_btn(pbtn,swidth,sheight)
    sbtn.align(None,lv.ALIGN.IN_RIGHT_MID,-30,0)
    if not state:
        lv.btn.set_state(sbtn,lv.btn.STATE.PR)
    elif state and sw_flag == 0:
        lv.btn.set_state(pbtn,lv.btn.STATE.PR)
    label = set_label_for_obj(pbtn,"%s"%name)
    label.align(None,lv.ALIGN.IN_LEFT_MID,30,0)
    if state:
        img = set_symbol_for_obj(sbtn,lv.SYMBOL.OK)
        ls = create_list(parent,ls,index)
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr
def control_bar(parent,bar_value):
    pbtn_width = 300
    pbtn_height = 60
    bar_width = 200
    bar_height = 20
    pbtn = create_btn(parent,pbtn_width,pbtn_height,layout_flag=lv.LAYOUT.OFF)
    pbtn.align(None,lv.ALIGN.CENTER,0,0)
    pbtn.set_hidden(True)
    label = set_label_for_obj(pbtn,'%d'%bar_value+"%")
    label.align(None,lv.ALIGN.IN_BOTTOM_MID,0,0)
    bar = lv.bar(pbtn)
    bar.set_size(bar_width,bar_height)
    bar.set_range(0,100)
    bar.set_value(bar_value,lv.ANIM.OFF)
    bar.align(None,lv.ALIGN.CENTER,0,0)
    #加号按钮
    mute_plus = create_btn(pbtn,40,40)
    mute_plus.align(None,lv.ALIGN.IN_RIGHT_MID,0,0)
    set_symbol_for_obj(mute_plus,lv.SYMBOL.RIGHT)
    #减号按钮
    mute_minus = create_btn(pbtn,40,40)
    mute_minus.align(None,lv.ALIGN.IN_LEFT_MID,0,0)
    set_symbol_for_obj(mute_minus,lv.SYMBOL.LEFT)
    return bar_value,pbtn,mute_plus,mute_minus

def lan_ch_page(scr,parent,ls,index):
    lan_ls = lv.list(parent)
    lan_ls.set_size(200,100)
    lan_ls.align(None,lv.ALIGN.IN_TOP_LEFT,20,40)
    ch_ls = lv.list(parent)
    ch_ls.set_size(50,100)
    ch_ls.align(None,lv.ALIGN.IN_TOP_LEFT,220,40)
    lan_btn0 = lan_ls.add_btn(None,ls[0])
    lan_btn1 = lan_ls.add_btn(None,ls[1])
    lan_ls.set_btn_selected(lan_btn0)
    ch_btn0 = ch_ls.add_btn(lv.SYMBOL.OK,"")
    ch_btn1 = ch_ls.add_btn(None,"")
    if lan.flag == 1:
        ch_ls.clean()
        ch_btn0 = ch_ls.add_btn(None,"")
        ch_btn1 = ch_ls.add_btn(lv.SYMBOL.OK,"")
    if index == 1:
        lan_ls.set_btn_selected(lan_btn1)
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr

def toggle_swich_page(scr,parent,name,sw_state,names,list_index):
    width = 320
    height = 40
    state_btn = create_btn(parent,width,height,layout_flag=lv.LAYOUT.OFF)
    swich = create_swich_btn(state_btn,sw_off_style,sw_on_style)
    swich_label = set_label_for_obj(state_btn,name)
    if sw_state:
        swich.on(lv.ANIM.OFF)
    swich.align(None,lv.ALIGN.IN_RIGHT_MID,-20,0)
    swich_label.align(None,lv.ALIGN.IN_LEFT_MID,20,0)

    if sw_state:
        ls = create_list(parent,names,list_index)
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr


def create_template():
    tools_pos = 10
    v_pos = 5
    scr = lv.obj()
    #顶部状态栏button
    top_state_btn = create_top_state_btn(scr)
    #电池状态按钮，位于右边
    create_battery_sign(top_state_btn,battery_h_pos,battery_v_pos,battery_flag)
    #蓝牙状态按钮，位于左边
    if create_bluetooth_sign(top_state_btn,tools_pos,v_pos):
        tools_pos += TOOLS_WIDTH
    #无线状态按钮，位于左边
    if create_wifi_sign(top_state_btn,tools_pos,v_pos):
        tools_pos += TOOLS_WIDTH
    sub_btn = create_btn(scr,320,210,sub_btn_style,sub_btn_style,layout_flag=lv.LAYOUT.OFF)
    sub_btn.align(None,lv.ALIGN.IN_TOP_MID,0,30)
    return scr,sub_btn

def create_home_page(scr,parent,index,prm,app,setting,dire):
    #print("enter home page")
    HOME_TAB_WIDTH = 150
    HOME_TAB_HEIGHT = 100
    prm_btn = create_btn(parent,HOME_TAB_WIDTH,HOME_TAB_HEIGHT,tab_style_rel,tab_style_pr)
    prm_btn.align(None,lv.ALIGN.IN_TOP_LEFT,10,0)
    set_symbol_for_obj(prm_btn,lv.SYMBOL.PLAY)
    #set_label_for_obj(prm_btn,"Program")
    app_btn = create_btn(parent,HOME_TAB_WIDTH,HOME_TAB_HEIGHT,tab_style_rel,tab_style_pr)
    app_btn.align(None,lv.ALIGN.IN_TOP_RIGHT,-10,0)
    set_symbol_for_obj(app_btn,lv.SYMBOL.LIST)
    #set_label_for_obj(app_btn,"App")
    set_btn = create_btn(parent,HOME_TAB_WIDTH,HOME_TAB_HEIGHT,tab_style_rel,tab_style_pr)
    set_btn.align(None,lv.ALIGN.IN_BOTTOM_RIGHT,-10,-10)
    set_symbol_for_obj(set_btn,lv.SYMBOL.SETTINGS)
    #set_label_for_obj(set_btn,"Setting")
    file_btn = create_btn(parent,HOME_TAB_WIDTH,HOME_TAB_HEIGHT,tab_style_rel,tab_style_pr)
    file_btn.align(None,lv.ALIGN.IN_BOTTOM_LEFT,10,-10)
    set_symbol_for_obj(file_btn,lv.SYMBOL.DIRECTORY)
    #set_label_for_obj(file_btn,"File")
    if LAN_flag:
        set_label_for_obj(prm_btn,"Program")
        set_label_for_obj(app_btn,"App")
        set_label_for_obj(set_btn,"Setting")
        set_label_for_obj(file_btn,"Directory")
    else:
        set_label_for_obj(prm_btn,"程序")
        set_label_for_obj(app_btn,"应用")
        set_label_for_obj(set_btn,"设置")
        set_label_for_obj(file_btn,"文件")
    if index == 0:
        lv.btn.set_state(prm_btn,lv.btn.STATE.PR)
    elif index == 1:
        lv.btn.set_state(app_btn,lv.btn.STATE.PR)
    elif index == 2:
        lv.btn.set_state(set_btn,lv.btn.STATE.PR)
    else:
        lv.btn.set_state(file_btn,lv.btn.STATE.PR)
    prm.btn_state = lv.btn.get_state(prm_btn)
    app.btn_state = lv.btn.get_state(app_btn)
    setting.btn_state = lv.btn.get_state(set_btn)
    dire.btn_state = lv.btn.get_state(file_btn)

    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr,index,prm,app,setting,dire


def create_set_page1(parent,index,mute,buth,wifi):
    #print("enter setting page")
    #音量控制条
    #ctr_bar = Control_bar()
    mute.bar_value,mute_message_btn,mute_plus,mute_minus = control_bar(parent,mute.bar_value)
    #蓝牙控制按钮
    bu_state_btn = create_btn(parent,80,30,layout_flag=lv.LAYOUT.OFF)
    bu_state_btn.align(None,lv.ALIGN.IN_TOP_MID,0,0)
    bu_state_btn.set_hidden(True)
    bu_state = create_swich_btn(bu_state_btn,sw_off_style,sw_on_style)
    #wifi 控制按钮
    wifi_state_btn = create_btn(parent,80,30,layout_flag=lv.LAYOUT.OFF)
    wifi_state_btn.align(None,lv.ALIGN.IN_TOP_LEFT,-10,0)
    wifi_state_btn.set_hidden(True)
    wifi_state = create_swich_btn(wifi_state_btn,sw_off_style,sw_on_style)
    #mute_btn.set_state(lv.btn.STATE.PR)
    mute_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    mute_btn.align(None,lv.ALIGN.IN_TOP_LEFT,10,0)
    set_symbol_for_obj(mute_btn,lv.SYMBOL.MUTE)
    #set_label_for_obj(mute_btn,"Mute")
    #power 按钮
    power_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    power_btn.align(None,lv.ALIGN.IN_TOP_MID,0,0)
    set_symbol_for_obj(power_btn,lv.SYMBOL.POWER)
    #set_label_for_obj(power_btn,"Power")
    #bu 按钮
    bu_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    bu_btn.align(None,lv.ALIGN.IN_TOP_RIGHT,-10,0)
    set_symbol_for_obj(bu_btn,lv.SYMBOL.BLUETOOTH)
    #set_label_for_obj(bu_btn,"Bluetooth")
    #wf 按钮
    wifi_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    wifi_btn.align(None,lv.ALIGN.IN_BOTTOM_RIGHT,-10,-10)
    set_symbol_for_obj(wifi_btn,lv.SYMBOL.WIFI)
    #set_label_for_obj(wifi_btn,"Wifi")
    name_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    name_btn.align(None,lv.ALIGN.IN_BOTTOM_MID,0,-10)
    set_symbol_for_obj(name_btn,lv.SYMBOL.EDIT)
    #set_label_for_obj(name_btn,"Name")
    info_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    info_btn.align(None,lv.ALIGN.IN_BOTTOM_LEFT,10,-10)
    set_symbol_for_obj(info_btn,lv.SYMBOL.DRIVE)
    #set_label_for_obj(info_btn,"Info")
    if LAN_flag:
        set_label_for_obj(mute_btn,"Mute")
        set_label_for_obj(power_btn,"Power")
        set_label_for_obj(bu_btn,"Bluetooth")
        set_label_for_obj(wifi_btn,"Wifi")
        set_label_for_obj(name_btn,"Name")
        set_label_for_obj(info_btn,"Info")
    else:
        set_label_for_obj(mute_btn,"音量")
        set_label_for_obj(power_btn,"电源")
        set_label_for_obj(bu_btn,"蓝牙")
        set_label_for_obj(wifi_btn,"无线")
        set_label_for_obj(name_btn,"设备名称")
        set_label_for_obj(info_btn,"信息")
    if index == 0:
        lv.btn.set_state(mute_btn,lv.btn.STATE.PR)
    elif index == 1:
        lv.btn.set_state(power_btn,lv.btn.STATE.PR)
    elif index == 2:
        lv.btn.set_state(bu_btn,lv.btn.STATE.PR)
    elif index == 3:
        lv.btn.set_state(wifi_btn,lv.btn.STATE.PR)
    elif index == 4:
        lv.btn.set_state(name_btn,lv.btn.STATE.PR)
    else:
        lv.btn.set_state(info_btn,lv.btn.STATE.PR)
    #打开音量控制
    if mute.chart:
        mute_message_btn.move_foreground()
        mute_message_btn.set_hidden(False)
        if mute.cm_flag == 0:
            pass
        elif mute.cm_flag == 1:
            lv.btn.set_state(mute_plus,lv.btn.STATE.PR)
        elif mute.cm_flag == 2:
            lv.btn.set_state(mute_minus,lv.btn.STATE.PR)
        else:
            pass
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr,mute,buth,wifi

def create_set_page2(parent,index,light):
    lan_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    lan_btn.align(None,lv.ALIGN.IN_TOP_LEFT,10,0)
    set_symbol_for_obj(lan_btn,lv.SYMBOL.LOOP)
    #set_label_for_obj(lan_btn,"Language")
    light_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    light_btn.align(None,lv.ALIGN.IN_TOP_MID,0,0)
    set_symbol_for_obj(light_btn,lv.SYMBOL.EJECT)
    #set_label_for_obj(light_btn,"Light")
    dev_btn = create_btn(parent,TAB_WIDTH,TAB_HEIGHT,tab_style_rel,tab_style_pr)
    dev_btn.align(None,lv.ALIGN.IN_TOP_RIGHT,-10,0)
    set_symbol_for_obj(dev_btn,lv.SYMBOL.LEFT)
    #set_label_for_obj(dev_btn,"Devices")
    if LAN_flag:
        set_label_for_obj(lan_btn,"Language")
        set_label_for_obj(light_btn,"Light")
        set_label_for_obj(dev_btn,"Devices")
    else:
        set_label_for_obj(lan_btn,"语言")
        set_label_for_obj(light_btn,"亮度")
        set_label_for_obj(dev_btn,"设备")
    if index == 6:
        lv.btn.set_state(lan_btn,lv.btn.STATE.PR)
    elif index == 7:
        lv.btn.set_state(light_btn,lv.btn.STATE.PR)
    elif index == 8:
        lv.btn.set_state(dev_btn,lv.btn.STATE.PR)
    if lan_btn.get_state() == lv.btn.STATE.PR:
        #language控制
        pass
    elif light.chart:
        light.bar_value,light_message_btn,light_plus,light_minus = control_bar(parent,light.bar_value)
        light_message_btn.move_foreground()
        light_message_btn.set_hidden(False)
        if light.cm_flag == 0:
            pass
        elif light.cm_flag == 1:
            lv.btn.set_state(light_plus,lv.btn.STATE.PR)
            light.tmp = 1
        elif light.cm_flag == 2:
            lv.btn.set_state(light_minus,lv.btn.STATE.PR)
            light.tmp = 2
        else:
            pass
    elif dev_btn.get_state() == lv.btn.STATE.PR:
        #设备控制
        pass
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr,light
def create_prm_page(parent,index):
    ls_width = 280
    ls_height = 240
    prm_list = lv.list(parent)
    prm_list.set_size(ls_width,ls_height)
    prm_list.align(None,lv.ALIGN.CENTER,0,30)
    prm_list.set_style(lv.list.STYLE.BTN_PR,ls_style_pr)
    ls_btn0 = prm_list.add_btn(lv.SYMBOL.SAVE,"Tracking car")
    ls_btn1 = prm_list.add_btn(lv.SYMBOL.SAVE,"Table lamp")
    ls_btn2 = prm_list.add_btn(lv.SYMBOL.SAVE,"Garbage classification")
    if index == 0:
        prm_list.set_btn_selected(ls_btn0)
    elif index == 1:
        prm_list.set_btn_selected(ls_btn1)
    elif index == 2:
        prm_list.set_btn_selected(ls_btn2)
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr
def create_keyboard_page():
    scr = lv.obj()
    # Create styles for the keyboard
    rel_style = lv.style_t()
    pr_style  = lv.style_t()

    lv.style_copy(rel_style, lv.style_btn_rel)
    rel_style.body.radius = 0
    rel_style.body.border.width = 1
    lv.style_copy(pr_style, lv.style_btn_pr)
    pr_style.body.radius = 0
    pr_style.body.border.width = 1
    # Create a keyboard and apply the styles
    kb = lv.kb(scr)
    kb.set_cursor_manage(True)
    kb.set_map(defalt_kb_map)
    kb.set_style(lv.kb.STYLE.BG, lv.style_transp_tight)
    kb.set_style(lv.kb.STYLE.BTN_REL, rel_style)
    kb.set_style(lv.kb.STYLE.BTN_PR, pr_style)

    #lv.btnm.set_btn_width(kb,0,1)
    lv.btnm.set_btn_width(kb,11,2)
    lv.btnm.set_btn_width(kb,12,2)
    lv.btnm.set_btn_width(kb,22,2)

    pwd_ta = lv.ta(scr)
    pwd_ta.set_text("");
    pwd_ta.set_pwd_mode(True)
    pwd_ta.set_one_line(True)
    pwd_ta.set_width(240 // 2 - 20)
    pwd_ta.set_pos(5, 20)
    # Create a label and position it above the text box
    pwd_label = lv.label(scr)
    pwd_label.set_text("Password:")
    pwd_label.align(pwd_ta, lv.ALIGN.OUT_TOP_LEFT, 0, 0)
    #ta.set_placeholder_text( "sjfowfw")
    # Assign the text area to the keyboard
    kb.set_ta(pwd_ta)
    kb.set_cursor_manage(True)
    cur_scr = scr.get_screen()
    lv.scr_load(scr)
    return cur_scr,kb,btn_index,pwd_ta
def creat_preload(parent,sw_int,lw_int,clo_hex=0xFF0000,time_ms=2000,st=lv.style_plain):
    pre = lv.preload(parent)
    st.line.width = lw_int
    st.line.color = lv.color_hex(clo_hex)
    pre.set_arc_length(int(sw_int*2))
    pre.set_spin_time(time_ms)
    pre.set_size(sw_int,sw_int)
    pre.set_style(0,style)

def key_detect():
    global cmd
    global time0
    global gpio_flag
    global new_key_once
    gpio_flag+=1
    if gpio_flag >=200:
        gpio_flag = 0
    if gpio_flag >= 100:
        GPIO(GPIO.GPIO4,GPIO.IN,GPIO.PULL_UP)
    elif gpio_flag <100:
        GPIO(GPIO.GPIO4,GPIO.IN,GPIO.PULL_DOWN)
    if key_flag == 0:
        adc = nic.adc()
        if adc[3] == 15:
            new_key_once = 1
            print(adc[3])
        else:
            print(adc[3])
        if new_key_once == 1:
            if adc[3] == 7:
                cmd = "left"
                #print("left")
                time0 = time.ticks_ms()
                new_key_once = 0
            elif adc[3] == 13:
                cmd = "right"
                #print("right")
                time0 = time.ticks_ms()
                new_key_once = 0
            elif adc[3] == 14:
                cmd = "ok"
                #print("ok")
                time0 = time.ticks_ms()
                new_key_once = 0
            elif adc[3] == 11:
                cmd = "back"
                #print("back")
                time0 = time.ticks_ms()
                new_key_once = 0
            else:
                pass

#program page variable init
prm = Program()
app = App()
setting = Setting()
dire = Dir()
#setting page variable init
wifi = WB_tools()
mute = ML_tools()
light = ML_tools()
buth = WB_tools()
lan = Language()
power = Power()
info = Info()

btn_index = 0
power_flag = 0
home_flag = 1
set_flag = 0
prm_flag = 0
app_flag = 0
dir_flag = 0
keyboard_flag = 0
gpio_flag = 0
new_key_noce = 0
start_time = time.ticks_ms()
chart_cont_starttime = 0

aps = nic.scan()
while True:

    wifi_scan_result = []
    buth_scan_result = []
    i = 0;
    for ap in aps:
#print("SSID:{:}".format(ap[0]))
      wifi_scan_result.append(ap[0])
      i = i + 1
    if home_flag:
        scr,sub_btn = create_template()
        cur_scr,btn_index,prm,app,setting,dire = create_home_page(scr,sub_btn,btn_index,prm,app,setting,dire)
        FLAG = 1
        print("-----------------------------------------")
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime>250:
                FLAG = 0
                print("******")
                if cmd == "right":
                    if btn_index >= 3:
                        btn_index = 0
                    else:
                        btn_index += 1
                elif cmd == "left":
                    if btn_index == 0:
                        btn_index = 3
                    else:
                        btn_index -= 1
                elif cmd == "ok":
                    home_flag = 0
                    if btn_index ==0:
                        prm_flag = 1
                        prm.index = 0
                    elif btn_index ==1:
                        app_flag = 1
                        #app.index = 0
                    elif btn_index == 2:
                        set_flag = 1
                        setting.index = 0
                    elif btn_index == 3:
                        dir_flag = 1
                    else:
                        print("error")
                elif cmd == "back":
                    #print("this is home page")
                    pass
        key_init()
        cur_scr.delete()
    elif set_flag:
        scr,sub_btn = create_template()
        if setting.index <= 5:
            cur_scr,mute,buth,wifi = create_set_page1(sub_btn,setting.index,mute,buth,wifi)
        elif setting.index <= 8:
            cur_scr,light = create_set_page2(sub_btn,setting.index,light)
        FLAG = 1
        print("-----------------------------------------")
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if mute.chart:
                #print("enter mute in_de_crease control")
                if key_flag :
                    if cmd == "right":
                        mute.cm_flag = 1
                        if taketime > 250:
                            FLAG = 0
                            mute.bar_value += 10
                            if mute.bar_value >= 100:
                                mute.bar_value = 100
                            mute.cm_flag = 3
                            key_init()
                    elif cmd == "left":
                        mute.cm_flag = 2
                        if taketime > 250:
                            FLAG = 0
                            mute.bar_value -= 10
                            if mute.bar_value <= 0:
                                mute.bar_value = 0
                            mute.cm_flag = 3
                            key_init()
                    elif cmd == "back" and taketime > 250:
                        FLAG = 0
                        mute.chart = 0
                        key_init()
                    elif cmd == "ok" and taketime > 250:
                        FLAG = 0
                        key_init()
            elif light.chart:
                #print("enter light control bar")
                if key_flag:
                    if cmd == "right":
                        light.cm_flag = 1
                        if taketime > 250:
                            FLAG = 0
                            if light.bar_value >= 100:
                                light.bar_value = 100
                            else:
                                light.bar_value += 25
                                if light.bar_value > 100:
                                    light.bar_value = 100
                            light.cm_flag = 3
                            key_init()
                    elif cmd == "left":
                        light.cm_flag = 2
                        if taketime > 250:
                            FLAG = 0
                            if light.bar_value <= 0:
                                light.bar_value = 0
                            else:
                                light.bar_value -= 25
                                if light.bar_value < 0 :
                                    light.bar_value = 0
                            light.cm_flag = 3
                            key_init()
                    elif cmd == "back" and taketime > 250:
                        FLAG = 0
                        light.chart = 0
                        key_init()
                    elif cmd == "ok" and taketime > 250:
                        FLAG = 0
                        key_init()
            if key_flag and taketime > 250:
                FLAG = 0
                if power_flag:
                    pass
                if cmd == "right":
                    if setting.index >= 8:
                        setting.index = 0
                    else:
                        setting.index += 1
                elif cmd == "left":
                    if setting.index <= 0:
                        setting.index = 8
                    else:
                        setting.index -= 1
                elif cmd == "ok":
                    if setting.index == 0:
                        mute.chart = True
                    elif setting.index == 1:
                        power.flag = 1
                        print("power")
                    elif setting.index == 2:
                        buth.toggle_flag = 1
                        set_flag = 0
                    elif setting.index == 3:
                        wifi.toggle_flag = 1
                        set_flag = 0
                    elif setting.index == 5:
                        info.page_flag = 1
                        set_flag = 0
                    elif setting.index == 6:
                        lan.toggle_flag = 1
                        set_flag = 0
                    elif setting.index == 7:
                        light.chart = True
                    else:
                        print("the block is empty now")
                elif cmd == "back":
                    set_flag = 0
                    home_flag = 1
                key_init()
        cur_scr.delete()
    elif prm_flag:
        scr,sub_btn = create_template()
        cur_scr = create_prm_page(sub_btn,prm.index)
        FLAG = 1
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                FLAG = 0
                if cmd == "right":
                    if prm.index == 2:
                        prm.index = 0
                    else:
                        prm.index += 1
                elif cmd == "left":
                    if prm.index == 0:
                        prm.index = 2
                    else:
                        prm.index -= 1
                elif cmd == "ok":
                    pass
                elif cmd == "back":
                    prm_flag = 0
                    home_flag = 1
                key_init()
        cur_scr.delete()
    elif app_flag:
        print("app")
        app_flag = 0
        home_flag =1
    elif dir_flag:
        print("dir_flag")
        dir_flag = 0
        home_flag = 1
    elif wifi.toggle_flag:
        print("wifi swich page")
        scr,sub_btn = create_template()
        #创建wifi开关
        cur_scr = select_box(scr,sub_btn,"wifi",wifi.state,wifi.sw_flag,wifi.ls,wifi.index)
        if wifi.cont_flag == 1:
            chart_cont_starttime = time.ticks_ms()
            btn = lv.btn(cur_scr)
            btn.set_size(100,100)
            btn.align(None,lv.ALIGN.CENTER,0,0)
            label = lv.label(btn)
            label.set_text("success")
        elif wifi.cont_flag == 2:
            chart_cont_starttime = time.ticks_ms()
            btn = lv.btn(cur_scr)
            btn.set_size(100,100)
            btn.align(None,lv.ALIGN.CENTER,0,0)
            label = lv.label(btn)
            label.set_text("failed")
        #cur_scr = toggle_swich_page(scr,sub_btn,"Wifi",wifi.state,wifi.names,wifi.list_index)
        FLAG = 1
        print("-----------------------------------------")
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            if chart_cont_starttime:
                if tim - chart_cont_starttime > 500:
                    FLAG = 0
                    wifi.cont_flag = 0
                    chart_cont_starttime = 0
                    continue
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                FLAG = 0
                if wifi.sw_flag == 0:
                    if cmd == "ok" :
                        if wifi.state == 0:
                            wifi.state = 1
                            wifi.flag =1
                            wifi.ls = wifi_scan_result
                        else:
                            wifi.state = 0
                            wifi.flag = 0
                            wifi.index = 0
                            wifi.ls = []
                    elif cmd == "back":
                        wifi.toggle_flag = 0
                        set_flag = 1
                    elif cmd == "right":
                        if wifi.state:
                            wifi.sw_flag = 1
                            if len(wifi.ls):
                                wifi.index = 1
                            else:
                                wifi.index = 0
                else:
                    if len(wifi.ls):
                        if cmd == "right":
                            if wifi.index == len(wifi.ls):
                                pass
                            else:
                                wifi.index += 1
                        elif cmd == "left":
                            if wifi.index == 1:
                                wifi.sw_flag = 0
                                wifi.index = 0
                            else:
                                wifi.index -= 1
                        elif cmd == "ok":
                            wifi.toggle_flag = 0
                            keyboard_flag =  1
                        elif cmd == "back":
                            wifi.toggle_flag = 0
                            set_flag = 1
                    else:
                        if cmd == "back":
                            wifi.toggle_flag = 0
                            set_flag = 1
                        elif cmd == "ok":
                            if wifi.state == 0:
                                wifi.state = 1
                                wifi.flag =1
                                wifi.ls = wifi_scan_result
                            else:
                                wifi.state = 0
                                wifi.flag = 0
                                wifi.index = 0
                                wifi.ls = []
                key_init()
        cur_scr.delete()
    elif buth.toggle_flag:
        #print("buth swich page")
        scr,sub_btn = create_template()
        #cur_scr = toggle_swich_page(scr,sub_btn,"BLUETOOTH",buth.state,buth.names,buth.list_index)
        cur_scr = select_box(scr,sub_btn,"Bluetooth",buth.state,buth.sw_flag,buth.ls,buth.index)
        FLAG = 1
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                FLAG = 0
                if buth.sw_flag == 0:
                    if cmd == "ok" :
                        if buth.state == 0:
                            buth.state = 1
                            buth.flag = 1
                            buth.ls = buth_scan_result
                        else:
                            buth.state = 0
                            buth.flag = 0
                            buth.index = 0
                            buth.ls = []
                    elif cmd == "back":
                        buth.toggle_flag = 0
                        set_flag = 1
                    elif cmd == "right":
                        if buth.state :
                            buth.sw_flag = 1
                            if len(buth.ls):
                                buth.index = 1
                            else:
                                buth.index = 0
                else:
                    if len(buth.ls):
                        if cmd == "right":
                            if buth.index == len(buth.ls):
                                pass
                            else:
                                buth.index += 1
                        elif cmd == "left":
                            if buth.index == 1:
                                buth.sw_flag = 0
                                buth.index = 0
                            else:
                                buth.index -= 1
                        elif cmd == "ok":
                            #进入buth密码输入页面
                            pass
                        elif cmd == "back":
                            buth.toggle_flag = 0
                            set_flag = 1
                    else:
                        if cmd == "back":
                            buth.toggle_flag = 0
                            set_flag = 1
                        elif cmd == "ok" :
                            if buth.state == 0:
                                buth.state = 1
                                buth.flag = 1
                                buth.ls = buth_scan_result
                            else:
                                buth.state = 0
                                buth.flag = 0
                                buth.index = 0
                                buth.ls = []
                key_init()
        cur_scr.delete()
    elif lan.toggle_flag:
        scr,sub_btn = create_template()
        cur_scr = lan_ch_page(scr,sub_btn,lan.names,lan.index)
        FLAG = 1
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                FLAG = 0
                if cmd == "left" or cmd == "right":
                    if lan.index == 0:
                        lan.index =1
                    else:
                        lan.index = 0
                elif cmd == "ok":
                    if lan.index == 0:
                        lan.flag = 0
                    elif lan.index == 1:
                        lan.flag = 1
                elif cmd == "back":
                    lan.toggle_flag = 0
                    set_flag = 1
        key_init()
        cur_scr.delete()
    elif info.page_flag:
        scr,sub_btn = create_template()
        btn = create_btn(sub_btn,100,100)
        label = set_label_for_obj(btn,"open sensor")
        lv.scr_load(scr)
        cur_scr = scr.get_screen()
        FLAG = 1
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                FLAG = 0
                if cmd == "ok":
                    cur_scr.delete()
                    key_init()
                    res = open_sensor()
                    if res:
                        key_init()
                    print(FLAG,"---------------")
                elif cmd == "back" and taketime > 250:
                    info.page_flag = 0
                    set_flag = 1
                    key_init()
                    cur_scr.delete()
    elif keyboard_flag:
        flag = 1
        btn_index = 18
        k_style = lv.style_t()
        upper_kb_map=["#","Q","W","E","R","T","Y","U","I","O","P","Bksp","\n",
                       "abc","A","S","D","F","G","H","J","K","L","Enter","\n",
                       "_","-","Z","X","C","V","B","N","M",",",".",":","\n",
                       "0","1","2","3","4","5","6","7","8","9",""]
        defalt_kb_map = ["#","q","w","e","r","t","y","u","i","o","p","Bksp","\n",
                        "ABC","a","s","d","f","g","h","j","k","l","Enter","\n",
                        "_","-","z","x","c","v","b","n","m",",",".",":","\n",
                        "0","1","2","3","4","5","6","7","8","9",""]
        cur_scr,kb,btn_index,pwd_ta = create_keyboard_page()
        FLAG = 1
        while FLAG:
            lv.tick_inc(5)
            lv.task_handler()
            tim = time.ticks_ms()
            char = lv.btnm.get_btn_text(kb,btn_index)
            lv.btnm.set_pressed(kb,btn_index)
            key_detect()
            if cmd:
                key_flag = 1
                taketime = time.ticks_ms() - time0
            if key_flag and taketime > 250:
                if cmd == "right":
                    if btn_index >= 44:
                        btn_index = 0
                    else:
                        btn_index += 1
                elif cmd == "left":
                    if btn_index <= 0:
                        btn_index = 44
                    else:
                        btn_index -= 1
                elif cmd == "ok":
                    #print(char,type(char))
                    if char == "Bksp":
                        print("enter del")
                        lv.ta.del_char(pwd_ta)
                    elif char == "ABC":
                        kb.set_map(upper_kb_map)
                        lv.btnm.set_btn_width(kb,11,2)
                        lv.btnm.set_btn_width(kb,12,2)
                        lv.btnm.set_btn_width(kb,22,2)
                        btn_index = 18
                    elif char == "abc":
                        kb.set_map(defalt_kb_map)
                        lv.btnm.set_btn_width(kb,11,2)
                        lv.btnm.set_btn_width(kb,12,2)
                        lv.btnm.set_btn_width(kb,22,2)
                        btn_index = 18
                    elif char == "Enter":
                        #connect success wifi.cont_flag = 1  if failed,wifi.cont_flag = 2
                        res = pwd_ta.get_text()
                        pwd_ta.set_text("")
                        print(res)
                        FLAG = 0
                        keyboard_flag = 0
                        wifi.cont_flag = 1
                        wifi.toggle_flag = 1
                    else:
                        pwd_ta.add_text("%s"%char)
                elif cmd == "back":
                    FLAG = 0
                    keyboard_flag = 0
                    wifi.toggle_flag = 1
                key_init()
        cur_scr.delete()
    while time.ticks_ms()-tim < 0.0005:
        pass

