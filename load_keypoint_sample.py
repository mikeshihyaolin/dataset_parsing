# -*-coding:utf-8-*-
# @author Shih-Yao (Mike) Lin
# @email  shihyaolin@tencent.com
# @date   2019-04-08
# @brief  crop hands and save the cropped results and the new keypoint labels.
# @usage  python load_keypoint_sample.py -i [input_file_path] 

import subprocess
import os
import sys
from os import listdir, makedirs
import shutil
from os.path import isfile, isdir, join
import argparse
import numpy as np
import cv2
import glob
import pickle

def load_keypoint(input_file_path):
	with open (input_file_path, 'rb') as fp:
		data = pickle.load(fp)

	for i, f in enumerate(data):
		print("frame " + str(f[0][0]))
		print("x: " + str(f[0][1]))
		print("y: " + str(f[0][2]))
		print("-------")

	print("number of frames: "+str(len(data)))

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_file_path", "-i", type=str, default = None)
	args = parser.parse_args()

	print("input path: "+args.input_file_path)

	load_keypoint(args.input_file_path)
