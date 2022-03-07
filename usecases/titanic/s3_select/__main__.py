import boto3
import os

endpoint_url = os.getenv('DATALAKE_URL') \
    or sys.exit("DATALAKE_URL is not set")

access_key = os.getenv('DATALAKE_ACCESS_KEY') \
    or sys.exit("DATALAKE_ACCESS_KEY is not set")
secret_key = os.getenv('DATALAKE_SECRET_KEY') \
    or sys.exit("DATALAKE_SECRET_KEY is not set")
bucket = os.getenv('DATALAKE_BUCKET', 'group-prj00001')

s3 = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name='us-east-1'
)

r = s3.select_object_content(
    Bucket=bucket,
    Key='titanic/data/train.csv',
    ExpressionType='SQL',
    Expression="select count(*) from s3object s where s.Survived=1 and s.Embarked='C' ",
    InputSerialization={
        'CSV': {
            "FileHeaderInfo": "USE",
        },
        # 'CompressionType': 'GZIP',
    },
    OutputSerialization={'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print("How many people embarked at Cherbourg and survived: ", records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytes Scanned:   ", statsDetails['BytesScanned'])
        print("Stats details bytes Processed: ", statsDetails['BytesProcessed'])
