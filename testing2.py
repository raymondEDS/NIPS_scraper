import numpy as np
import pandas as pd
import math
# list of strings

 
# Calling DataFrame constructor on list
#df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6],"d": [4, 5, 6],"Ba": [4, 5, 6],"Bf": [4, 5, 6],"Bb": [4, 5, 6],"Bd": [4, 5, 6]})


df = pd.read_csv("nips_paper_reviews_2015.csv") 
print(len(df.keys()))

x = len(df.keys())
print(x)
for i in range(3,x):
    print(i)
    if i == x-1:
        print(df.keys()[i])
        df.rename(columns={df.keys()[i]:'Author Rebutal'},inplace=True)
    elif i%2 == 0:
        df.rename(columns={df.keys()[i]:"Reviewer " + str(math.floor((i-1)/2))+':Q2'},inplace=True)
    else:
        df.rename(columns={df.keys()[i]:"Reviewer " + str(math.floor(i/2))+':Q1'},inplace=True)

#df.rename(columns = {'A':'rename worked'},inplace=True)
print(df)
print(df.keys())