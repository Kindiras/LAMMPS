"""This code converts the lammps out file and makes into the simpler .json format and next it does calculate the sublimation rate
of dimer for AMD"""

import pandas as pd
import numpy as np
import math
import json
import yaml
import os
import shutil
import math
from mpmath import mp
import sys
from glob import glob
import statistics as st

def fileload(filename):
    with open(filename,"rt") as f:
      data = [[i for i in line.split()] for line in f.readlines()]
    return data

def check_sublimation(data,r):#This checks whether there is sublimation and if there is then check if it isdimer or monomer
    t=0
    dimer_sub=0
    mono_sub=0
    no_sub=0
    for i in range(0,len(data)-10):
        if(int(len(data[t])>=10)):
            if(str(data[t][1])=='ATOMS'):
                if(int(len(data[t+1])>=5)):
                    if(str(data[t+1][1]).isdigit()):
                        if(str(data[t+2][1]).isdigit()):
                            dimer_sub=1
                            #print("yes")
                        else:
                            mono_sub=1
                else:
                    no_sub=1
        t=t+1
    return dimer_sub,mono_sub,no_sub


def window_dimer_info(data,runs):
    MDtime = []
    z1 = [];z2 = []; zcm = []; v2x = []; v1x = [];v2y = []; v1y = [];v2z = []; v1z = []
    vxcm=[];vycm=[];vzcm=[];V=[];theta=[]
    t=0
    p=0
    for i in range(0,len(data)-10):
        if(int(len(data[t])>=10)):
            if(str(data[t][1])=='ATOMS'):
                if(int(len(data[t+1])>=5)):
                    if(str(data[t+1][1]).isdigit()):
                        if(str(data[t+2][1]).isdigit()): #Record info if Zcm is within the window.
                            if(runs==5):
                                nt=int(data[t-7][0])+8000000
                                MDtime.append(nt)

                            elif(runs==4):
                                nt=int(data[t-7][0])+6000000
                                MDtime.append(nt)


                            elif(runs==3):
                                nt=int(data[t-7][0])+4000000
                                MDtime.append(nt)

                            elif(runs==2):
                                nt=int(data[t-7][0])+2000000
                                MDtime.append(nt)

                            elif(runs==1):
                                MDtime.append(int(data[t-7][0]))

                            else:
                                print("something went wrong check:")    

                            z1.append(data[t+1][4])
                            z2.append(data[t+2][4])
                            zcm.append((float(z1[p])+float(z2[p]))/2)
                            v1x.append(data[t+1][5])
                            v2x.append(data[t+2][5])
                            vxcm.append((float(v1x[p])+float(v2x[p]))/2)
                            v1y.append(data[t+1][6])
                            v2y.append(data[t+2][6])
                            vycm.append((float(v1y[p])+float(v2y[p]))/2)
                            v1z.append(data[t+1][7])
                            v2z.append(data[t+2][7])
                            vzcm.append((float(v1z[p])+float(v2z[p]))/2)
                            V.append(np.sqrt((vxcm[p])**2+(vycm[p])**2+(vzcm[p])**2))
                            theta.append(round(np.degrees(math.acos(vzcm[p]/V[p])),2))
                            p=p+1
        t=t+1   

    return MDtime,zcm,vzcm,theta

def conf_MDsteps_PE_info(dataconf1,dataconf2,dataconf3,dataconf4,dataconf5,runs):
    PE = []
    MDsteps = []
    AtomsNum =[]
    steps = 0
    if(runs>=1):
        a = 0
        for i in range(0,len(dataconf1)):
            if(int(len(dataconf1[a])!=0)):
                if(dataconf1[a][0]=='Step'):
                    for s in range(1,200001):
                            PE.append(dataconf1[a+s][7])
                            MDsteps.append(dataconf1[a+s][0])
                            AtomsNum.append(dataconf1[a+s][2])
                                    
            a=a+1  

    if(runs>=2):
        na=0
        for j in range(0,len(dataconf2)):
            if(int(len(dataconf2[na])!=0)):
                if(dataconf2[na][0]=='Step'):
                    for ns in range(1,200002):
                        PE.append(dataconf2[na+ns][7])
                        steps = int(dataconf2[na+ns][0])+2000000
                        MDsteps.append(steps)
                        AtomsNum.append(dataconf2[na+ns][2])
            na=na+1      

    if(runs>=3):
        nna=0
        for k in range(0,len(dataconf3)):
            if(int(len(dataconf3[nna])!=0)):
                if(dataconf3[nna][0]=='Step'):
                    for nns in range(1,200002):
                        PE.append(dataconf3[nna+nns][7])
                        steps = int(dataconf3[nna+nns][0])+4000000
                        MDsteps.append(steps)
                        AtomsNum.append(dataconf3[nna+nns][2])
            nna=nna+1 

    if(runs>=4):
        nnna=0
        for l in range(0,len(dataconf4)):
            if(int(len(dataconf4[nnna])!=0)):
                if(dataconf4[nnna][0]=='Step'):
                    for nnns in range(1,200002):
                        PE.append(dataconf4[nnna+nnns][7])
                        steps = int(dataconf4[nnna+nnns][0])+6000000
                        MDsteps.append(steps)
                        AtomsNum.append(dataconf4[nnna+nnns][2])
            nnna=nnna+1      

    if(runs>=5):
        nnnna=0
        for m in range(0,len(dataconf5)):
            if(int(len(dataconf5[nnnna])!=0)):
                if(dataconf5[nnnna][0]=='Step'):
                    for nnnns in range(1,200002):
                        PE.append(dataconf5[nnnna+nnnns][7])
                        steps = int(dataconf5[nnnna+nnnns][0])+8000000
                        MDsteps.append(steps)
                        AtomsNum.append(dataconf5[nnnna+nnnns][2])
            nnnna=nnnna+1      


    return MDsteps,PE,AtomsNum             
 

