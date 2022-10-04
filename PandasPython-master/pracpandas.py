import pandas as pd 
import matplotlib.pyplot as plt 
import os
import random
"""Creating thd data sets"""
names = ['Devid','Sham','Shiva','Krishna','Ram']
ages = [25,38,70,100,200]
"""merging these data"""
nameages=list(zip(names,ages))
print(nameages)
"""in the form of excel spreadsheet"""
df=pd.DataFrame(nameages,columns={'Names','Ages'})
print(df)
"""Export to csv files"""
df.to_csv("nameage.csv",index=False, header=False)
"""remove the .csv file"""
os.remove("nameage.csv")
"""Lesson-2"""
random_names=[]
random_names.append([names[random.randint(0,len(names)-1)]for i in range(100)])
print(random_names)
births=[random.randint(0,200) for i in range(100)]
print(births)
albirthsnames=list(zip(random_names,births))
print(albirthsnames)
df=pd.DataFrame(albirthsnames,columns={'Names','Ages'})
print(df)
#df.to_csv("births.csv")