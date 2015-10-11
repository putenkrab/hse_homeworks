#Mukhomorova Olga
from itertools import product
import numpy as np

def isDiagZero(x):
    for i in range(0,5):
        if x[i,i]!=0:
            return False
    return True

def isAssimetric(x):
    for i in range(0,5):
        for j in range(0,5):
            if x[i,j]+x[j,i]==2:
                return False
    return True

def isTrasitive(x):
    for i in range(0,5): #row
        for j in range(0,5):#column
            if x[i,j]==1:
                for k in range(0,5):#second row
                    if x[j,k]==1 and x[i,k]!=1:
                        return False
    return True


x = np.empty((5,5), dtype=int)

count=0
for i in product([0,1], repeat=25):
    x.flat[:] = i
    if isDiagZero(x):
        if isAssimetric(x):
            if isTrasitive(x):
                count+=1
    #print x

print count
