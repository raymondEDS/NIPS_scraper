import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os


def split_train_dev_test(filename):
    #will take input file and split into train,test,dev based on the peerRead distributions
    df = pd.read_csv(filename)
    dir_name = 'dataset_'+filename
    folder_exists = os.path.isdir(dir_name)
    if not folder_exists:
        os.makedirs(dir_name)
        train , validtest = train_test_split(df, test_size=0.1, random_state = 42)
        dev,test = train_test_split(validtest, test_size=0.5, random_state = 42)
        datasets = [train,dev,test]
        dataset_names = ['train','dev','test']

        for split, set_name in zip(datasets,dataset_names):
            split.to_csv(dir_name + '/'+set_name+'_'+filename,index = False)
    else:
        print('folder exists')

filename= "nips_paper_reviews_2016.csv"
split_train_dev_test(filename)
