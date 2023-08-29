import os
import requests
import json

print(os.environ)
project=os.environ['SYSTEM_TEAMPROJECT']
buildId=os.environ['BUILD_BUILDID']
token=os.environ['SYSTEM_ACCESSTOKEN']
project=os.environ['SYSTEM_TEAMPROJECT']
requester=os.environ['BUILD_REQUESTEDFOR']
sourcebranch=os.environ['BUILD_SOURCEBRANCH']
organization='cooclass'
headers = {'Authorization': f'Bearer {token}'}

def get_related_work_item(id):
    build_url=f'https://dev.azure.com/{organization}/{project}/_apis/build/builds/{id}/workitems?api-version=7.0'
    response = requests.get(build_url, headers=headers)
    return response.json()

def get_item(id):   
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    response=requests.get(url, headers=headers)
    print('getitem():',response.json())
    return response.json()
def patch_item(url, value):
    data=[{
        'op': 'replace',
        'path': '/fields/System.State',
        'value':value
	}]
    headers={'Authorization': f'Bearer {token}','Content-Type': 'application/json-patch+json', 'charset':'utf-8'}
    response=requests.patch(url, json=data, headers=headers)
    return response
    
def update_item(id):
    response=get_item(id)
    item_type=response['fields']["System.WorkItemType"]
    print('Work item type', item_type)
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    #if (response['fields']["System.WorkItemType"] == 'Task') and (response['fields']['System.State']=='Deploy to test'):
    if (item_type == 'Task' or item_type == 'Bug'):
        state=response['fields']['System.State']
        assigned_to=response['fields']['System.AssignedTo']['displayName']
        print('assigned to:', assigned_to, ', Requester:', requester, ', State:', state)
        if  (state=='Deploy to test') and (requester==assigned_to) and (sourcebranch=='refs/heads/uat'):
            value='Ready to Test'
            response=patch_item(url,value)
            return response
        elif (state=='Code Review')and (requester==assigned_to) and (sourcebranch=='refs/heads/dev'):
            value='Deploy to Test'
            response=patch_item(url,value)
            return response
        elif (state=='In Progress') and (requester==assigned_to) and ('refs/pull' in sourcebranch):
            value='Code Review'
            response=patch_item(url,value)
            return response
        else:
            print('Cant patch item: State not "Deploy to test"/"Code review"/"In Progress"')
    else:
        print('Cant patch item: Not a "Task" or "Bug"')


output=get_related_work_item(buildId) #Get build related work items
print("Work items:", output)
count = output['count']
if count > 0:
    for i in range(count):
        response=update_item(output['value'][i]['id'])
        print('Patched:', response)
else:
    print('No related work items found')
