import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import numpy as np
import cv2
import pickle


bline_list = [[0,1],[0,2], [2,3], [5,4], [4,6], [6,7], [13,12], [12,14], [14,15], [9,8], [8,10], [10,11], [17,16], [16,18], [18,19], [17, 20], [20,1], [20,5], [20,13], [20,9]]
bone_list = np.array(bline_list) 

def plot_2d_hand_pose(input_pkl_path, input_img_path):
	with open (input_pkl_path, 'rb') as fp:
		labels = pickle.load(fp)
	
	print(labels)

	label = labels[1][0]
	y = label[1]
	x = label[2]
	print(label)

	img = cv2.imread(input_img_path)
	print(img.shape)

	for i, _ in enumerate(x):
		cv2.circle(img, (x[i], y[i]), 5, (0, 0, 255), -1)

	# cv2.imshow("img",img)
	# cv2.waitKey()
		cv2.imwrite("/Users/shihyaolin/Desktop/joints_cpm/%03d.jpg"%i, img)


path_pkl = "/Users/shihyaolin/Documents/data/lm3d_cpm/cpm/res_keypoint_1_3.pkl" 
img_path = "/Users/shihyaolin/Documents/data/lm3d_processed_data/rendered_data_1/3/_0001_.jpg"
# img_path = "/Users/shihyaolin/Documents/data/lm3d_cpm/cpm/res_1/1/00000.jpg"


# path_pkl = "/Users/shihyaolin/Desktop/res_keypoint_1_3.pkl" 

# img_path = "/Users/shihyaolin/Desktop/res_1/1/00000.jpg"


plot_2d_hand_pose(path_pkl,img_path)



