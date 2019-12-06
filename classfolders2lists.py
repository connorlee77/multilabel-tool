import os
import glob
import numpy as np 
import pandas as pd 

import shutil
import tqdm

### CHANGE DATA PATH (FOLDERS FOR CLASSIFICATION) ###
DATA_PATH = 'data'
### CHANGE EXTENSION HERE ###
IMAGE_EXTENSION = 'jfif'
### NO MORE CHANGES! ###


IMAGE_DIR = 'images'
LABEL_DIR = 'labels'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
if not os.path.exists(LABEL_DIR):
    os.makedirs(LABEL_DIR)

folders = [directory for directory in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH,directory))]

dataset = {}
with open('class_mapping.txt', 'w') as class_mapping:
	for i, folder in enumerate(tqdm.tqdm(folders)):

		# Add class to mapping
		print(i, folder, file=class_mapping)
		
		folder_path = os.path.join(DATA_PATH, folder)
		files = os.listdir(folder_path)
		for f in files:
			if f in dataset:
				# Have seen image previously. Image has already been copied. 
				dataset[f].append(i)
			else:
				# First time we see image. Copy it to images directory. 
				dataset[f] = [i]
				src_img = os.path.join(folder_path, f)
				dst_img = os.path.join(IMAGE_DIR, f)
				shutil.copyfile(src_img, dst_img)
		
print(dataset)
# Create labels
for file in tqdm.tqdm(dataset):
	txt_file_name = file.replace(IMAGE_EXTENSION, 'txt')
	label_dst = os.path.join(LABEL_DIR, txt_file_name)
	labels = np.asarray(dataset[file]).astype(dtype=int)
	np.savetxt(label_dst, labels, fmt='%i')

