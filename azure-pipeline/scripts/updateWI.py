import os
import requests
import json

project=os.environ['SYSTEM_TEAMPROJECT']
buildId=os.environ['BUILD_BUILDID']
token=os.environ['SYSTEM_ACCESSTOKEN']
project=os.environ['SYSTEM_TEAMPROJECT']
organization='cooclass'
headers = {'Authorization': f'Bearer {token}'}

def get_related_work_item(id):
    build_url=f'https://dev.azure.com/{organization}/{project}/_apis/build/builds/{id}/workitems?api-version=7.0'
    response = requests.get(build_url, headers=headers)
    return response.json()

def get_item(id):   
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    response=requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def update_item(id):
    response=get_item(id)
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    #if (response['fields']["System.WorkItemType"] == 'Task') and (response['fields']['System.State']=='Deploy to test'):
    if (response['fields']['System.State']=='Deploy to test'):
        data=[{
            'op': 'replace',
            'path': '/fields/System.State',
            'value':'Ready to UAT'
		}]
		
        headers={'Authorization': f'Bearer {token}','Content-Type': 'application/json-patch+json', 'charset':'utf-8'}
        response=requests.patch(url, json=data, headers=headers)
        print(response.text)
        return response.json()
    else:
        print('Cant patch item: State not "Deploy to test"')


output=get_related_work_item(buildId)
count = output['count']
if count > 0:
    for i in range(count):
        response=update_item(output['value'][i]['id'])
        print(response)
else:
    print('No related work items found')