def fileload_json(filename):
    """
    Load a json or specs file, determined by the extension.
    """

    with open(filename, 'r') as f:
        if filename.endswith('.json'):
            file_dict = json.load(f)
        elif filename.endswith('.yaml'):
            file_dict = yaml.load(f)
    return file_dict



def filedump(dict_to_file, filename):
    """
    Dump a json or specs file, determined by the extension. Indentation of json
    and flow style of yaml is set.
    """

    with open(filename, 'w') as f:
        if filename.endswith('.json'):
            json.dump(dict_to_file, f, indent=4)
        elif filename.endswith('.yaml'):
            yaml.dump(dict_to_file, f, default_flow_style=False)

def listing_params(PEinfo,wdinfo):
    params={}
    params['MDsteps'] = PEinfo[0]
    params['PE']=PEinfo[1]
    params['MDsteps-sublimation'] = wdinfo[0]
    params['Zcm'] = wdinfo[1]
    params['Vzcm'] = wdinfo[2]
    params['theta'] = wdinfo[3]
    return params

def listing_reqired_cal(PEinfo,wdinfo):
    md=[]
    pot=[]
    subtime=[]
    vzcm=[]
    vzcm.append(wdinfo[2][0]) #storeing first value
    subtime.append(wdinfo[0][0])#storing first value
    for (i,j,k) in zip(PEinfo[0],PEinfo[1],PEinfo[2]):
        if(int(k) >= 2400):
            md.append(i)
            pot.append(j)
        else:
            print("atom is lost after MDsteps:",i) 
            break           
    return md,pot,subtime,vzcm

def get_params_cal(paramscal):
    Cparams= {}
    Cparams['MDsteps'] = paramscal[0]
    Cparams['PE'] = paramscal[1]
    Cparams['MDsteps-sublimation']=paramscal[2]
    Cparams['Vzcm'] = paramscal[3]
    return Cparams

def window_data_frame(dimer_subA,mono_subA,no_subA):
    params={}
    params['dimer_sub'] = dimer_subA
    params['mono_sub'] = mono_subA
    params['no_sub'] = no_subA
    return params     


def get_window_time(hw,b,params):
    """LAMMPS prints data in every 10 steps and time step is 0.001 ps. 1ps=>1000 stpes and it will be in 100the row in the data****1MD steps=>0.001ps***"""
    tau_old = 0; tau_in=0;tau_out=0;steps_b =0;steps_b1=0;steps_times=0
    """LAMMPS start detecting dimer if the lower atom is above 24.7 A from the top layer of bulk surface of CdTe plus 1A"""
    tau_old = params['MDsteps-sublimation'][0] #This is the MD time step when dimer enter the bottom of window
    print("MD steps when dimer reaches bottom of window:",tau_old)
    v_cm = round(params['Vzcm'][0],3) # it gets the z velocities of center of mass when the dimer enters the window
    print("Vcm:",v_cm)
    ws=abs(hw) #this is the shifting of the window height from 24.7 A
    shift_window = int(1000*ws/v_cm) # MD steps by which new window is shifted
    if(shift_window%10>=5):
        shift_window=shift_window - shift_window%10+10 
    else:
        shift_window=shift_window - shift_window%10
    print("MD steps of window shift:",shift_window)
    if(hw<0):
        tau_in = tau_old-shift_window #negative when the window is lowered by certain height of original height.
    else:
        tau_in = tau_old+shift_window #This is the time when the dimer hits the bottomw of new window
             
    steps_b1 = int(1000*0.1/v_cm) #this is just to avoid numerical inconsitency 
    if(steps_b1%10>=5):
        steps_b1=steps_b1 - steps_b1%10+10 
    else:
        steps_b1=steps_b1 - steps_b1%10 
    steps_times = round(b/0.1) #it helps in rounding the values not to have any numerical incosistency 

    steps_b = steps_times*steps_b1#it gives the MD steps within the window of width b
    print("small steps:",steps_b1,"window size in MD steps:",steps_b,"steps_time:",steps_times,"for b:",b)    
    tau_out= tau_in+steps_b #This is the MD step when the dimer leaves the window divid it by 10 gives array position
    print("MD steps when dimer eneters the bottom of window (tau_in):",tau_in,"& when it leaves the window (tau_out):",tau_out)
    return tau_in, tau_out,v_cm        

