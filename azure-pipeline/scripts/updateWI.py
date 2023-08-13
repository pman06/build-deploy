# echo $SYSTEM_ACCESSTOKEN
# echo $Build.BuildId
# echo $System.CollectionId
# $organization=$System.CollectionId
# $project=$Build.TriggeredBy.ProjectID
# $buildId=$Build.BuildId
# $token=$SYSTEM_ACCESSTOKEN
# $url='https://dev.azure.com/{organization}/{project}/_apis/build/builds/{buildId}/workitems?api-version=7.0'
# $authorization="Bearer $token"
# curl()

import os
import requests

print(os.environ)
print(os.environ['SYSTEM_ACCESSTOKEN'])
print(os.environ['BUILD_BUILDID'])

buildId=os.environ['BUILD_BUILDID']
token=os.environ['SYSTEM_ACCESSTOKEN']
project=os.environ['SYSTEM_TEAMPROJECT']
organization='cooclass'
url=f'https://dev.azure.com/{organization}/{project}/_apis/build/builds/{buildId}/workitems?api-version=7.0'

response = requests.get(api_url, headers=headers)
print(response.json())
