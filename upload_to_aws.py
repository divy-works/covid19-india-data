import boto3
from botocore.exceptions import NoCredentialsError
from os import path
from json import load as json_load


def upload_to_aws(local_file, bucket, s3_file, aws_config_file_path):
    aws_config_file = 'aws_key_config.json'
    if path.isfile(aws_config_file_path):
        with open(aws_config_file_path) as json_file:
            aws_config_data = json_load(json_file)
            aws_access_key_id = aws_config_data['aws_access_key_id']
            aws_secret_access_key = aws_config_data['aws_secret_access_key']
    else:
        aws_access_key_id = str(input("Enter AWS Access Key Id : "))
        aws_secret_access_key = str(input("Enter AWS Secret Key : "))

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

if __name__ == '__main__':
    aws_config_file_path = '../aws/aws_key_config.json'
    local_file = 'covid19_district_data.json'
    bucket = "covid19-india-datasets"
    s3_file = 'covid19_district_data.json'
    upload_to_aws(local_file, bucket, s3_file, aws_config_file_path)
    local_file = 'covid-india-states-data.json'
    bucket = "covid19-india-datasets"
    s3_file = 'covid-india-states-data.json'
    upload_to_aws(local_file, bucket, s3_file, aws_config_file_path)