# python3 python script_crop_hand.py -i ~/Documents/data/lm3d_hand_pose_dataset/multiview_hand_pose_dataset_release/ -o ~/Documents/data/mike
# @author shihyaolin(@tencent.com)
# @date   2019-04-08
# @brief  generate bash for crop hand
# python script_crop_hand.py -i ~/Documents/data/lm3d_hand_pose_dataset/multiview_hand_pose_dataset_release/ -o ~/Documents/data/mike


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
        # print("remove existing "+path)
        makedirs(path)
        print("create folder: "+path)
    else:
        makedirs(path)
        print("create foder: "+path)

def create_bash_4_hand_crop(input_path, output_path):

    reset(output_path)

    f_shell = open("_crop_hand.sh",'w')

    nb_view = 4
    nb_data = 21
    count = 0

    for i in range(nb_data):
        reset(output_path+"/data_"+str(i+1)+"/")
        for j in range(nb_view):
            reset(output_path+"/data_"+str(i+1)+"/"+str(j+1)+"/")
            count = count +1

            args = "python3 ./crop_hand.py -i "+input_path+"/data_"+str(i+1)+"/ -o "+output_path+ "/data_"+str(i+1)+"/ -v "+str(j+1)+"\n"
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

    create_bash_4_hand_crop(args.input_path, args.output_path)
