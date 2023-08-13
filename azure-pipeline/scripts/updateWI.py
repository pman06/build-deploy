# echo $SYSTEM_ACCESSTOKEN
# echo $Build.BuildId
# echo $System.CollectionId
# $organization=$System.CollectionId
# $project=$Build.TriggeredBy.ProjectID
# $buildId=$Build.BuildId
# $token=$SYSTEM_ACCESSTOKEN
import os
import requests

print(os.environ)
print(os.environ['SYSTEM_ACCESSTOKEN'])
print(os.environ['BUILD_BUILDID'])

buildId=os.environ['BUILD_BUILDID']
token=os.environ['SYSTEM_ACCESSTOKEN']
print(token)
project=os.environ['SYSTEM_TEAMPROJECT']
organization='cooclass'
build_url=f'https://dev.azure.com/{organization}/{project}/_apis/build/builds/160/workitems?api-version=7.0'
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(build_url, headers=headers)

output=response.json()
count = output['count']
def get_item(id):   
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    response=requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def update_item(id):
    response=get_item(id)
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    
    if (response['fields']["System.WorkItemType"] == 'Epic') and (response['fields']['System.State']=='Active'):
        data=[{
            'op': 'replace',
            'path': '/fields/System.State',
            'value':'Resolved'
		},]
        headers={'Authorization': f'Bearer {token}','Content-Type': 'application/json-patch+json', 'charset':'utf-8'}
        response=requests.patch(url, data=data, headers=headers)
        print(response.text)
        return response.json()
    else:
        print('Cant patch item: not a task and not acive')

if count > 0:
    for i in range(count):
        response= update_item(output['value'][i]['id'])
        print(response)
        
