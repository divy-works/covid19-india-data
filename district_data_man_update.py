from json import load as json_load
from requests import get as requests_get
from os import path
from tabula import convert_into
from sys import argv

with open('config.json') as json_file:
    config_data = json_load(json_file)
    covid_data_link = config_data['covid19_data_link']
    pdf_data_file_name = config_data['pdf_data_file_name']
    csv_data_file_name = config_data['csv_data_file_name']

#download covid19 data for India
print("downloading pdf data file...")
pdf_file_download = requests_get(covid_data_link)
open(pdf_data_file_name, 'wb').write(pdf_file_download.content)

#convert covid19 data from pdf to csv
print("converting pdf data file to csv...")
convert_into(pdf_data_file_name, pages='all', output_format='csv', output_path=path.join(path.curdir, csv_data_file_name))

#check if the csv file is converted right
user_response = input("Check if the csv file has been converted right?(yes/no)")
if user_response.lower() == 'yes':
    #upload data to aws s3
    local_file = csv_data_file_name #manually created 
    bucket = "covid19-india-datasets"
    s3_file = csv_data_file_name
    upload_to_aws(local_file, bucket, s3_file, aws_config_file_path)