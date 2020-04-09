from bs4 import BeautifulSoup
from requests import get
from upload_to_aws import upload_to_aws
from json import dump as json_dump
from get_lat_lng import get_lat_lang

url = "https://www.mohfw.gov.in/"

#this is very specific to the website being used
def scrape_website_for_stats(aws_config_file_path):
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_of_classes = ['bg-blue', 'bg-green', 'bg-red', 'bg-orange']
    dashboard_data = soup.find(id='site-dashboard').find(class_='site-stats-count')
    dashboard_dict = {}
    for class_type in list_of_classes:
        text = soup.find(class_=class_type).find('span').get_text()
        number = int(soup.find(class_=class_type).find('strong').get_text())
        if 'active' in text.lower():
            dashboard_dict['active'] = number
        if 'death' in text.lower():
            dashboard_dict['deaths'] = number
        if 'cured' in text.lower():
            dashboard_dict['recovered'] = number
        if 'migrated' in text.lower():
            dashboard_dict['migrated'] = number
    
    update_time = dashboard_data.find(class_='status-update').find('span').get_text()
    dashboard_dict['update_time'] = update_time

    covid_india_stats_filename = 'covid-india-stats.json'
    with open(covid_india_stats_filename, 'w') as json_file:
        json_dump(dashboard_dict, json_file)

    upload_to_aws("covid-india-stats.json","covid19-india-datasets", "covid-india-stats.json", aws_config_file_path)


def scrape_website_for_state_data(aws_config_file_path):
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = soup.find(id='state-data')
    table_data = soup.find('tbody').find_all('tr')
    state_data = {}
    #order of data in row in with name of serial number, state, total cases, recovered and deaths
    for row in table_data:
        row = row.find_all('td')
        if len(row) == 5:
            state_name = row[1].get_text()
            active_cases = row[2].get_text()
            recovered = row[3].get_text()
            deaths = row[4].get_text()
            state_latitude, state_longitude = get_lat_lang(None, state_name, 'previous_data.json')
            state_data[state_name] = {
                'active_cases' : active_cases,
                'recovered' : recovered,
                'deaths' : deaths,
                'latitude' : state_latitude,
                'longitude': state_longitude
            }
    
    covid_india_states_data_filename = 'covid-india-states-data.json'

    with open(covid_india_states_data_filename, 'w') as json_file:
        json_dump(state_data, json_file)

    upload_to_aws("covid-india-states-data.json", "covid19-india-datasets", "covid-india-states-data.json", aws_config_file_path)

if __name__ == '__main__':
    scrape_website_for_stats()
    scrape_website_for_state_data()