import json
import boto3

def lambda_handler(event, context):
    from datetime import date, timezone
    from botocore.vendored import requests
    
    today = str(date.today())
    
    # Generate content for the glip message
    eventdetail = getEvent(today)
    
    glipmessage = writejson(eventdetail,today)
    testuri = #Insert a TEST URI here [optional]
    produri = #Insert a PROD URI here 
    
    headers = {
        'Content-Type': 'application/json',
      }

    data = glipmessage

    # Flip between test and prod URI's
    r = requests.post(produri, headers=headers, data=data)

# Connect to your dynamoDB table
def getEvent(Date, dynamodb='None'):
    dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('tblTDRschedule')

    response = table.get_item(
        Key={
            'Date': Date
        })
    return response['Item']

# Writes the glip message JSON payload
def writejson(eventdetail,today):

    data = {}
    data['attachments'] = []
    data['attachments'].append({
       "type": "Card",
    "fallback": "Something bad happened",
    "pretext": "TDR Status Bot (Alpha)",
    "color": "#00ff2a",
    "title": "TDR " + today,
    "fields": [
    {
        "title": "Sites",
        "value": eventdetail['Sites'],
        "short": "true"
    },
    {
        "title": "Command Center",
        "value": "**Endpoint Engineering:** " + eventdetail['Engineering'] +"\n**Epic:** " + eventdetail['Epic'] + "\n**1VU:** " + eventdetail['1VU'],
        "short": "true"
    },
     {
        "title": "Deployment",
        "value": "Payload A - 5:00PM Pacific\nPayload C - BCA 5:00PM Pacific\nPayload B - When operatories are clear",
        "short": "false"
    },
     {
        "title": "BCA",
        "value": eventdetail['BCA'],
        "short": "false"
    }
        
    ]
})
    return json.dumps(data)

