# #####################################################################################################################
# Project UNDYNE - GUI
# #####################################################################################################################

import tkinter as tk
import time
import ttk
import socket
import sys
import threading
import multiprocessing as mp

def ceasecomms():
    #s.sendall(disconnect.encode('utf-8'))
    #s.close()
    root.destroy()



def motordata(motordemand, piddemand):
    # send a message to tell UNDYNE what to do with the data
    #s.sendall(codeword2.encode('utf-8'))
    # Construct message to be sent
    #print(motordemand)
    #message = "%s'%s'%s'%s'" % (motordemand[0], motordemand[1], motordemand[2], motordemand[3])
    message = "%s'%s'%s'%s'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f'%0.2f' ACK" % (motordemand[0], motordemand[1], motordemand[2], motordemand[3],piddemand[0], piddemand[1],piddemand[2],piddemand[3],piddemand[4],piddemand[5],piddemand[6],piddemand[7],piddemand[8],piddemand[9],piddemand[10],piddemand[11], piddemand[12], piddemand[13])
    #message +=message2
    #print(message)
    #s.sendall(message.encode('utf-8'))

    message = ""
    while (message[-4:] != " ACK"):
        message += s.recv(16).decode('utf-8')


    return message

def currentdata():
    #s.sendall(codeword.encode('utf-8'))
    sensordata = ""
    while (sensordata[-4:] != " ACK"):
        sensordata += s.recv(16).decode('utf-8')
    #print(sensordata)
    return sensordata




