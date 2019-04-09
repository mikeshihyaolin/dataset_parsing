import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import numpy as np
import cv2


bline_list = [[0,1],[0,2], [2,3], [5,4], [4,6], [6,7], [13,12], [12,14], [14,15], [9,8], [8,10], [10,11], [17,16], [16,18], [18,19], [17, 20], [20,1], [20,5], [20,13], [20,9]]
bone_list = np.array(bline_list) 

def plot_2d_hand_pose(input_file_path, input_img_path):
	f = open(input_file_path,'r')
	f = f.readlines()
	x = []
	y = []

	for i, fi in enumerate(f):
		f_line = fi.split(" ")
		x.append(int(float(f_line[1])))
		y.append(int(float(f_line[2][:len(f_line[2])-1])))

	if input_img_path != None:
		img = cv2.imread(input_img_path)
	else:
		img = np.zeros((480, 640, 3), np.uint8)
		# img = np.zeros((1440, 1920, 3), np.uint8)
		img[:] = 255

	for bone in bone_list:
		cv2.line(img, (x[bone[0]], y[bone[0]]), (x[bone[1]], y[bone[1]]), (255, 0, 0), 3)
	for i, _ in enumerate(x):
		cv2.circle(img, (x[i], y[i]), 7, (0, 255, 0), -1)
		# cv2.imshow("img",img)
		# cv2.waitKey()
	cv2.imshow("img",img)
	cv2.waitKey()

def plot_3d_hand_pose(input_file_path):
	f = open(input_file_path,'r')
	f = f.readlines()
	x = []
	y = []
	z = []
	for i, fi in enumerate(f):
		print(f)
		f_line = fi.split(" ")
		x.append(int(float(f_line[1])))
		y.append(int(float(f_line[2][:len(f_line[2])])))
		z.append(int(float(f_line[3][:len(f_line[3])-1])))
	
	print(x)
	print(y)
	print(z)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	
	for bone in bone_list:
		print(bone)
		ax.plot([x[bone[0]], x[bone[1]]],[y[bone[0]], y[bone[1]]], [z[bone[0]], z[bone[1]]], 'b')
	ax.scatter3D(x,y,z)	
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	plt.show()

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file_path", "-i", type=str, default = None)
	parser.add_argument("--input_img_path", "-img", type=str, default = None)
	args = parser.parse_args()

	print("input path: "+args.input_file_path)

	if "Cam" in args.input_file_path:
		plot_2d_hand_pose(args.input_file_path, args.input_img_path)
	else:
		plot_3d_hand_pose(args.input_file_path)