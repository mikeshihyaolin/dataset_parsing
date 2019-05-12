# -*-coding:utf-8-*-
# @file   save_hand_pose.py
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-08
# @brief  generate bash for data pre-processing
# @usage  python script_pre-processing.py -i [dataset_path] -o [output_path] 
# @example  python script_pre-processing.py -i ../multiview_hand_pose_dataset_release/ -o ../data/  
# @dataset  http://www.rovit.ua.es/dataset/mhpdataset/#explore
#

import subprocess
import os
import sys
from os import listdir, makedirs
import shutil
from os.path import isfile, isdir, join
import time
import argparse
import glob

def reset(reset_path):
    path = reset_path
    if os.path.isdir(path):
        shutil.rmtree(path)
        makedirs(path)
        print("create folder: "+path)
    else:
        makedirs(path)
        print("create foder: "+path)

def create_bash_4_preprocessing(input_path, output_path):
    reset(output_path)
    f_shell = open("_bash4preprocessing.sh",'w')

    nb_view = 4
    nb_data = 21

    for i in range(nb_data):
        for j in range(nb_view):
            args = "python3 ./pre-processing.py -i "+input_path+"/ -o "+output_path+ " -d "+str(i+1)+" -v "+str(j+1)+"\n"
            args2 = "echo "+output_path+ "/data_"+str(i+1)+"/"+str(j+1)+"/ is done \n"

            f_shell.write(args)
            f_shell.write(args2)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", "-i", type=str)
    parser.add_argument("--output_path","-o", type=str)
    args = parser.parse_args()
    print(args)
    print(args.input_path)
    print(args.output_path)

    create_bash_4_preprocessing(args.input_path, args.output_path)
