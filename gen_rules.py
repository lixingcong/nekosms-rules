#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NekoSMS filter rules print/encode

import json
import datetime

# print keyword from json
def print_kw(filename):
	items={}
	with open(filename) as f:
		data=json.load(f)

		for filter in data['filters']:
			action=filter['action']
			
			if items.has_key(action) is False:
				items[action]=[]
			
			items[action].append(filter['body']['pattern'])
	
	for key, value in items.iteritems():
		print 'action: '+key
		for pattern in value:
			print pattern
		print '*'*20

# Generate json from keyword file
def get_filter_from_kw(keyword_filename, action):
	# Read all keywords
	keyword_array=[]
	with open(keyword_filename, 'r') as f:
		for line in f.readlines():
			line_striped=line.strip()
			if len(line_striped) > 0:
				keyword_array.append(line_striped)
	
	# Add keywords to filter array
	filters=[]
	for keyword in keyword_array:
		a_filter={'action':action, 'body':{'mode':'contains', 'pattern':keyword, 'case_sensitive':False}}
		print action+': '+keyword
		filters.append(a_filter)
	
	if len(filters) <= 0:
		print keyword_filename+': filter was empty'
	
	return filters

# write the array to a json file
def write_all_filters_to_file(filters, filename, version):
	# Add version to json head
	data_final={'version':version, 'filters':filters}
	json_obj=json.dumps(data_final, indent=1, ensure_ascii=False)

	# Write to file
	with open(filename, 'wb') as f:
		print '*'*20
		print 'writing to '+filename
		f.write(json_obj)

if __name__ == "__main__":
	filename_nsbak_to_load='/tmp/nekosms.nsbak'
	filename_keyword_block='keywords_block.txt'
	filename_keyword_allow='keywords_allow.txt'
	
	print '1 for print from '+filename_nsbak_to_load
	print '2 for generate new rules from txt files'
	mode=raw_input("Enter the number: ")
	
	if '2' == mode:
		# To generate nsbak from keyword.txt
		filter_block=get_filter_from_kw(filename_keyword_block,'block')
		filter_allow=get_filter_from_kw(filename_keyword_allow,'allow')
		
		time_str=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
		filename_nsbak_to_save='/tmp/nekosms_'+time_str+'.nsbak'
		write_all_filters_to_file(filter_block+filter_allow,filename_nsbak_to_save,'3')
	else:
		# To print all keyword from 'nsbak' file
		print_kw(filename_nsbak_to_load)
