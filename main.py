from requests import get as requests_get
from json import load as json_load
from json import dump as json_dump
from tabula import convert_into
from csv import reader as csv_reader
from os import path
from get_lat_lng import get_lat_lang
from upload_to_aws import upload_to_aws
from sys import argv
from scrape_website_for_stats import scrape_website_for_state_data, scrape_website_for_stats


with open('config.json') as json_file:
    config_data = json_load(json_file)
    covid_data_link = config_data['covid19_data_link']
    pdf_data_file_name = config_data['pdf_data_file_name']
    csv_data_file_name = config_data['csv_data_file_name']
    json_data_file_name = config_data['json_data_file_name']
    aws_bucket_name = config_data['aws_bucket_name']
    uploaded_data_link = config_data['aws_json_data_link']

#download covid19 data for India
print("downloading pdf data file...")
pdf_file_download = requests_get(covid_data_link)
open(pdf_data_file_name, 'wb').write(pdf_file_download.content)

#convert covid19 data from pdf to csv
print("converting pdf data file to csv...")
convert_into(pdf_data_file_name, pages='all', output_format='csv', output_path=path.join(path.curdir, csv_data_file_name))

previous_data_file_name = 'previous_data.json'
previously_uploaded_data = requests_get(uploaded_data_link)
open(previous_data_file_name, 'wb').write(previously_uploaded_data.content)

#clean up csv data and arrange it as a dictionary 
district_covid_cases = {}
#update with the number of active cases, cured, deaths and migrated 
state_name = ''
with open(csv_data_file_name) as csvFile:
    readCSV = csv_reader(csvFile, delimiter=',')
    for row in readCSV:
        if row[0] != '' and row[1] != '' and row[2] != '' and row[3] != '':
            state_name = row[0]
            state_district_count = row[1]
            district_name = row[2]
            district_count = row[3]
        elif row[0] != '' and row[1] != '':
            district_name = row[0]
            district_count = row[1]
        elif row[1] != '' and row[2] != '':
            district_name = row[1]
            district_count = row[2]
        elif row[2] != '' and row[3] != '':
            district_name = row[2]
            district_count = row[3]
        
        if state_name != '' and 'district_name' in vars():
            try:
                district_count = int(district_count)
                latitude, longitude = get_lat_lang(district_name, state_name, previous_data_file_name)
                if state_name not in district_covid_cases.keys():
                    state_latitude, state_longitude = get_lat_lang(None, state_name, previous_data_file_name)
                    district_covid_cases[state_name] = {
                        "latitude" : state_latitude,
                        "longitude" : state_longitude,
                        "total_count" : district_count,
                        "districts" : {}
                    }
                    district_covid_cases[state_name]['districts'][district_name] = {'count': district_count, 'latitude': latitude, 'longitude': longitude}
                else:
                    district_covid_cases[state_name]['total_count'] += district_count
                    district_covid_cases[state_name]['districts'][district_name] = {'count': district_count, 'latitude': latitude, 'longitude': longitude}
            except:
                Warning('count for district = ' + district_name + ' is not a number')

print("writing covid districts data file...")
with open(json_data_file_name, 'w') as json_file:
    json_dump(district_covid_cases, json_file)


aws_config_file_path = argv[1]
upload_to_aws(json_data_file_name, aws_bucket_name, json_data_file_name, aws_config_file_path)
scrape_website_for_stats(aws_config_file_path)
scrape_website_for_state_data(aws_config_file_path)