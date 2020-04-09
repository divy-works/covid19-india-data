import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_aws(local_file, bucket, s3_file):
    aws_access_key_id = str(input("Enter AWS Access Key Id : "))
    aws_secret_access_key = str(input("Enter AWS Secret Key : "))

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

local_file = 'covid19_district_data.json'
s3_file_name = local_file
bucket_name = 'covid19-india-datasets'

uploaded = upload_to_aws(local_file, bucket_name, s3_file_name)
