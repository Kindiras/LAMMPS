import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy.random as np

np.seed(111)


def CreateData(number=1):
    dataout=[]
    for i in range(number):
        rng=pd.date_range(start='1/1/2009',end='12/31/2012',freq='W-MON')
        #rng=pd.date_range(start='1/1/2009',end='12/31/2012',freq='A')
        data=np.randint(low=25,high=1000,size=len(rng))
        status=[1,2,3]
        random_status=[status[np.randint(low=0,high=len(status))] for i in range(len(rng))]   
        states=['GA','fl','NY','NJ','TX','OH'] 
        random_states=[states[np.randint(low=0,high=len(states))] for i in range(len(rng))]
        dataout.extend(zip(random_states,random_status,data,rng))
        return dataout

dataset=CreateData(3)
df=pd.DataFrame(data=dataset,index=None,columns=['States','Status','CustomerCount','StatusDate'])  
plt.plot(df['StatusDate'],df['CustomerCount'])
plt.show()
"""upper case"""

df['States']=df.States.apply(lambda x: x.upper())
#df['States']=df.States.apply(lambda x: x.lower())
sortdf = df[df['States']=='NY'].sort_index(axis=0)
df.to_excel('lesson3.xlsx',index=False)
df.info()