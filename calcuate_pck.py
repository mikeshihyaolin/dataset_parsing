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

	# for i, f in enumerate(gt):
		# print("frame " + str(f[0][0]))
		# print("x: " + str(f[0][1]))
		# print("y: " + str(f[0][2]))
		# print("-------")

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
			for j in range(21):
				if j >1: # ignore the joint 0 and 1
					dst = distance.euclidean([pre_x[j], pre_y[j]], [gt_x[j], gt_y[j]])

					# dst = np.sqrt(np.sum((pre_x[j]- gt_x[j])**2) +  np.sum((pre_y[j]- gt_y[j])**2))
					# dst = distance.euclidean([1, 0, 0], [0, 1, 0])
					avg_dst = avg_dst + dst

			avg_dst = int(avg_dst / 20	)	
			dist_list.append(avg_dst)	
			print("dist: "+ str(avg_dst))
			print("----------")

			mean = mean + int(avg_dst)
	mean = mean / c
	
	print(dist_list)
	print("avg. error: "+str(mean)+"pixels")
	dist_list = np.array(dist_list)
	# print(dist_list)
	num_bins = 100
	n, bins, patches = plt.hist(dist_list, num_bins, facecolor='blue')
	plt.xlabel('error (pixel)')
	plt.ylabel('number')
	plt.title(r'Histogram of finger erros')
	plt.savefig('HIST.png')

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
