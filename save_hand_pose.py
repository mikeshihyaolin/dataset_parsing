# -*-coding:utf-8-*-
# @file   save_hand_pose.py
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-02
# @brief  parse the data of ``Large-scale Multiview 3D Hand Pose Dataset" and save the plotted hand keypoint images
# @usage  python save_hand_pose.py -i [input_file_path] -v [camera_veiw] -o [output_img_path] // save 2d parsed hand images  
# @usage  python save_hand_pose.py -i [input_file_path] -o [output_img_path] // save parsed 3d hand images  
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

bline_list = [[0,1],[0,2], [2,3], [5,4], [4,6], [6,7], [13,12], [12,14], [14,15], [9,8], [8,10], [10,11], [17,16], [16,18], [18,19], [17, 20], [20,1], [20,5], [20,13], [20,9]]
bone_list = np.array(bline_list) 

def reset(reset_path):
    path = reset_path
    if os.path.isdir(path):
        shutil.rmtree(path)
        makedirs(path)
    else:
        makedirs(path)

def save_2d_hand_pose(input_file_path, camera_view, output_img_path):

	reset(output_img_path+"/"+camera_view+"/")
	file_list= sorted(glob.glob(input_file_path+"*_jointsCam_"+camera_view+".txt"))
	img_list = sorted(glob.glob(input_file_path+"*_webcam_"+camera_view+".jpg"))
	# print(file_list)
	# print(img_list)
	
	for j, _ in enumerate(img_list):
		f = open(file_list[j],'r')
		f = f.readlines()
		x = []
		y = []

		for i, fi in enumerate(f):
			f_line = fi.split(" ")
			x.append(int(float(f_line[1])))
			y.append(int(float(f_line[2][:len(f_line[2])-1])))

		if img_list[j] != None:
			img = cv2.imread(img_list[j])
		else:
			img = np.zeros((480, 640, 3), np.uint8)

		for bone in bone_list:
			cv2.line(img, (x[bone[0]], y[bone[0]]), (x[bone[1]], y[bone[1]]), (255, 0, 0), 3)
		for i, _ in enumerate(x):
			cv2.circle(img, (x[i], y[i]), 7, (0, 255, 0), -1)
		
		name = img_list[j][len(input_file_path):]
		name = name.split("_")
		out_path = str(output_img_path+"/"+camera_view+"/%04d_"%int(name[0])+".jpg")
		cv2.imwrite(out_path, img)

def save_3d_hand_pose(input_file_path, output_img_path):

	reset(output_img_path+"/")
	file_list= sorted(glob.glob(input_file_path+"*_joints.txt"))

	for j, _ in enumerate(file_list):
		f = open(file_list[j],'r')

		f = f.readlines()
		x = []
		y = []
		z = []

		for i, fi in enumerate(f):
			f_line = fi.split(" ")
			# print(f_line)
			x.append(int(float(f_line[1])))
			y.append(int(float(f_line[2][:len(f_line[2])])))
			z.append(int(float(f_line[3][:len(f_line[3])-1])))
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		
		for bone in bone_list:
			ax.plot([x[bone[0]], x[bone[1]]],[y[bone[0]], y[bone[1]]], [z[bone[0]], z[bone[1]]], 'b')
		ax.scatter3D(x,y,z, c = 'g', s = 40)	
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')

		name = file_list[j][len(input_file_path):]
		name = name.split("_")
		# print(name)
		out_path = str(output_img_path+"/%04d_"%int(name[0])+".jpg")
		plt.savefig(out_path)
	plt.show()

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file_path", "-i", type=str, default = None)
	parser.add_argument("--camera_veiw", "-v", type=str, default = None)
	parser.add_argument("--output_img_path", "-o", type=str, default= "")
	args = parser.parse_args()

	print("input path: "+args.input_file_path)
	print("output path: "+args.output_img_path)
	
	if  args.camera_veiw != None:
		save_2d_hand_pose(args.input_file_path, args.camera_veiw, args.output_img_path)
	else:
		save_3d_hand_pose(args.input_file_path, args.output_img_path)



# def data_preprocessing(input_file_path, camera_view):
# 	file_list= sorted(glob.glob(input_file_path+"*_jointsCam_"+camera_view+".txt"))
# 	reset(input_file_path+"/processed_files/")

# 	for i, fi in enumerate(file_list):
# 		name = fi[len(input_file_path):]
# 		name = name.split("_")
# 		print(name)

# 		with open(input_file_path+"/processed_files/"+"%04d"%int(name[0])+name[1]+".txt", 'a') as fo:
# 			for line in open(fi):
# 				if '\n' in line:
# 					fo.write(line)