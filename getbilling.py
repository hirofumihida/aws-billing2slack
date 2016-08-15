import boto3
from datetime import datetime, timedelta

import json
import requests

import os

cloudwatch = boto3.resource('cloudwatch')
metric = cloudwatch.Metric('AWS/Billing','EstimatedCharges')

url = os.environ["WEBHOOK_URL"]

d = datetime.today() - timedelta(days=1)
start_time = datetime(d.year, d.month, d.day, 0, 0, 0)
end_time = datetime(d.year, d.month, d.day, 23, 59, 59)

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
        'Average'
    ]
    )

bill_average = response['Datapoints'][0]['Average']

content = format(round(bill_average,2), '.2f') + 'USD' + ' (Average: from ' + str(start_time) + ' to ' + str(end_time) + ')'

payload_dic = {
    "text":content,
    "username":'AWS Monthly Billing',
    "icon_emoji":':dollar:',
    "channel":'#test_01',
    }

if __name__=='__main__':
    r = requests.post(url, data=json.dumps(payload_dic))
