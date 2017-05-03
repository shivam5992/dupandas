from Levenshtein import ratio as lev_ratio
import pandas as pd 

traversed_indexes = {}

def levenshtein_match(text1, text2):
	return lev_ratio(text1, text2)

def match_records(x, flag):
	if flag == 'halka':
		t1 = str(x['src_Patwari halka name'])
		t2 = str(x['src_Hname']) 	

		t3 = str(x['cln_Patwari halka name'])
		t4 = str(x['cln_Hname'])
	elif flag == 'revenue':
		t1 = str(x['src_Revenue circle name'])
		t2 = str(x['src_Rname']) 

		t3 = str(x['cln_Revenue circle name'])
		t4 = str(x['cln_Rname'])
	elif flag == 'village':
		t1 = str(x['src_VillageName'])
		t2 = str(x['src_Vname']) 

		t3 = str(x['cln_VillageName'])
		t4 = str(x['cln_Vname'])	

	matched = False 
	score = levenshtein_match(t3, t4)
	if score >= 0.65:
		matched = True 

	if matched == False:
		t3w = t3.split()
		t4w = t4.split()

		if len(t3w) > 1 or len(t4w) > 1:
			t3w = t3w[0]
			t4w = t4w[0]
			score = levenshtein_match(t3w, t4w)
			if score >= 0.75:
				matched = True
			# else:
			# 	score = levenshtein_match(t3w, t4w)


	return score

def inp_architecture(inpDF):
	print "Matching Halkas"
	inpDF['halka_scr'] = inpDF.apply(lambda x: match_records(x, 'halka'), axis=1)

	print "Matching Revenue Circles"
	inpDF['revenue_scr'] = inpDF.apply(lambda x: match_records(x, 'revenue'), axis=1)

	print "Matching Villages"
	inpDF['village_scr'] = inpDF.apply(lambda x: match_records(x, 'village'), axis=1)

	print "Combining Scores"
	inpDF['score'] = inpDF.apply(lambda x: x['halka_scr']+x['revenue_scr']+x['village_scr'], axis=1)

	# Drop irrelevant columns 
	drop = []
	# drop = ['cln_Patwari halka name', 'cln_Vname', 'cln_VillageName', 'cln_Revenue circle name', 'cln_Rname', 'cln_Hname']
	drop.extend(['src_Patwari halka name', 'src_Vname', 'src_VillageName', 'src_Revenue circle name', 'src_Rname', 'src_Hname'])
	inpDF = inpDF.drop(drop, axis=1)
	
	fixed_inpDF = inpDF[((inpDF['village_scr']>=0.70) & (inpDF['halka_scr']>=0.70) & (inpDF['revenue_scr']>=0.70))]
	flex_inpDF = inpDF[((inpDF['village_scr']>=0.70) & ((inpDF['halka_scr']>=0.70) | (inpDF['revenue_scr']>=0.70)))]
	
	return inpDF, fixed_inpDF, flex_inpDF


def update_row(pairDF, flag_tag, columns):
	mrow = pairDF.sort(['score'], ascending=[False]).iloc[0]
	obtained_row = {}

	if flag_tag == 'LowMatch1':
		if (mrow['score']>2.0) :#and (mrow['halka_scr']>0.6) and (mrow['village_scr']>0.55) and (mrow['revenue_scr']>0.6):
			pass 
		else:
			return obtained_row

	## Ingest Row
	for col in columns:
		if col in mrow:
			obtained_row[col] = mrow[col]
		else:
			obtained_row[col] = ""
	obtained_row['tag'] = flag_tag

	## Track Master Index
	master_index = mrow['master_index']
	if master_index not in traversed_indexes:
		traversed_indexes[master_index] = 1

	return obtained_row

# def remove_custom_noise(text, sort = False):
# 	text = str(text).lower().strip()
# 	text = "".join([x for x in text if x not in combined_exclude]).strip()
# 	if sort:
# 		text = "".join(sorted(text)).strip()
# 	return text

# def fix_last_cases(r, flag):
# 	dv, dh, dr = r['VillageName'], r['Patwari halka name'], r['Revenue circle name']
# 	sv, sh, sr = r['Vname'], r['Hname'], r['Rname']

# 	if flag == 'v':
# 		s1 = lev_ratio(remove_custom_noise(str(dv)), remove_custom_noise(str(sv)))
# 	elif flag == 'h':
# 		s1 = lev_ratio(remove_custom_noise(str(dh)), remove_custom_noise(str(sh)))
# 	elif flag == 'r':
# 		s1 = lev_ratio(remove_custom_noise(str(dr)), remove_custom_noise(str(sr)))
# 	return s1 


