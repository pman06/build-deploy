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
print(response.json())
output=response.json()
count = output['count']
def get_item(id):
    fields=["System.WorkItemType","System.State"]
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?fields={fields}&api-version=7.0'
    response=requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def update_item(id):
    response=get_item(id)
    url=f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?validateOnly={validateOnly}&api-version=7.0'
    print(f'WorkItem = {response["System.WorkItemType"]}')
    if (response['System.WorkItemType'] == 'Task') and (response['System.State']=='Deploy to test'):
        json={
            'op': 'replace',
            'path': '/fields/System.State',
            'value':'Ready to UAT'
		}
        response=requests.patch(url, json=json, headers=headers)
        return response
    else:
        print('Cant patch item: not a task and not acive')

if count > 0:
    for i in range(count):
        update_item(output['value'][i]['id'])
        