def get_avginvWR_window(params,tau_in,tau_out,s,PE_min):
    print("mini PE to substract for easy exponential calculation:", PE_min)
    iapos = int(tau_in/10) #initial position of potential in row when dimer enters the window
    fapos = int(tau_out/10)
    AvginvWR=0
    invWRA = []
    suminvWR = 0
    KB = 8.617*10**(-5)
    T = 1000
    dp=0  
    delpe=0
    for j in range(iapos,fapos+1):
        delpe=float(params['PE'][j]) + float(PE_min)# to make the exponential small for the size we are using
        invWR = mp.exp((-delpe*(s-1))/(s*KB*T))
        invWRA.append(invWR)
        dp=dp+1 #how  many data points we have
    for k in range(dp):
        suminvWR = suminvWR+invWRA[k] 
        #print(suminvWR)
    AvginvWR = suminvWR
    #print("windosum:",AvginvWR)
    return AvginvWR    

def get_avginvWR_config(params,tau_in,s,dcor_time,PE_min):
    print("mini PE to substract for easy exponential calculation:", PE_min)
    """dcor_time is given in ps. 0.001x10ps =>1 in row of data"""
    fapos = int(tau_in/10)
    iapos=int(100*dcor_time) #this gives the position in row.
    AvgconfinvWR = 0
    confinvWRA = []
    sumconfinvWR = 0
    KB = 8.617*10**(-5)
    T = 1000
    dp=0
    delpe=0 
    print("decorrelation time (ps):",0.001*int(params['MDsteps'][iapos]))
    for i in range(iapos,fapos+1):#this gives the summing after decorrelation time to bottom of the window
        delpe=float(params['PE'][i]) + float(PE_min)
        invWR = mp.exp((-delpe*(s-1))/(s*KB*T))
        confinvWRA.append(invWR)
        dp=dp+1 #how  many data points we have
    for j in range(dp):
        sumconfinvWR = (sumconfinvWR)+(confinvWRA[j])     
    AvgconfinvWR = (sumconfinvWR) 
    return AvgconfinvWR
    
    
def get_constant_factor():
    KB = 8.617*10**(-5)
    T = 1000.0
    pi = 3.141592653589793
    m = 4.23779496*10**(-25)
    vel=10**10*((KB*T*1.60218*10**(-19))/(2*pi*m))**0.5 #This value we get in the unit of Angstrom/sec
    const = vel #Angstrom/s
    return const

def get_KTST(const,num_b,Denwow,Denww):
    """sum the numerator of all 100 runs and divide it by the denominaotr of each runs gives the best result"""
    ktstww = const*num_b/Denww #ksts with window in the denominator
    ktstwow = const*num_b/Denwow #ktst without window in the denominator
    return ktstww,ktstwow      

def get_sublimation_act_time(tau_out,dcor_time):
    tsub_ps = tau_out*0.001 - dcor_time
    return tsub_ps # it returns the time of sublimation in ps


def write_time_rate(filename,rate):
    with open(filename,'w') as tr:
        tr.write("The actual average time rate in per second is :")
        tr.write("\t")
        tr.write("\t")
        tr.write(str(rate))
        tr.write("\n")

def write_info(filename,s,b,ktstww,ktstwow):
    with open(filename,'w') as ft:
        #ft.write("s")
        ft.write("s")
        ft.write("\t")
        ft.write("b")
        ft.write("\t")
        ft.write("KTST(N/(N+D))")
        ft.write("\t")
        ft.write("KTST(N/D)")
        ft.write("\n")
        for i in range(len(b)):
            ft.write(str(s[i]))
            ft.write("\t")
            ft.write(str(b[i]))
            ft.write("\t")
            ft.write(str(round(ktstww[i],30)))
            ft.write("\t")
            ft.write(str(round(ktstwow[i],30)))
            ft.write("\n")


