#
# 1) Checks a dynamo table for an index of date. 
# 2) If one matches today, generate a payload and send to a glip webhook.
# 
# Can manually trigger or create an AWS Eventbridge rule. 
# Ryan Gamo, 2020 
#
import json
import boto3

def lambda_handler(event, context):
    from datetime import date, timezone
    from botocore.vendored import requests
    
    today = str(date.today())
    
    # Generate content for the glip message
    # Calls getEvent() and gets the item/row for the index (in this case, date) matching today
    eventdetail = getEvent(today)
    
    # Generate the JSON Payload
    # Calls writejson() formatting elements from the item in eventdetail.
    # Passes the date in because it's used in the JSON payload.
    glipmessage = writejson(eventdetail,today)
    
    # URI variables in case you have a test/prod webhook
    testuri = #Insert a TEST URI here [optional]
    produri = #Insert a PROD URI here 
    
    # Required headers and payload
    headers = {
        'Content-Type': 'application/json',
      }

    data = glipmessage

    # Flip between test and prod URI's
    r = requests.post(produri, headers=headers, data=data)

# Connect to your dynamoDB table
def getEvent(Date, dynamodb='None'):
    dynamodb = boto3.resource('dynamodb',region_name='us-west-2')
    table = dynamodb.Table('#PUT YOUR TABLE NAME HERE')

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

