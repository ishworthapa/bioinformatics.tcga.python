#!/usr/bin/python3

################################################################################
# Titile: addBarcode.py                                                        #
# Description: A script that calls gdc api to get barcode for the FPKM files   #
# Author: Ishwor Thapa                                                         #
# Version: 20180105                                                            #
# Usage: ./addBarcode.py inputManifestFile outputCsv                           #
# Python: >3                                                                   #
# Requires: requests, json                                                     #
################################################################################

import requests, json
import sys

input = sys.argv
if len(input) != 3:
	sys.stderr.write("Error: Invalid input\n")
	sys.stderr.write("Usage: ./addBarcode.py inputManifestFile outputCsv\n")
	sys.exit(1)

manifest, output = input[1:]
fin = open(manifest,'r')
fout = open(output, 'w')

for line in fin.readlines():
	uuid, filename, md5, size, state = line.strip().split()
	if uuid == "id": continue
	# refer https://docs.gdc.cancer.gov/API/Users_Guide/Search_and_Retrieval/
	# refer https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/
	cases_endpt = 'https://api.gdc.cancer.gov/files/' + uuid
	params = {'fields':'file_id,file_name,cases.samples.sample_type,' +\
		'cases.samples.submitter_id','format':'json'}
	response = requests.get(cases_endpt, params = params)
	content = json.loads(response.content)
	file_id = content['data']['file_id']
	file_name = content['data']['file_name']
	barcode = content['data']['cases'][0]['samples'][0]['submitter_id']
	sample_type = content['data']['cases'][0]['samples'][0]['sample_type']

	fout.write(','.join([file_id, file_name, barcode, sample_type]) + '\n')

fout.close()
fin.close()