class commandcentre(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.updatedata = 9
        self.demand = []
        self.pid = []
        self.pack()
        self.createwidets()


    def createwidets(self):
        self.topframe = tk.Frame(self)
        self.generallabel = tk.Label(self.topframe, text="")
        self.generallabel.pack(side="top")
        tk.Label(self.topframe, text="UNDYNE AUV COMMAND CENTER", font="ubuntu 13 bold").pack(side="top")
        tk.Label(self.topframe, text="").pack(side="top")

        self.frame1 = tk.Frame(self)
        ttk.Label(self.frame1, text="        Battery Voltage:  ").pack(side="left")
        self.batterynow = tk.StringVar()
        self.battery = ttk.Label(self.frame1, textvariable=self.batterynow).pack(side="left")
        ttk.Label(self.frame1, text="           Cell Voltage:  ").pack(side="left")
        self.cellnow = tk.StringVar()
        self.cell = ttk.Label(self.frame1, textvariable=self.cellnow).pack(side="left")
        ttk.Label(self.frame1, text="         System Temperature:  ").pack(side="left")
        self.tempnow = tk.StringVar()
        self.temp = ttk.Label(self.frame1, textvariable=self.tempnow).pack(side="left")

        self.frame2 = tk.Frame(self)
        self.generallabel2 = tk.Label(self.frame2, text="")
        self.generallabel2.pack(side="top")

        self.frame3 = tk.Frame(self)
        tk.Label(self.frame3, text="Desired Heading", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)
        tk.Label(self.frame3,  text="Heading", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)
        tk.Label(self.frame3, text="Desired Roll   ", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)
        tk.Label(self.frame3, text="Roll     ", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)
        tk.Label(self.frame3, text="Desired Pitch        ", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)
        tk.Label(self.frame3, text="Pitch    ", anchor=tk.CENTER, width=16).pack(side="left", fill="x",expand=True)

        self.frame4 = tk.Frame(self)
        self.h = tk.StringVar()
        self.h.set("0")
        ttk.Label(self.frame4, text=" ").pack(sid="left")
        self.h_desired = ttk.Entry(self.frame4, textvariable=self.h)
        self.h_desired.pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")
        self.euler_hnow = tk.StringVar()
        self.euler_h = ttk.Label(self.frame4, textvariable=self.euler_hnow, width=20, anchor=tk.CENTER).pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")

        self.r = tk.StringVar()
        self.r.set("0")
        self.r_desired = ttk.Entry(self.frame4, textvariable=self.r)
        self.r_desired.pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")
        self.euler_rnow = tk.StringVar()
        self.euler_r = ttk.Label(self.frame4, textvariable=self.euler_rnow, width=20, anchor=tk.CENTER).pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")

        self.p = tk.StringVar()
        self.p.set("0")
        self.p_desired = ttk.Entry(self.frame4, textvariable=self.p)
        self.p_desired.pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")
        self.euler_pnow = tk.StringVar()
        self.euler_p = tk.Label(self.frame4, textvariable=self.euler_pnow, width=20, anchor=tk.CENTER).pack(side="left")
        ttk.Label(self.frame4, text=" ").pack(sid="left")

        self.frame5 = ttk.Frame(self)
        tk.Label(self.frame5, text="Charge Level").pack(side="top")
        tk.Label(self.frame5, text="").pack(side="top")
        self.chargepercent = tk.IntVar()
        charge=ttk.Progressbar(self.frame5, orient="vertical", maximum=100 , variable=self.chargepercent).pack()

        self.frame6 = tk.Frame(self)
        self.frame7 = tk.Frame(self)
        ttk.Label(self.frame6, text="").pack(sid="top")
        tk.Label(self.frame6, text="MOTOR CONTROLS", font="ubuntu 13 bold").pack(side="top")
        ttk.Label(self.frame6, text="").pack(side="top")
        ttk.Label(self.frame6, text="Distance", anchor=tk.CENTER,width=8).pack(side="left", fill="x", expand=True)
        ttk.Label(self.frame6, text="Depth", anchor=tk.CENTER,width=8).pack(side="left", fill="x", expand=True)
        ttk.Label(self.frame6, text="RT", anchor=tk.CENTER,width=8).pack(side="left", fill="x", expand=True)
        ttk.Label(self.frame6, text="RD",anchor=tk.CENTER, width=8).pack(side="left", fill="x", expand=True)
        ttk.Label(self.frame6, text="LT",anchor=tk.CENTER ,width=8).pack(side="left", fill="x", expand=True)
        ttk.Label(self.frame6, text="LD",anchor=tk.CENTER ,width=8).pack(side="left", fill="x", expand=True)
        self.distanceset = tk.StringVar()
        self.distanceset.set("0")
        self.depthset = tk.StringVar()
        self.depthset.set("0")
        self.RTset = tk.StringVar()
        self.RTset.set("0")
        self.LTset = tk.StringVar()
        self.LTset.set("0")
        self.RDset = tk.StringVar()
        self.RDset.set("0")
        self.LDset = tk.StringVar()
        self.LDset.set("0")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.distance = ttk.Entry(self.frame7, textvariable=self.distanceset)
        self.distance.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.depth = ttk.Entry(self.frame7, textvariable=self.depthset)
        self.depth.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.RT = ttk.Entry(self.frame7, textvariable=self.RTset)
        self.RT.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.RD = ttk.Entry(self.frame7, textvariable=self.RDset)
        self.RD.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.LT = ttk.Entry(self.frame7, textvariable=self.LTset)
        self.LT.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.LD = ttk.Entry(self.frame7, textvariable=self.LDset)
        self.LD.pack(side="left")
        ttk.Label(self.frame7, text=" ").pack(sid="left")
        self.motorframe = tk.Frame(self)
        self.currentRT = tk.StringVar()
        self.currentRD = tk.StringVar()
        self.currentLT = tk.StringVar()
        self.currentLD = tk.StringVar()
        ttk.Label(self.motorframe, textvariable=self.currentRT).pack(side="left")
        ttk.Label(self.motorframe, textvariable=self.currentRD).pack(side="left")
        ttk.Label(self.motorframe, textvariable=self.currentLT).pack(side="left")
        ttk.Label(self.motorframe, textvariable=self.currentLD).pack(side="left")


        self.frame8 = tk.Frame(self)
        self.frame9 = tk.Frame(self)
        self.frame10 = tk.Frame(self)

        # PID for heading
        ttk.Label(self.frame8, text="").pack(side="top")
        ttk.Label(self.frame8, text="PID PARAMETER TUNING", font="ubuntu 13 bold").pack(side="top")
        ttk.Label(self.frame8, text="").pack(side="top")

        ttk.Label(self.frame8, text="HEADING: Kp", width=12).pack(side="left")
        self.kp_h = tk.StringVar()
        self.kp_h.set("1")
        self.KP_h = ttk.Entry(self.frame8, textvariable=self.kp_h)
        self.KP_h.pack(side="left")

        ttk.Label(self.frame8, text=" Ki ").pack(side="left")
        self.ki_h = tk.StringVar()
        self.ki_h.set("0")
        self.KI_h = ttk.Entry(self.frame8, textvariable=self.ki_h)
        self.KI_h.pack(side="left")

        ttk.Label(self.frame8, text=" Kd ").pack(side="left")
        self.kd_h = tk.StringVar()
        self.kd_h.set("0")
        self.KD_h = ttk.Entry(self.frame8, textvariable=self.kd_h)
        self.KD_h.pack(side="left")

        # PID control params for roll
        ttk.Label(self.frame9, text="ROLL:       Kp ", width=12).pack(side="left")
        self.kp_r = tk.StringVar()
        self.kp_r.set("1")
        self.KP_r = ttk.Entry(self.frame9, textvariable=self.kp_r)
        self.KP_r.pack(side="left")

        ttk.Label(self.frame9, text=" Ki ").pack(side="left")
        self.ki_r = tk.StringVar()
        self.ki_r.set("0")
        self.KI_r = ttk.Entry(self.frame9, textvariable=self.ki_r)
        self.KI_r.pack(side="left")

        ttk.Label(self.frame9, text=" Kd ").pack(side="left")
        self.kd_r = tk.StringVar()
        self.kd_r.set("0")
        self.KD_r = ttk.Entry(self.frame9, textvariable=self.kd_r)
        self.KD_r.pack(side="left")

        # Boxes for setting PID control params for pitch
        ttk.Label(self.frame10, text="PITCH:      Kp ", width=12).pack(side="left")
        self.kp_p = tk.StringVar()
        self.kp_p.set("1")
        self.KP_p = ttk.Entry(self.frame10, textvariable=self.kp_p)
        self.KP_p.pack(side="left")

        ttk.Label(self.frame10, text=" Ki ").pack(side="left")
        self.ki_p = tk.StringVar()
        self.ki_p.set("0")
        self.KI_p = ttk.Entry(self.frame10, textvariable=self.ki_p)
        self.KI_p.pack(side="left")

        ttk.Label(self.frame10, text=" Kd ").pack(side="left")
        self.kd_p = tk.StringVar()
        self.kd_p.set("0")
        self.KD_p = ttk.Entry(self.frame10, textvariable=self.kd_p)
        self.KD_p.pack(side="left")

        self.frame11 = ttk.Frame(self)
        # Boxes for setting PID control params for depth
        ttk.Label(self.frame11, text="DEPTH:      Kp ", width=12).pack(side="left")
        self.kp_d = tk.StringVar()
        self.kp_d.set("1")
        self.KP_d = ttk.Entry(self.frame11, textvariable=self.kp_p)
        self.KP_d.pack(side="left")

        ttk.Label(self.frame11, text=" Ki ").pack(side="left")
        self.ki_d = tk.StringVar()
        self.ki_d.set("0")
        self.KI_d = ttk.Entry(self.frame11, textvariable=self.ki_p)
        self.KI_d.pack(side="left")

        ttk.Label(self.frame11, text=" Kd ").pack(side="left")
        self.kd_d = tk.StringVar()
        self.kd_d.set("0")
        self.KD_d = ttk.Entry(self.frame11, textvariable=self.kd_p)
        self.KD_d.pack(side="left")

        self.emergency = ttk.Button(self.frame5, text="Emergency Surface", command=self.surface)
        self.fullforward = ttk.Button(self.frame5,text="Full Forward Throttle", command=self.forwardtrottle)
        self.fullreverse = ttk.Button(self.frame5,text="Full Reverse Throttle", command=self.reversetrottle)
        self.steadydive = ttk.Button(self.frame5, text="Steady Dive", command=self.dive)
        tk.Label(self.frame5, text="").pack(side="top")
        tk.Label(self.frame5, text="").pack(side="top")
        self.emergency.pack(side="top", fill="x")
        self.fullforward.pack(side="top", fill="x")
        self.fullreverse.pack(side="top", fill="x")
        self.steadydive.pack(side="top", fill="x")

        self.exit = ttk.Button(self, text="End Session", command=ceasecomms)
        self.exit.pack(side="bottom")
        tk.Label(self, text="").pack(side="bottom")

        self.topframe.pack(side="top")
        self.frame5.pack(side="right")
        self.frame1.pack(side="top", fill="x")
        self.frame2.pack(side="top")
        self.frame3.pack(side="top", fill="x")
        self.frame4.pack(side="top")
        self.frame6.pack(side="top", fill="x")
        self.frame7.pack(side="top", fill="x")
        self.motorframe.pack(side="top")
        self.frame8.pack(side="top")
        self.frame9.pack(side="top")
        self.frame10.pack(side="top")
        self.frame11.pack(side="top")
        #threading._start_new_thread(self.setdata, ())
        #self.setdata()


    def setdata(self):

        RT = self.RT.get()
        if not self.RT.get(): RT = 0
        RD = self.RD.get()
        if not self.RD.get(): RD = 0
        LT = self.LT.get()
        if not self.LT.get(): LT = 0
        LD = self.LD.get()
        if not self.LD.get(): LD = 0
        self.demand = [int(RT), int(RD), int(LT), int(LD)]

        setpoint_h = self.h_desired.get()
        if not self.h_desired.get(): setpoint_h = 0
        setpoint_r = self.r_desired.get()
        if not self.r_desired.get(): setpoint_r = 0
        setpoint_p = self.p_desired.get()
        if not self.p_desired.get(): setpoint_p = 0
        setpoint_dph = self.depth.get()
        if not self.depth.get(): setpoint_dph = 0
        setpoint_s = self.distance.get()
        if not self.distance.get(): setpoint_s = 0
        kp_h = self.KP_h.get()
        if not self.KP_h.get(): kp_h = 1
        ki_h = self.KI_h.get()
        if not self.KI_h.get(): ki_h = 0
        kd_h = self.KD_h.get()
        if not self.KD_h.get(): kd_h = 0
        kp_r = self.KP_r.get()
        if not self.KP_r.get(): kp_r = 1
        ki_r = self.KI_r.get()
        if not self.KI_r.get(): ki_r = 0
        kd_r = self.KD_r.get()
        if not self.KD_r.get(): kd_r = 0
        kp_p = self.KP_p.get()
        if not self.KP_p.get(): kp_p = 1
        ki_p = self.KI_p.get()
        if not self.KI_p.get(): ki_p = 0
        kd_p = self.KD_p.get()
        if not self.KI_p.get(): ki_p = 0
        self.pid =  [float(setpoint_h), float(setpoint_r), float(setpoint_p), float(setpoint_dph), float(setpoint_s),float(kp_h), float(ki_h), float(kd_h), float(kp_r), float(ki_r), float(kd_r), float(kp_p), float(ki_p), float(kd_p)]

        values = currentdata()
        self.demand = motordata(self.demand, self.pid)
        #print(demand)
        #print(values)

        self.updatedata += 1
        if self.updatedata == 10:
            self.updatedata = 0
            values = values.split("'")
            self.demand = self.demand.split("'")[:4]

            self.currentRT.set(self.demand[0])
            self.currentRD.set(self.demand[1])
            self.currentLT.set(self.demand[2])
            self.currentLD.set(self.demand[3])
            self.batterynow.set(values[0])
            self.cellnow.set(values[1])
            self.tempnow.set(values[2])
            self.euler_hnow.set(values[3])
            self.euler_rnow.set(values[4])
            self.euler_pnow.set(values[5])
            self.batterypercent = (float(values[1]) - 3.5)/0.007
            self.chargepercent.set(self.batterypercent)

        self.after(200, self.setdata)


    def forwardtrottle(self):
        self.RT.delete(0, 'end')
        self.LT.delete(0, 'end')
        self.RD.delete(0, 'end')
        self.LD.delete(0, 'end')
        self.RT.insert(0, "100")
        self.LT.insert(0, "100")

    def reversetrottle(self):
        self.RT.delete(0, 'end')
        self.LT.delete(0, 'end')
        self.RD.delete(0, 'end')
        self.LD.delete(0, 'end')
        self.RT.insert(0, "-100")
        self.LT.insert(0, "-100")

    def surface(self):
        self.RT.delete(0, 'end')
        self.LT.delete(0, 'end')
        self.RD.delete(0, 'end')
        self.LD.delete(0, 'end')
        self.RD.insert(0, "100")
        self.LD.insert(0, "100")
        self.RT.insert(0, "0")
        self.LT.insert(0, "0")

    def dive(self):
        self.RT.delete(0, 'end')
        self.LT.delete(0, 'end')
        self.RD.delete(0, 'end')
        self.LD.delete(0, 'end')
        self.RD.insert(0, "-75")
        self.LD.insert(0, "-75")
        self.RT.insert(0, "75")
        self.LT.insert(0, "75")

    def stahp(self):
        self.RT.delete(0, 'end')
        self.LT.delete(0, 'end')
        self.RD.delete(0, 'end')
        self.LD.delete(0, 'end')
        self.RD.insert(0, "0")
        self.LD.insert(0, "0")
        self.RT.insert(0, "0")
        self.LT.insert(0, "0")

    # implement a button with recommended PID params
    #def pidtuned(self):

if __name__ == '__main__':
    #s = socket.socket()
    #address = ('192.168.0.41', 666)
    #print("Awaiting connection, to UDYNE...")
    #s.connect(address)

    codeword = "SD ACK"
    codeword2 = "MD ACK"
    disconnect = "DC ACK"


    root = tk.Tk()
    root.title("UNDYNE Command Center")
    root.iconbitmap('icon.ico')

    #root.minsize(width=750, height=800)
    root.option_add('*font', ('ubuntu', 11))
    app = commandcentre(master=root)


    """
    # some data
    data = StringVar()
    setdata(data)
    
    # Heading, Pitch, Yaw
    euler = Frame()
    eulervalue = Frame()
    eulerdesired = Frame()
    
    heading = IntVar()
    pitch = IntVar()
    yaw = IntVar()
    
    
    
    
    
    Label(euler,text="Heading",width=8).pack(side=LEFT,  padx = (190,0), pady= 10)
    Label(euler,text="Pitch",width= 8).pack(side=LEFT,  padx = (10,0), pady=10)
    Label(euler,text="Yaw",width=8).pack(side=LEFT,  padx = 10, pady=10)
    Label(eulervalue, textvariable= heading,width=8).pack(side=LEFT,  padx = (190,0), pady=10)
    Label(eulervalue, textvariable= pitch,width=8).pack(side=LEFT,  padx = (10,0), pady=10)
    Label(eulervalue, textvariable= yaw,width=8).pack(side=LEFT,  padx = 10, pady=10)
    Label(eulerdesired, text="Desired Euler Angles").pack(side=LEFT,  padx = 10, pady=10)
    
    
    d_heading = Entry(eulerdesired ,width=8)
    d_heading.insert(0,"0")
    d_heading.pack(side=LEFT,  padx = 10, pady=10)
    d_pitch = Entry(eulerdesired ,width=8)
    d_pitch.insert(0,"0")
    d_pitch.pack(side=LEFT,  padx = 10, pady=10)
    d_yaw = Entry(eulerdesired ,width=8)
    d_yaw .insert(0,"0")
    d_yaw .pack(side=LEFT,  padx = 10, pady=10)
    #d_heading = Entry(eulerdesired ,width=8).pack(side=LEFT,  padx = 10, pady=10)
    #d_pitch = Entry(eulerdesired,width=8).pack(side=LEFT,  padx = 10, pady=10)
    #d_yaw = Entry(eulerdesired, width=8).pack(side=LEFT,  padx = 10, pady=10)
    #d_heading.insert(0,"1")
    
    
    
    
    
    
    
    euler.pack(side=TOP)
    eulervalue.pack(side=TOP)
    eulerdesired.pack(side=TOP)
    """

    root.mainloop()


