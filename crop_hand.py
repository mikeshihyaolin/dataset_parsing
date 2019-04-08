# -*-coding:utf-8-*-
# @file   save_hand_pose.py
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-07
# @brief  parse the data of ``Large-scale Multiview 3D Hand Pose Dataset" and save the plotted hand keypoint images
# @usage  python crop_hand.py -i [input_file_path] -v [camera_veiw] -o [output_img_path] // crop hand by using bbox   
# @dataset  http://www.rovit.ua.es/dataset/mhpdataset/#explore

import subprocess
import os
import sys
from os import listdir, makedirs
import shutil
from os.path import isfile, isdir, join
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import numpy as np
import cv2
import glob

def reset(reset_path):
    path = reset_path
    if os.path.isdir(path):
        shutil.rmtree(path)
        makedirs(path)
    else:
        makedirs(path)

def crop_hand(input_file_path, camera_view, output_img_path):

	reset(output_img_path+"/"+camera_view+"/")
	file_list= sorted(glob.glob(input_file_path+"*_bbox_"+camera_view+".txt"))
	img_list = sorted(glob.glob(input_file_path+"*_webcam_"+camera_view+".jpg"))

	for j, _ in enumerate(img_list):
		bbox = []
		f = open(file_list[j],'r')
		f = f.readlines()
		for i, fi in enumerate(f):
			f_line = fi.split(" ")
			bbox.append(int(f_line[1]))

		print(file_list[j])
		print(bbox)

		# find the new bbox width
		new_width = int(max(bbox[2]-bbox[0], bbox[3]-bbox[1])/2)
		center = [int((bbox[2]-bbox[0])/2+bbox[0]), int((bbox[3]-bbox[1])/2+bbox[1])]
		print(center)
		print(new_width)
		new_bbox = [center[0]-new_width, center[1]-new_width, center[0]+new_width, center[1]+new_width]
		print(new_bbox)
		print("-------------------")

		if img_list[j] != None:
			img = cv2.imread(img_list[j])

		name = img_list[j][len(input_file_path):]
		name = name.split("_")
		out_path = str(output_img_path+"/"+camera_view+"/%04d_"%int(name[0])+".jpg")
		# cv2.imwrite(out_path, img[bbox[0]:bbox[2],bbox[1]:bbox[3]])
		cv2.imwrite(out_path, img[new_bbox[0]:new_bbox[2],new_bbox[1]:new_bbox[3]])


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file_path", "-i", type=str, default = None)
	parser.add_argument("--camera_veiw", "-v", type=str, default = None)
	parser.add_argument("--output_img_path", "-o", type=str, default= "")
	args = parser.parse_args()

	print("input path: "+args.input_file_path)
	print("output path: "+args.output_img_path)

	crop_hand(args.input_file_path, args.camera_veiw, args.output_img_path)
