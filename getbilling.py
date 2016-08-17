import boto3
from datetime import datetime, timedelta

import json
import requests

import os

cloudwatch = boto3.resource('cloudwatch')
metric = cloudwatch.Metric('AWS/Billing','EstimatedCharges')

url = os.environ["WEBHOOK_URL"]
channel_name = '#billing'

d0 = datetime.now() - timedelta(hours=24)
d1 = datetime.now()

start_time = datetime(d0.year, d0.month, d0.day, d0.hour, 0, 0)
end_time = datetime(d1.year, d1.month, d1.day, d1.hour, 0, 0)

#print start_time
#print end_time

response = metric.get_statistics(
    Dimensions=[
        {
            'Name': 'Currency',
            'Value': 'USD'
        },
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=86400,
    Statistics=[
        'Maximum',
    ]
    )

#print response

bill_max = response['Datapoints'][0]['Maximum']

content = format(round(bill_max,2), '.2f') + 'USD' + ' (Max: from ' + str(start_time) + ' to ' + str(end_time) + ')'

payload_dic = {
    "text":content,
    "username":'AWS Monthly Billing',
    "icon_emoji":':awscloud:',
    "channel":channel_name,
    }

if __name__=='__main__':
    r = requests.post(url, data=json.dumps(payload_dic))
