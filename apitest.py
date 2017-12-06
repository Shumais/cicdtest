
#!/usr/local/bin/python3
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# This program upload files from FTP server to S3
#
# Author: Hamza Sarwar
#
# Modification Log:
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Date                      Author                  Description
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# 06/15/2017                Hamza Sarwar             Initial Draft
import requests
import json 
import boto3
import os
import urllib.request





file_path = 'images/5.pdf'  # webhook will provide filepath
s3_client = boto3.client('s3')
brick_api_url= "https://nbs.brickftp.com/api/rest/v1/"
brick_credentials = {'username': "waseem.nbs", "password": "waseem123"}
output_bucket = 'temp-hamza'


file_url=''
file_name=''
def brickftp_file_url(args):
	global file_url

	try:
		session = requests.post(brick_api_url+"sessions", brick_credentials)
		session_json = json.loads(session.text)
		session_id = session_json['id']
		
		
		request = requests.get(brick_api_url+"files/"+file_path , cookies= dict(BrickAPI=session_id))
		file_url= json.loads(request.text)['download_uri']
		file_size = json.loads(request.text)['size']
		if file_size == 0:
			print("Empty_file")
			exit(0)
	except Exception as e:
		print("URL_not_retrieved")
		print(e)
		exit(1)


def brickftp_download_file(args):
	global file_name

	try:
		file_name = file_path.split('/')
		urllib.request.urlretrieve(file_url, file_name[-1])

	except Exception as e:
		print("file_not_downloaded")
		exit(1)


def upload_file_to_s3(args):
	global file_name
	try:
		s3_client.upload_file(file_name[-1] , output_bucket, file_path)	
	except Exception as e:
		print("Upload failed")
		print(e)
		exit(1)

def delete_file_from_runner(args):
	global file_name
	try:
		os.remove(file_name[-1])
	except Exception as e:
		print("delete failed")
		print(e)
		exit(1)


if __name__ == '__main__':
	brickftp_file_url('')
	brickftp_download_file('')
	upload_file_to_s3('')
	delete_file_from_runner('')
	print('process completed successfully')

