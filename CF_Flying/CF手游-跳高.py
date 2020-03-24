#imports
from time import time
from time import sleep
import tkinter as tk
from tkinter import messagebox
from damo import Key,Mouse,DM,Time,VK
dm = DM()
vk = VK
kk = Key(dm)
ms = Mouse(dm)

class Change_data():
    def __init__(self):
        self.process_name = 'LdBoxHeadless.exe'
        self.feature_code = "F4 04 35 3F F4 04 35 3F 00 00 00 00 00 00 80 3F 00 00 00 00 21 D5 31 3F CD CC 4C 3D 85 EB 51 3E 00 00 00 00 00 00 00 00 00 00 80 3F 00 01 00 01"
        self.move = '5c'
        self.addrs = 0

    # 根据特征码定位内存地址
    def get_hwnd(self):
        self.hwnd = dm.FindWindowByProcess(self.process_name, '', '')
        return self.hwnd

    #得到特征码地址
    def get_addrs(self):

        t1 = Time()
        # addrs = dm.FindData(hwnd, "00040000-FFFFFFFF", feature_code).split('|')
        self.addrs = dm.FindDataEx(self.hwnd, "00040000-FFFFFFFF", self.feature_code, 4, 1, 0).split('|')

        self.cost_time = round(t1.now(), 1)
        print(self.cost_time, '秒,', self.addrs)

    # 16进制的运算，根据特征码+偏移，得到数据地址
    def get_addr(self,move):
        if(self.addrs == 0):
            print('Error!')
            return 0
        return [hex(int(i, 16) + int(move, 16)) for i in self.addrs]

    # 得到xyz坐标的地址
    def get_addr_xyz(self):
        self.addr_x = self.get_addr('54')
        self.addr_z = self.get_addr('5c')
        self.addr_y = self.get_addr('64')
        self.addr_xyz = self.addr_x,self.addr_y,self.addr_z

    # 得到xyz坐标的真实数值
    def get_value_xyz(self):
        self.x, self.y, self.z = self.get_double_data(self.addr_x), self.get_double_data(self.addr_y), self.get_double_data(self.addr_z)
        self.xyz = self.x, self.y, self.z
        return self.x, self.y, self.z

    #简化版，综合以上
    def get_xyz(self):
        self.get_addr_xyz()
        self.get_value_xyz()
        return self.x,self.y,self.z

    # init
    if(1):
        # 一些16进制的计算函数，16进制的字符串之间的运算

        def str_int(self, str_x):
            x0 = '0x' + str_x
            x0 = int(x0, 16)
            x0
            return x0

        def str_hex(self, str_x):
            x0 = '0x' + str_x
            x0 = int(x0, 16)
            x0
            return hex(x0)

        def sub_x0_xs(self, x0, x_s):
            if (x_s.__class__.__name__ == 'str'):
                return hex(self.str_int(x0) - self.str_int(x_s))

            ls = []
            for i in x_s:
                if (i == ''):
                    continue
                ls.append(hex(self.str_int(x0) - self.str_int(i)))
            return ls

        def add_x0_xs(self, x0, x_s):
            if (x_s.__class__.__name__ == 'str'):
                return hex(self.str_int(x0) + self.str_int(x_s))

            ls = []
            for i in x_s:
                if (i == ''):
                    continue
                ls.append(hex(self.str_int(x0) + self.str_int(i)))
            return ls

        def get_double_data(self,addr):
            return [dm.ReadDouble(self.hwnd, i) for i in addr]

    # 写入UI界面中entry输入的数值
    def write_entry_data(self,addr,sleep_t=0.01):
        data = float(v_entry.get())
        # for addr_i in addr:
            #dm.WriteData(self.hwnd, addr_i, data)
        if (dm.stop_0('a')):
            dm.WaitKey(ord('A'),0)
        print(data)
        sleep(sleep_t)

    def stop(self):
        if(kk.state(vk.alt)):
            if(kk.state('t')):
                print('---stop!---')
                sleep(0.5)
                dm.WaitKey('t',0)

    #死锁数值
    def run_func(self,addr,value=2.3, T=3, sleep_t=0.001):
        #addr = self.addr_z

        print(value,T,sleep_t)



        data = dm.DoubleToData(value)
        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break
            if(self.stop()):
                break

            for addr_i in addr:
                dm.WriteData(self.hwnd, addr_i, data)
            sleep(sleep_t)

    # 快捷键型死锁数值，Alt+w = 高度增加，ALt+s = 高度减少
    def jump(self,addr,value = 3, T=3, sleep_t=0.1,control_value = 0.3):
        #addr = self.addr_z

        print(value,T,sleep_t)

        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break
            if(self.stop()):
                break

            if(1):  #是否用按键控制跳跃的高度
                tmp_key = 0.3
                if (kk.state(vk.ctrl)):
                    if (kk.state(kk.get_ord('w'))):
                        value += control_value
                        print(value)
                        sleep(tmp_key)
                if (kk.state(vk.ctrl)):
                    if (kk.state(kk.get_ord('s'))):
                        value -= control_value
                        print(value)
                        sleep(tmp_key)


            for addr_i in addr:
                data = dm.DoubleToData(value)
                dm.WriteData(self.hwnd, addr_i, data)
            sleep(sleep_t)



    def move_to_xyz(self,values=[0,0,0], T=3, sleep_t=0.001):
        #values = [0, 0, 0]; T = 3; sleep_t = 0.001
        print(values,'---', T, sleep_t)

        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break
            if(self.stop()):
                break

            #dict(zip(cd.addr_xyz,values))
            #cd.addrs
            # for addr,data in dict(zip(self.addr_xyz,values)) :
            #     for addr_i in addr:
            #         dm.WriteData(self.hwnd, addr_i, data)
            #         #print(addr_i,data)

            import numpy as np

            array_xyz = np.array(cd.addr_xyz)
            # for i in range(array_xyz.shape[1]):
            #     #for j in range(array_xyz.shape[0]):
            #     for addr,data in enumerate(dict(zip(array_xyz[:,i],values))):
            #         print(addr,data)
            #     print()
            for i in range(array_xyz.shape[1]):
                #for j in range(array_xyz.shape[0]):
                for addr,data in enumerate(dict(zip(array_xyz[:,i],values))):
                    dm.WriteData(self.hwnd, addr, data)



            # for addr_i,data in enumerate( dict(zip(cd.addr_xyz,values)) ):
            #     print(addr_i,data)
            # for addr in self.addr_xyz :
            #     for addr_i,data in dict(zip(addr,values)):
            #         dm.WriteData(self.hwnd, addr_i, data)

            sleep(sleep_t)
        return 1

    def move_to_xyz_slowly(self,values=[0,0,0], T=3, sleep_t=0.001):
        #values = [0, 0, 0]; T = 3; sleep_t = 0.001
        print(values,'---', T, sleep_t)

        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break
            if(self.stop()):
                break

            #dict(zip(cd.addr_xyz,values))
            #cd.addrs
            # for addr,data in dict(zip(self.addr_xyz,values)) :
            #     for addr_i in addr:
            #         dm.WriteData(self.hwnd, addr_i, data)
            #         #print(addr_i,data)

            import numpy as np

            array_xyz = np.array(cd.addr_xyz)
            # for i in range(array_xyz.shape[1]):
            #     #for j in range(array_xyz.shape[0]):
            #     for addr,data in enumerate(dict(zip(array_xyz[:,i],values))):
            #         print(addr,data)
            #     print()
            for i in range(array_xyz.shape[1]):
                #for j in range(array_xyz.shape[0]):
                array_xyz_i = array_xyz[:,i]
                #values_ = array_xyz_i

                for addr,data in enumerate( dict(zip(array_xyz_i, values)) ):

                    dm.WriteData(self.hwnd, addr, data)



            # for addr_i,data in enumerate( dict(zip(cd.addr_xyz,values)) ):
            #     print(addr_i,data)
            # for addr in self.addr_xyz :
            #     for addr_i,data in dict(zip(addr,values)):
            #         dm.WriteData(self.hwnd, addr_i, data)

            sleep(sleep_t)
        return 1

    def print_xyz(self,T=10, sleep_t=0.1):
        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break
            if (self.stop()):
                break

            self.get_xyz()

            import numpy as np
            self.xyz = np.array([self.x,self.y,self.z])
            print(self.xyz)

            sleep(sleep_t)

        return

    def x_pp(self, addr, tmp=0.01, T=5, value=[-100, 100], sleep_t=0.01):
        hwnd = self.hwnd

        tt = Time()
        while (1):
            if (tt.exceed(T)):
                break
            if (dm.stop_0()):
                break

            data0 = -100
            for addr_i in addr:
                data_init = dm.ReadDouble(hwnd, addr_i)
                data = data_init + tmp
                # print(data)
                # if (data0 - data == 0):
                #     return 1
                data0 = data

                if (data < value[0]):
                    data = value[0]
                if (data > value[1]):
                    data = value[1]

                data_ = dm.DoubleToData(data)
                dm.WriteData(hwnd, addr_i, data_)

            sleep(sleep_t)
        return 0
    1
