import json
import yaml
import pandas as pd
import numpy as np 
import math
from mpmath import mp
import sys
from glob import glob
import statistics as st

from CdTe_sublimation import fileload_json,get_constant_factor,get_window_time,get_avginvWR_window,get_avginvWR_config,get_KTST, \
    write_info,get_sublimation_act_time,write_time_rate


if __name__ == '__main__':
    #***********make file in run changes the following********
    dcor_time = 40 #decorrelation time in ps. 
    PE_min = 4600.00 #this is to make exponential calculation easy, it depends on the substrate size
    heigt_win_shift = 0
    bmin = 0.2 #minimum value to start b (window width)
    bmax = 2.0 # maximum value for b
    db = 0.02
    #***************don't change any of the following******************

    max_value = int(bmax/db)
    b = bmin
    s=1
    b_array=[]
    AvgktstwwA=[]
    AvgktstwowA =[]
    s_array=[]

    const=get_constant_factor()
    print("constant value (Ang/sec:",const)
    dir_list = glob("../*.json")
    
    for i in range(0,max_value):
        KTSTww_array=[]
        KTSTwow_array=[]
        tsub_array = []
        tot_tsub = 0 
        tot_ktstww=0
        tot_ktstwow=0
        print("Right now running for b:",b)

        for j in dir_list:
            fnum = int(j.replace("../Results-","").replace(".json",""))	
            params = fileload_json(j)
            print("file:",j)
            tau_in,tau_out,vz_cm = get_window_time(heigt_win_shift,b,params)
            if(s==1 and b == bmin):
                tsub_ps = get_sublimation_act_time(tau_out,dcor_time) #this gives the time of sublimation for each run in ps
                tsub_array.append(tsub_ps)    

            invWRw = get_avginvWR_window(params,tau_in,tau_out,s,PE_min)
            invWRc = get_avginvWR_config(params,tau_in,s,dcor_time,PE_min)

            Denww = invWRc+invWRw #Denominator with inclusion of numerator
            Denwow=invWRc#denominator without numerator
            num_b = invWRw/b #Numerator (window) value divided by b

            ktstww,ktstwow = get_KTST(const,num_b,Denwow,Denww)
            KTSTwow_array.append(ktstwow)
            KTSTww_array.append(ktstww)

        for q in range(len(KTSTww_array)):
            tot_ktstww = tot_ktstww + KTSTww_array[q]
            tot_ktstwow = tot_ktstwow + KTSTwow_array[q]

        if(s==1 and b == bmin):
            for t in range(len(tsub_array)):
                tot_tsub = tot_tsub + tsub_array[t]
            Avg_tsub = tot_tsub/len(tsub_array)
            rate = 10**12/Avg_tsub
            write_time_rate("actual_time_rate.dat",rate)
            print("Avg_MDsteps of sublimation:", rate)   
            
             
        Avg_ktstwow = tot_ktstwow/len(KTSTwow_array)    
        Avg_ktstww = tot_ktstww/len(KTSTww_array)
        print("s:",s,"b:",b,"AvgdenominatorwithoutN:",Avg_ktstww,"AvgdenominatorwithN:",Avg_ktstww)
        AvgktstwwA.append(Avg_ktstww)
        AvgktstwowA.append(Avg_ktstwow)
        b_array.append(b)
        s_array.append(s)
        b=b+db

    write_info('WH0AS1.dat',s_array,b_array,AvgktstwwA,AvgktstwowA)        




           




