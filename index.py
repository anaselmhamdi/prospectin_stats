import json
import pymongo
import os
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime, timedelta


dbName = os.environ['dbName']
collectionName = os.environ['collectionName']
mongoUri = os.environ['mongoUri']

def parse_email_html(html):
    soup = BeautifulSoup(html,'lxml')
    members = soup.find_all('div',class_='member')
    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    results = []
    for member in members:
        name = member.span.get_text()
        results.append({
            "Name": name if 'My company' not in name else 'Total',
            "Invites sent": member.find('img',src="https://i.ibb.co/R0VPN8M/icon-link.png").next.next.get_text(),
            "Messages sent": member.find('img',src="https://i.ibb.co/cyqKTW7/icon-msg.png").next.next.get_text(),
            "Visits": member.find('img',src="https://i.ibb.co/JRKQ00F/icon-follow.png").next.next.get_text(),
            "Message w/ answer": member.find('img',src="https://i.ibb.co/f9TsZ3d/icon-msg-r.png").next.next.get_text(),
            "Invites w/ answer": member.find('img',src="https://i.ibb.co/44ZqMyf/icon-link-r.png").next.next.get_text(),
            "Accepted invites": member.find('img',src="https://i.ibb.co/rbSXybz/icon-link-v.png").next.next.get_text(),
            "Date": date
        })
    return results

headers = {
                'Access-Control-Allow-Credentials' : True,
                "Access-Control-Allow-Origin": "*"
                }    

def stats_storage(event, context):
    results = parse_email_html(data['html'])
    client = pymongo.MongoClient(mongoUri)
    client.dbName.collectionName.insert_many(results)
    return {
        "statusCode":200, 
        "body":json.dumps({"success":True}),
        "headers":headers
        }

def get_stats(event,context):
    queryStringParam = event["queryStringParameters"]
    last_days = 7 # defaults to a week
    if queryStringParam:
        last_days = queryStringParam.get('last_days') 
    client = pymongo.MongoClient(mongoUri)
    search_date = (datetime.utcnow() - timedelta(days=int(last_days))).strftime('%Y-%m-%d')
    dp = pd.DataFrame([d for d in client.dbName.collectionName.find({"Date":{"$gte":search_date}},{"_id":0})])
    if len(dp) > 0:
        dp.drop(columns=['Date'], inplace=True)
        dp = dp.astype({
                k: 'int32' for k in ['Invites sent','Messages sent','Visits','Message w/ answer','Invites w/ answer','Accepted invites']
                }).copy()
        dp = dp.groupby('Name').sum().reset_index().copy()
        return {
            "statusCode":200,
            "body": json.dumps(dp.to_dict(orient='records')),
            "headers": headers
        }
    else:
        return {
            "statusCode":200,
            "body": json.dumps([]),
            "headers": headers
        }  