cd = Change_data()

#调试
if(0):  # 调试用
    cd = Change_data()

    cd.get_hwnd()   # 得到窗口句柄
    cd.get_addrs()  # 根据特征码+偏移，定位地址
    cd.get_xyz()    # 得到人物xyz坐标的地址和数据

    cd.jump(cd.addr_z, value = 10, T=60, sleep_t=0.1, control_value=0.5)        # 重点功能-按键调整高度，高度10，只适用于生化金字塔

    # data = dm.DoubleToData(value)
    # dm.WriteData(hwnd, addr_i, data)

    # #其它功能
    # #cd.run_func(cd.addr_z,2,5,0.01)
    # cd.x_pp(cd.addr_z+cd.addr_x,tmp= -0.01,T = 5,sleep_t = 0., value = [-1,1])
    # cd.x_pp(cd.addr_z+cd.addr_y, tmp=0.001, T=10, sleep_t=0., value=[-1, 1])
    # #
    # #ctrl+w 向上飞，ctrl+s 向下飞
    #
    # def get_xyz_list(xx):
    #     return [xx[0][0],xx[1][0],xx[2][0]]
    # xyz = get_xyz_list(cd.get_xyz())
    # xyz
    #
    #
    # cd.run_func(cd.addr_z,15,10,0.1)
    #
    # #cd.stop()pp
    # cd.move_to_xyz(xyz,T = 5,sleep_t=0.)
    # cd.x_pp(cd.addr_z+cd.addr_y,tmp= 0.1,T = 5,sleep_t = 0., value = [-1,1])
    # #cd.move_to_xyz([])
    # cd.x_pp(cd.addr_z+cd.addr_x,tmp= 0.01,T = 10,sleep_t = 0.001, value = [-1,1])

