import pandas as pd
import numpy as np
d={'Age':pd.Series([20,27,38],index=['Devid','Chris','Chad']), 'Children':pd.Series([2,3,1,4],index=['Devid','Chris','Chad','Sham'])}
df=pd.DataFrame(d)
print(df)
print(df.apply(np.mean))
print(df['Age'].map(lambda x: x>20))
print(df.applymap(lambda x: x>20))