def _process_records(config):
	print "Reading Files"
	StateMaster = pd.read_csv(config['state_master_file'])
	DistBatch = pd.read_csv(config['dist_file'])
	
	print "Merge Datasets"	
	StateMaster.rename(columns={'State Record DName': 'DistrictName'}, inplace = True)
	StateMaster.rename(columns={'State Record TName': 'SubDistrictName'}, inplace = True)
	
	# Apply District Name Filter and Merge both datasets on the basis of DistrictName
	DistrictSubset = StateMaster[StateMaster['DistrictName'] == list(DistBatch['DistrictName'])[0]]
	
	# Apply Filter on SubDistrictName and obtain Cartesian Pairs 
	subDistDF = pd.merge(DistBatch, DistrictSubset, on = ['SubDistrictName'])	
	completeDF, fixed_inpDF, flex_inpDF = inp_architecture(subDistDF)
	completeDF.to_csv("complete.csv")
	

	# Apply Non Sub District and obtain Cartesian Pairs, Calculate this on smaller DistBatch -- after performing first filter 
	nonSubDistDF = pd.merge(DistBatch, DistrictSubset, on = ['DistrictName'])
	complete_nonSub_DF, nonSub_fixed_inpDF, nonSub_flex_inpDF = inp_architecture(nonSubDistDF)
	
	# Iterate in original Distt DF and append the matches
	columns = list(fixed_inpDF)
	cnt = 0
	all_rows = []
	non_sr = []
	for i, row in DistBatch.iterrows():
		dist_index = row['dist_index']
		
		## Find Matched based on Complete Matching
		obtained = False
		matched_pairs = fixed_inpDF[fixed_inpDF['dist_index'] == dist_index]
		if len(matched_pairs) > 0:
			obtained_row = update_row(matched_pairs, 'StrongMatch', columns)
			all_rows.append(obtained_row)
			obtained = True
		
		if obtained == False:
			## Find Matched based on One of the two Matching
			flex_pairs = flex_inpDF[flex_inpDF['dist_index'] == dist_index]
			if len(flex_pairs) > 0:
				obtained_row = update_row(flex_pairs, 'LowMatch', columns)
				all_rows.append(obtained_row)
				obtained = True

		if obtained == False:
			## Find Matched based on non Tehsil Filter
			nonT_matched_pairs = nonSub_fixed_inpDF[nonSub_fixed_inpDF['dist_index'] == dist_index]
			if len(nonT_matched_pairs) > 0:	
				obtained_row = update_row(nonT_matched_pairs, 'nonT_StrongMatch', columns)
				all_rows.append(obtained_row)
				obtained = True 
		
		if obtained == False:
			## Find Matched based on non Tehsil Filter and one of the two match
			nonT_flex_pairs = nonSub_flex_inpDF[nonSub_flex_inpDF['dist_index'] == dist_index]
			if len(nonT_flex_pairs) > 0:	
				obtained_row = update_row(nonT_flex_pairs, 'nonT_LowMatch', columns)
				all_rows.append(obtained_row)
				obtained = True

		if obtained == False:
			## More Cases - Fixing 
			matched_pairs = completeDF[completeDF['dist_index'] == dist_index]
			if len(matched_pairs) > 0:	
				obtained_row = update_row(matched_pairs, 'LowMatch1', columns)
				if obtained_row:
					all_rows.append(obtained_row)
					obtained = True
		
		if obtained == False:
			obtained_row = {}
			for col in columns:
				if col in row:
					obtained_row[col] = row[col]
				else:
					obtained_row[col] = ""
			obtained_row['tag'] =  'notfoundinSR'
			all_rows.append(obtained_row)
	
	## Iterating in records from main file which are not matched in SR using Tehsil Filter
	non_dr = []
	for i, row in DistrictSubset.iterrows():
		if row['master_index'] not in traversed_indexes:
			traversed_indexes[row['master_index']] = 1 
			### Repeat the matching process 
			obtained_row = {}
			for col in columns:
				if col in row:
					obtained_row[col] = row[col]
				else:
					obtained_row[col] = ""
			obtained_row['tag'] = 'notfoundinDR'
			all_rows.append(obtained_row)

	# ## Generate the output file 
	outputDF = pd.DataFrame(all_rows)

	# nonDR = pd.DataFrame(non_dr)
	# nonSR = pd.DataFrame(non_sr)
	
	outputDF.rename(columns={'DistrictName_x': 'DistrictName'}, inplace = True)
	outputDF.rename(columns={'DistrictName_y': 'State Record DName'}, inplace = True)
	outputDF = outputDF.reindex(outputDF.index.rename('row_id'))

	
	columns = ['State Code','State Name','DistrictCode','DistrictName','SubDistrictCode','SubDistrictName','BlockCode','BlockName','VillageCode','VillageName','GramPanchyatCode','GramPanchyatName','Patwari halka number','Patwari halka name','Revenue  circle Number','Revenue circle name',' sr no','dcode','Dname','tcode','Tname','rcode','Rname','hcode','Hname','vcode','Vname', 'score', 'tag']
	outputDF = outputDF[columns]
	outputDF.to_csv("output/"+config['dist_file'])

if __name__ == '__main__':
	dist_files = ["datia.csv"]#, "Chhindwara.csv"]
	# dist_files = ["bhind.csv"]

	for dist_file in dist_files:
		state_master_file = "state_data.csv"
		config = {
			'state_master_file' : "data/cln_"+state_master_file,
			'dist_file' : "data/cln_"+dist_file
		}

		_process_records(config)
