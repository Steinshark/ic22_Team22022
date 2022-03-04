import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt
import json

port_to_region = {	'ACCO' : 'NA',
					'ANNA' : 'NA',
					'JRLO' : 'NA',
					'JRUP' : 'NA',
					'NPOT' : 'NA',
					'OXFO' : 'NA'}

regions = ["NA","GB","AFR","IRE",'NEU',"SEU","WI"]

def write_data():
	# We are in 
	data_dir =  "D:\\classes\\si470\\ic22\\data"



	# Go through all regional directories 
	global_data = {}



	for location_dir in os.listdir(data_dir):
		csv = open(f'{location_dir}.csv','w')
		csv.write('year,good,value,movement_type\n')
		# Add to global_data 
		movement_type = location_dir[-2:]
		port = location_dir[:4]
		cwd = os.path.join(data_dir,location_dir)	

		for year_csv in os.listdir(cwd):

			# Add to global_data 
			filename = os.path.join(cwd,year_csv)
			if 'RegionSummary' in year_csv:
				continue
			year = year_csv[6:10]
			if not "RegionSummary" in year_csv:

				with open(filename) as file:
					for i in range(4): file.readline()
					for line in file.readlines()[:-2]:
						item_list = line.strip().split(",")
						good = item_list[0].replace('"','')
						value = item_list[-1]
						csv.write(f"{year},{good},{value},{movement_type}\n")
		csv.close()
		data_table = pd.read_csv(f'{location_dir}.csv')
		data_table = data_table.pivot_table(index="year",columns='good',values='value')
		data_table.fillna(0,inplace=True)
		data_table.to_csv(f"{location_dir}_pivot.csv")

def aggregate_datae():


	# get all headers
	header = []
	main_df = pd.DataFrame()

	for file in os.listdir():

		if not "pivot" in file:
			continue 

		port = file[:4]
		this_df = pd.read_csv(file)
		this_df['PORT'] = [port for i in range(len(this_df[list(this_df.keys())[0]]))]

		main_df = pd.concat([main_df,this_df],ignore_index=0)


	main_df.loc[:,~(main_df==0.0).all(axis=0)]
	main_df.loc[:,~(main_df==float('nan')).all(axis=0)]

	keys = list(main_df.keys())
	keys.sort()
	keys.remove('PORT')
	keys.remove('year')
	keys.insert(0,'PORT')
	keys.insert(0,'year')
	main_df = main_df[keys]
	print(main_df)


def write_all():
	# We are in 
	data_dir =  "D:\\classes\\si470\\ic22\\data"



	# Go through all regional directories 
	global_data = {}
	movements = {'EN': {}, 'CL' : {}}

	raw = []

	for location_dir in os.listdir(data_dir):
		# Add to global_data 
		movement_type = location_dir[-2:]

		port = location_dir[:4]
		cwd = os.path.join(data_dir,location_dir)	
		movements[movement_type][port] = {}

		for year_csv in os.listdir(cwd):
			# Add to global_data 
			filename = os.path.join(cwd,year_csv)
			if 'RegionSummary' in year_csv:
				continue
			year = year_csv[6:10]
			movements[movement_type][port][year] = {}
			if not "RegionSummary" in year_csv:

				with open(filename) as file:
					headers = file.readline().split(",")

					for i in range(3): file.readline()
					for line in file.readlines()[:-2]:
						item_list = line.strip().split(",")
						good = item_list[0].replace('"','')

						total_value = item_list[-1]
						unit = item_list[1]	

						regions_represented = [x.strip() for x in regions if x.strip() in headers]

						region_indices = {r : headers.index(r) for r in regions_represented}

						deliveries = [{'destination' : r, 'amount' : item_list[region_indices[r]]} for r in region_indices]

						info = {}
						info['unit'] = unit
						info['total_value'] = total_value
						info['good'] = good 
						info['year'] = year
						info['direction'] = movement_type
						info['origin'] = port
						for d in deliveries:
							for i in info:
								d[i] = info[i]

						raw.append({'movement_type':movement_type, 'port' : port,'year':year,'good':good,'total_value':total_value})
	a = json.dumps(raw)
	open("dataDUMP",'w').write(a)

#write_data()
#data_table = pd.read_csv('full_data.csv')

write_all()
