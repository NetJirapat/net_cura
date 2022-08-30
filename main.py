import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 


a = open('./dog-2.5H.text')
x = []
y = []
z = []
h = 0 
for i in a:
    if 'G92 E0' in i :
        h += 0.5
        print(h)
    if 'X' in i and 'Y' in i :
        text = i.split(' ')
#         y_f = float()
        x_t  = text[1][1:-1].strip("'")
        y_t = text[2][1:-1].strip("'")
#         if x_t.isdigit():  
        try:
            x.append(float(x_t))
            y.append(float(y_t))
            z.append(h)
        except:
            pass
   
df = pd.DataFrame()

df['X'] = x
df['Y'] = y 
df['Z'] = z

ax = plt.axes(projection='3d')
ax.plot3D(df['X'][:], df['Y'][:], df['Z'][:])
plt.show()
        