#UI界面
if(1):
    import tkinter as tk
    from tkinter import messagebox

    window = tk.Tk()
    window.title('my window')
    # 窗口位置
    if (1):
        sw = window.winfo_screenwidth()  # 得到屏幕宽度
        sh = window.winfo_screenheight()  # 得到屏幕高度
        ww = 300
        wh = 300
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        window.geometry("%dx%d+%d+%d" % (ww, wh, x+500, y-300))

    #设置多线程
    if(1):
        import threading


        def thread_it(func, *args):
            '''将函数打包进线程'''
            # 创建
            t = threading.Thread(target=func, args=args)
            # 守护 !!!
            t.setDaemon(True)
            # 启动
            t.start()
            # 阻塞--卡死界面！
            # t.join()

    # 初始化按钮
    if (1):
        var = tk.StringVar()
        text_variable = tk.StringVar()
        text_variable.set('初始化')

        cd = Change_data()
        # on_hit = False

        def set_entry_var(value = -1):
            cd.get_xyz()
            cd.z
            if(len(cd.z)>1):
                print('多个内存，懒得完善了...')
            v1 = round(cd.xyz[value][0],2)
            v_entry.set(v1)
            return v1

        def regist():
            ###
            global  test_variable
            text_variable.set('运行中...')
            if(cd.get_hwnd() == 0):
                messagebox.showinfo(title='Default!', message='没有找到游戏窗口！')
                text_variable.set('重新初始化')
                return 0

            cd.get_addrs()  ####

            if( len(cd.addrs[0]) == 0 ):

                messagebox.showinfo(title='Default!', message='没有找到内存地址！')
                text_variable.set('重新初始化')

                return 0
            else:
                messagebox.showinfo(title='Success!', message='初始化成功~\n耗时：{}秒'.format(cd.cost_time))
                text_variable.set('再次初始化')
                # ---------- 要改变的参数默认为 addr_z!
                #set_entry_var()
                cd.get_xyz()
                return 1


        #tk.Button(window, text='音乐', command=thread_it(begin))
        # b = tk.Button(window, text='hit me', width=15, height=2, command=hit_me)
        # b.pack()
        #text = '初始化'

        tk.Button(window, textvariable = text_variable, width=15, height=2, command=lambda :thread_it(regist)).place(x=100, y=10)

    # 运行参数文本框输入 数值调整按钮
    if(1):
        # tk.Button(window, text='挂机次数： ', width = 10, height = 2, command=hit_me).place(x=20,y=110)
        x_1 = 50
        y_1 = 70
        #tk.Label(window, text='当前高度： ', font=('Arial', 12), width=15, height=2).place(x=x_1, y=y_1)
        tk.Button(window, text='当前高度:',  width=12, height=1, command=set_entry_var).place(x=x_1, y=y_1)
        v_entry = tk.IntVar()

        v1 = 10.0
        v_entry.set(v1)

        e = tk.Entry(window, width=6, textvariable=v_entry)
        e.place(x=150, y=y_1+10)
        #tk.Label(window, text='次', font=('Arial', 12), width=2, height=2, anchor='center').place(x=140, y=y_1)

        tmp_ = 1
        def add():
            global v_entry, v1, tmp_
            v1 = float(e.get())
            v1 += tmp_
            v_entry.set(v1)


        def substract():
            global v_entry, v1, tmp_
            v1 = float(e.get())
            v1 -= tmp_
            v_entry.set(v1)
        def refresh_entry():
            set_entry_var()

        tk.Button(window, text='+', width=3, height=1, command=add).place(x=205, y=y_1)
        tk.Button(window, text='-', width=3, height=1, command=substract).place(x=235, y=y_1)

    # 开始运行按钮
    if (1):
        y_2 = 120

        buttom_start = tk.StringVar()

        bottom_start_var ='开启高跳模式'
        buttom_start.set(bottom_start_var)

        def begin(type_begin = 0):
            global v_entry, v1
            #addr, value, T, delay = cd.addr_z, 3, 3, 0.001
            get_entry_var()

            v1 = float(v_entry.get())
            v1

            value = v1

            addr_split = entry_addr.entry.get().split(',')
            #addr_split = '0,1,2'.split(',')


            if(len(addr_split)>1):
                s = []
                for i in addr_split:
                    s += cd.addr_xyz[int(i)]
                addr = s
                #addr = [cd.addr_xyz[int(i)] for i in addr_split ]
            else:   addr = cd.addr_xyz[int(entry_addr.var)]

            addr = cd.addr_xyz[int(entry_addr.var)]
            T = float(entry_T.var)
            delay = float(entry_delay.var)

            # addr,value,Time,delay
            if(type_begin == 0):
                #cd.run_func(addr,value,T, delay)
                #tmp = float(entry_tmp.var)


                cd.jump(addr, value=value, T=120, sleep_t=delay, control_value=0.5)



                bottom_start_var = 'Alt+t 停止高跳'
                buttom_start.set(bottom_start_var)
                #cd.get_xyz()
                #13 0.1
                #[-6.435324668884277], [17.992692947387695], [10.913740988820805]

            else:
                tmp = float(entry_tmp.var)
                cd.x_pp(addr,tmp = tmp,T = T,value = [-100,100],sleep_t = delay)

            print('----------End!---------')


            #cd.x_pp(cd.addr_x + cd.addr_y + cd.addr_z, 0.01, T=4, sleep_t=0.)


        #tk.Button(window, text='Time', width=3, height=1, command=substract).place(x=235, y=y_1)
        #tk.Button(window, text='Time', width=3, height=1, command=substract).place(x=235, y=y_1)


        #tk.Button(window, text='刷新', width=5, height=1, command=set_entry_var).place(x=225, y=y_2-20)
        tk.Button(window, textvariable = buttom_start,width=15, height=2, command=lambda :thread_it(begin)).place(x=100, y=y_2)
        y_3 = y_2 + 50

        # addr,value,Time,delay
        addr = 3.0
        T = 5
        delay = 0.01
        #entry_addr,entry_T,entry_delay = tk.Entry(window, width=5, textvariable=v_entry),tk.Entry(window, width=5, textvariable=v_entry)tk.Entry(window, width=5, textvariable=v_entry)
        class Entry_:
            def __init__(self,var):
                #self.name = name
                self.var = var

                self.var_tk = tk.DoubleVar()
                self.var_tk.set(self.var)
                self.entry = tk.Entry(window, width=5, textvariable=self.var_tk)

            def get_var(self):
                try:
                    self.var = round(float(self.entry.get()),2)
                except:
                    self.var = self.entry.get()
                self.var_tk = tk.DoubleVar()
                self.var_tk.set(self.var)
                return self.var

            1

        entry_addr = Entry_(2)
        entry_T = Entry_(10)
        entry_delay = Entry_(0.1)
        entry_tmp = Entry_(0.01)

        entry_unit =  50 #像素宽度
        entry_addr.entry.place(x = 10+entry_unit*0, y = y_3)
        entry_T.entry.place(x=10+entry_unit*1, y=y_3)
        entry_delay.entry.place(x=10+ entry_unit*2, y=y_3)
        entry_tmp.entry.place(x=10 + entry_unit * 3, y=y_3)

        #entry_addr.get_var()
        def get_entry_var():
            entry_addr.get_var()
            entry_T.get_var()
            entry_delay.get_var()
            print('xyz：{}，时间：{}s,间隔：{}s'.format(entry_addr.var,entry_T.var,entry_delay.var))

        tk.Button(window, text='Test', width=8, height=1, command=lambda :thread_it(begin)).place(x=10+entry_unit*4, y=y_3)

        # 标签控件，显示文本和位图，展示在第一行
        # Label(tk, text="First").grid(row=0)
        # Label(tk, text="Second").grid(row=1)  # 第二行
        # Entry(tk).grid(row=0, column=1)

        # var2 = tk.DoubleVar()
        # v2 = 1.23
        # var2.set(v2)
        # def begin():
        #     global var2,v2
        #     v2 += 1
        #     var2.set(v2)
        #     pass
        # tk.Button(window,  textvariable = var2, width = 15, height = 2, command= begin).place(x = 100,y = y_2)
    # 注意事项
    Readme = '''
    若运行无效，则需重新初始化！
    Ctrl+w和Ctrl+s调整跳跃高度,
    Alt+t停止运行!
    参数：方向xyz,Time,delay,temp
    '''
    tk.Label(window, text=Readme, bg='green', font=('Arial', 12), width=30, height=5).place(x=10, y=202)

    window.mainloop()