# -*-coding:utf-8-*-
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-08
# @brief  crop hands and save the cropped results and the new keypoint labels.
# @usage  python pre-processing_.py -i [input_file_path] -o [output_file_path] -d [data_number] -v [camera_veiw]  
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

lm3d2opencv = [[16, 2], [18, 3], [19,4], [1,5], [0,6], [2,7], [3,8], [5,9], [4,10], [6,11], [7,12], [13,13], [12,14], [14,15], [15,16], [9,17], [8,18], [10,19], [11,20]]

bone_list_2 = [[2,3], [2,3], [3,4], [5,6], [6,7], [7,8], [9,10], [10,11], [11,12], [13,14], [14,15], [15,16], [17,18], [19,20]]
bone_list_2 = np.array(bone_list_2) 

def reset(reset_path):
    path = reset_path
    if os.path.isdir(path):
        shutil.rmtree(path)
        makedirs(path)
    else:
        makedirs(path)

def crop_hand(input_file_path, output_file_path, dataset_num, camera_view, crop_width):

	if not os.path.isdir(output_file_path):
		reset(output_file_path)
		reset(output_file_path+"/data_"+dataset_num)
		reset(output_file_path+"/rendered_data_"+dataset_num)
	else:
		if not os.path.isdir(output_file_path+"/data_"+dataset_num):
			reset(output_file_path+"/data_"+dataset_num)
			reset(output_file_path+"/rendered_data_"+dataset_num)


	reset(output_file_path+"/data_"+dataset_num+"/"+camera_view+"/")
	reset(output_file_path+"/rendered_data_"+dataset_num+"/"+camera_view+"/")

	file_list= sorted(glob.glob(input_file_path+"/data_"+dataset_num+"/*_bbox_"+camera_view+".txt"))
	joint_list=sorted(glob.glob(input_file_path+"/data_"+dataset_num+"/*_jointsCam_"+camera_view+".txt"))
	img_list = sorted(glob.glob(input_file_path+"/data_"+dataset_num+"/*_webcam_"+camera_view+".jpg"))

	print(input_file_path+"/data_"+dataset_num+"/"+camera_view+"/")
	print(file_list)

	crop_width = int(int(crop_width)/2)

	bbox_origin = []
	hand_keypoints = []

	for j, _ in enumerate(img_list):
		print(file_list[j])
		print(joint_list[j])

		# 1. load original bbox 
		bbox = []
		f = open(file_list[j],'r')
		f = f.readlines()
		for i, fi in enumerate(f):
			f_line = fi.split(" ")
			bbox.append(int(f_line[1]))

		# 2. calculate the center of the bbox
		center = [int((bbox[2]-bbox[0])/2+bbox[0]), int((bbox[3]-bbox[1])/2+bbox[1])]

		# 3. set the new bbox
		new_bbox = [center[0]-crop_width, center[1]-crop_width, center[0]+crop_width, center[1]+crop_width]

		# 4. load original images and crop hands
		if img_list[j] != None:
			img = cv2.imread(img_list[j])
			if new_bbox[0] < 0:			
				new_bbox[2] = new_bbox[2] - new_bbox[0]
				new_bbox[0] = 0

			if new_bbox[2] > 480:		
				new_bbox[0] = new_bbox[0] - (new_bbox[2] - 480)
				new_bbox[2] = 480


			if new_bbox[1] < 0:
				
				new_bbox[3] = new_bbox[3] - new_bbox[1]
				new_bbox[1] = 0

			if new_bbox[3] >= 640:
				
				new_bbox[1] = new_bbox[1] - (new_bbox[3] - 640)
				new_bbox[3] = 640

			name = img_list[j][len(input_file_path)+1:]
			name = name.split("_")
			if 26 == int(name[1][len(dataset_num)+1:]):
				print(new_bbox[2]-new_bbox[0])
				print(new_bbox[3]-new_bbox[1])

			crop_img = img[new_bbox[0]:new_bbox[2],new_bbox[1]:new_bbox[3]]
			
			if 26 == int(name[1][len(dataset_num)+1:]):
				print(new_bbox)
				print(crop_img.shape)

		
		out_path = str(output_file_path+"/data_"+dataset_num+"/"+camera_view+"/%04d_"%int(name[1][len(dataset_num)+1:])+".jpg")
		print(out_path)
		print("------------")
		cv2.imwrite(out_path, crop_img)

		# 5. record the bbox coordinate
		bbox_origin.append([new_bbox[1], new_bbox[0]])

		# 6. load hand keypoint
		x = []
		y = []
		fj = open(joint_list[j],'r')
		fj = fj.readlines()
		for i, f_val in enumerate(fj):
			f_line = f_val.split(" ")
			x.append(int(float(f_line[1]))-(new_bbox[1]))
			y.append(int(float(f_line[2][:len(f_line[2])-1]))-(new_bbox[0]))
		new_x = [0]*21
		new_y = [0]*21

		# 7. covert keypoint order via openpose's format
		for val in lm3d2opencv:
			new_x[val[1]] = x[val[0]]
			new_y[val[1]] = y[val[0]]

		hand_keypoints.append([[j, new_x, new_y]])

		# 8. write crop results
		for bone in bone_list_2:
			cv2.line(crop_img, (new_x[bone[0]], new_y[bone[0]]), (new_x[bone[1]], new_y[bone[1]]), (255, 0, 0), 3)
		for i, _ in enumerate(x):
			cv2.circle(crop_img, (new_x[i], new_y[i]), 7, (0, 255, 0), -1)

		out_path = str(output_file_path+"/rendered_data_"+dataset_num+"/"+camera_view+"/_%04d_"%int(name[1][len(dataset_num)+1:])+".jpg")
		cv2.imwrite(out_path, crop_img)

	# 9. save keypoint labels 
	import pickle
	out_name =  str(output_file_path+"/data_"+str(dataset_num)+"_"+str(camera_view)+"_bbox_origin.pkl")
	with open(out_name, 'wb') as fp:
		pickle.dump(bbox_origin, fp)
		print(out_name)

	out_name =  str(output_file_path+"/data_"+str(dataset_num)+"_"+str(camera_view)+"_hand_keypoints.pkl")
	with open(out_name, 'wb') as fp:
		pickle.dump(hand_keypoints, fp)
		print(out_name)

	print("-----------------")

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file_path", "-i", type=str, default = None)
	parser.add_argument("--output_file_path", "-o", type=str, default = None)
	parser.add_argument("--dataset_num", "-d", type=str, default = None)
	parser.add_argument("--camera_veiw", "-v", type=str, default = None)
	parser.add_argument("--crop_width",  "-cw", type=str, default= "368")
	args = parser.parse_args()

	print("input path: "+args.input_file_path)
	print("output path: "+args.output_file_path)
	print("dataset_num: "+args.dataset_num)
	print("camera_veiw path: "+args.camera_veiw)
	# print("crop width: "+args.crop_width)

	crop_hand(args.input_file_path, args.output_file_path, args.dataset_num, args.camera_veiw, args.crop_width)
