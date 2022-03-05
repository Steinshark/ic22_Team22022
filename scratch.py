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

dump = "dataDUMP"

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
	data_dir =  "data"



	# Go through all regional directories 
	global_data = {}
	movements = {'EN': {}, 'CL' : {}}

	raw = []

	for location_dir in os.listdir(data_dir):
		# Add to global_data 
		movement_type = location_dir[-2:]

		port = location_dir[:4]
		cwd = os.path.join(data_dir,location_dir)	

		if not len(location_dir) == 6:
			continue
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

							raw.append(d)
	a = json.dumps(raw)
	open("dataDUMP",'w').write(a)



def plot_grains():
	text_dump = open(dump,'r').read()

	transaction_list = json.loads(text_dump)

	# Find all headers 
	goods = {}
	for t in transaction_list:
		if not t['good'] in goods:
			this_good = t['good']
			this_good_o = t['origin']
			goods[this_good] = {'count':0, 'origin':[]}
			goods[this_good]['count'] = 1
			goods[this_good]['origin'] = [t['origin']]

		else:
			goods[this_good]['count'] += 1
			if not t['origin'] in goods[this_good]['origin']:
				goods[this_good]['origin'].append(t['origin'])

	
	entering_ann = {}
	leaving_ann	= {}

	looking_for = ["Corn","Wheat","Oats ","Flour and bread","Flour and biscuit","Flax ","Bread and flour","Flour",'RegionSummary']




	for t in transaction_list:
		if t['origin'] == 'ANNA' and t['good'] in looking_for:

			good = t['good']
			year = t['year']
			val = float(t['total_value'])
			direction = t['direction']


			if t['direction'] == 'EN':

				if good in entering_ann:
					entering_ann[good].append({'year':year,'val':val})
				else:
					entering_ann[good] = [{'year':year,'val':val}]

			elif t['direction'] == 'CL':
				if good in leaving_ann:
					leaving_ann[good].append({'year':year,'val':val})
				else:
					leaving_ann[good] = [{'year':year,'val':val}]



	fig,ax = plt.subplots(2)					
	for good in entering_ann:
		ax[0].plot([i['year'] for i in entering_ann[good]],[i['val'] for i in entering_ann[good]],label=good)

	for good in leaving_ann:
		ax[1].plot([i['year'] for i in leaving_ann[good]],[i['val'] for i in leaving_ann[good]],label=good)
	
	plt.legend()
	plt.show()



def plot_tobacco():
	text_dump = open(dump,'r').read()

	transaction_list = json.loads(text_dump)

	# Find all headers 
	goods = {}

	for t in transaction_list:
		if not t['good'] in goods:
			this_good = t['good']
			this_good_o = t['origin']
			goods[this_good] = {'count':0, 'origin':[]}
			goods[this_good]['count'] = 1
			goods[this_good]['origin'] = [t['origin']]

		else:
			goods[this_good]['count'] += 1
			if not t['origin'] in goods[this_good]['origin']:
				goods[this_good]['origin'].append(t['origin'])


	leaving_for_gb = {}
	leaving_for_wi = {}

	'ACCO'
	'JRLO'

	tobacco_to_gb = open("tobacco_to_gb.csv",'w')
	tobacco_to_wi = open("tobacco_to_wi",'w')
	tobacco_to_wi.write('year,amount\n')
	tobacco_to_gb.write('year,amount\n')

	for t in transaction_list:
		good = t['good']
		try:
			year = int(t['year'])
			val = float(t['total_value'])
		except ValueError:
			continue
		dest = t['destination']
		origin = t['origin']
		direction = t['direction']


		if not good == 'Tobacco' or not direction == 'CL' or not origin in ['ACCO',"JRLO"]:
			continue 
		
		if dest == 'GB':
			tobacco_to_gb.write(f"{year},{val}\n")
		elif dest =='WI':
			tobacco_to_wi.write(f"{year},{val}\n")

	tobacco_to_wi.close()
	tobacco_to_gb.close()

			


#write_all()
plot_tobacco()
