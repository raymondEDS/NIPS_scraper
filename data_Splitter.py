import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os


def split_train_dev_test(filename):
    #will take input file and split into train,test,dev based on the peerRead distributions
    df = pd.read_csv(filename)
    dir_name = 'dataset_'+filename
    if os.path.isfile(dir_name):
        os.makedirs(dir_name)
        train , validtest = train_test_split(df, test_size=0.1, random_state = 42)
        dev,test = train_test_split(validtest, test_size=0.5, random_state = 42)
        datasets = [train,dev,test]
        dataset_names = ['train','dev','test']

        for split, set_name in zip(datasets,dataset_names):
            split.to_csv(dir_name + '/'+set_name+'_'+filename,index = False)
    else:
        print('folder exists')

# df1 = pd.DataFrame(np.arange(1,20))
# df3 = pd.DataFrame(np.arange(1,20))
# df4 = pd.DataFrame(np.arange(1,20))

# list1 = [df1,df3,df4]
# list2 = ['d','b','c']
# for dataf, b in list1, list2:
#     print(type(dataf))
#     print(str(df1))
#     print(b)

filename= "nips_paper_reviews_2016.csv"
split_train_dev_test(filename)
