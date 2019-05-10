# -*-coding:utf-8-*-
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-12
# @brief  calculate pck 
# @usage  python calculate_pck.py -ig [input_ground_truth_pickle_labels] -ip [input_predicted_pickle_labels] -o [output_pck]

import argparse
import numpy as np
import glob
import pickle
from scipy.spatial import distance
import matplotlib.pyplot as plt

def calculate_pck(input_gt, input_p, output_pck):

	'''
	1. load ground-truth labels and predicted labels
	'''
	with open (input_gt, 'rb') as fp:
		gt = pickle.load(fp)
	with open (input_p, 'rb') as fp:
		pre = pickle.load(fp)

	mean = 0
	c = 0
	dist_list = []

	'''
	2. calculate the joint distance for each frame
	'''
	for i, f in enumerate(pre):

		pre_label = pre[i][0]
		gt_label = gt[i][0]

		if not pre_label[1] == None:
			print("frame :"+str(pre_label[0]))

			c = c+1

			pre_x = np.asarray(pre_label[2])
			pre_y = np.asarray(pre_label[1])

			gt_x  = np.asarray(gt_label[1])
			gt_y  = np.asarray(gt_label[2])

			print(gt_x)
			print(gt_y)

			print(pre_x)
			print(pre_y)

			'''
			2.1. calculate the distance for each joint
			'''
			avg_dst = 0
			for j in range(1,21):
				# if j >1: # ignore the joint 0 and 1
				dst = distance.euclidean((pre_x[j], pre_y[j]), (gt_x[j], gt_y[j]))
				avg_dst = avg_dst + dst

			avg_dst = avg_dst / 19
			dist_list.append(avg_dst)	
			print("dist: "+ str(avg_dst))
			print("----------")

			mean = mean + int(avg_dst)
	mean = mean / c
	
	print(dist_list)
	print("avg. error: "+str(mean)+"pixels")
	dist_list = np.array(dist_list)
	sorted_list = sorted(dist_list)


	pck_at_10 = 364*0.1
	pck_at_15 = 364*0.15
	pck_at_20 = 364*0.2

	print(sorted_list)
	print(pck_at_10)
	print(pck_at_20)
	print(len(sorted_list))
	c_pck_at_10 = 0
	c_pck_at_15 = 0
	c_pck_at_20 = 0

	for j, val in enumerate(sorted_list):
		if val > pck_at_10:
			c_pck_at_10 = j
			break
	print("pck@10: "+str(c_pck_at_10/len(sorted_list)))

	for j, val in enumerate(sorted_list):
		if val > pck_at_15:
			c_pck_at_15 = j
			break
	print("pck@15: "+str(c_pck_at_15/len(sorted_list)))
	
	for j, val in enumerate(sorted_list):
		if val > pck_at_20:
			c_pck_at_20 = j
			break
	print("pck@20: "+str(c_pck_at_20/len(sorted_list)))


	# calculate PCK
	PCK_list = []
	c = 0
	for j in np.arange(1, len(sorted_list), len(sorted_list)/100) :
		PCK_list.append(sorted_list[c])
		c = c +1

	PCK_list = list(map(lambda i: (i), PCK_list))

	ratio_list = np.arange(0,1, 0.01)
	# print(ratio_list)
	plt.rcParams.update({'font.size': 15})
	plt.plot(PCK_list, ratio_list, '-b', label = "CPM", linewidth=3)
	plt.grid()
	plt.xlabel("threshold (px)")
	plt.ylabel("PCK")
 
	# plt.xlim(30, 34)
	plt.ylim(0, 1)
	plt.legend()
	plt.savefig("/Users/shihyaolin/Desktop/img.png")


	print("number of frames: "+str(len(pre)))

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_gt_pickle", "-ig", type=str, default = None)
	parser.add_argument("--input_predicted_pickle", "-ip", type=str, default = None)
	parser.add_argument("--output_pck", "-o", type=str, default = " ")
	args = parser.parse_args()

	print("input groud truth labels: "+args.input_gt_pickle)
	print("input predicted labels: "+args.input_predicted_pickle)
	print("output pck results: "+args.output_pck)

	calculate_pck(args.input_gt_pickle, args.input_predicted_pickle, args.output_pck)
