import pandas as pd 
import os 


# Make initial declarations 
data_folder = r"C:\ic22_Team22022\Data\Data_NOSLs\Summaries by Region and year"


# Go thorugh every folder found in 'Data'

for folder in os.listdir(data_folder):

	# Data about this specific folder 
	region 		= folder[:-2]
	movement 	= folder[-2:]
	folder_dir	= data_folder + "\\" + folder
	
	for filename in os.listdir(folder_dir):

		# Ignore the region summaries 
		if "RegionSummary" in filename: continue 

		# Get file information 
		year		= filename[5:9]
		filepath 	= folder_dir + "\\" + filename 


