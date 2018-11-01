#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NekoSMS filter rules print/encode

import json

# print keyword from json
def print_kw(filename):
	with open(filename) as f:
		data=json.load(f)

		for filter in data['filters']:
			print filter['body']['pattern']

# Generate json from keyword file
def generate_json_from_kw(filename_to_load, filename_to_save, version):
	# Read all keywords
	keyword_array=[]
	with open(filename_to_load, 'r') as f:
		for line in f.readlines():
			line_striped=line.strip()
			if len(line_striped) > 0:
				keyword_array.append(line_striped)
	
	# Add keywords to filter array
	filters=[]
	for keyword in keyword_array:
		a_filter={'action':'block', 'body':{'mode':'contains', 'pattern':keyword, 'case_sensitive':False}}
		filters.append(a_filter)
	
	# Add version to json head
	data_final={'version':version, 'filters':filters}
	json_obj=json.dumps(data_final, indent=1, ensure_ascii=False)

	# Write to file
	with open(filename_to_save, 'wb') as f:
		f.write(json_obj)

if __name__ == "__main__":
	# To print all keyword from 'nsbak' file
	print_kw('/tmp/nekosms.nsbak')
	
	# To generate nsbak from keyword.txt
	#generate_json_from_kw('keywords_block.txt','/tmp/keywords_block.nsbak','3')
