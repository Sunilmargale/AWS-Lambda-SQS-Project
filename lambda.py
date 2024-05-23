import boto3
import json

def lambda_handler(event, context):
    # Get the SQS messages from the event
    print(event)
    ses_client = boto3.client('ses', region_name='ap-south-1')
    reciever_email = 'sunilmargale2706@gmail.com'
    
    for record in event['Records']:
        data = json.loads(record['body'])
        records = data['Records']
        
        for record in records:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            
            if "sensitive" in object_key.lower():
                print('Bucket has sensitive file')
                send_email(ses_client, reciever_email, bucket_name)
            else:
                print('Nothing suspicious')
            
    
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully!'
    }

def send_email(ses_client, to_email, bucket_name):
    subject = 'Bucket Alert'
    body = f'The bucket {bucket_name} requires attention.'
    
    response = ses_client.send_email(
        Source='sunilmargale27@gmail.com',
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    
    print("Email sent for forthuer investigation :", response)
