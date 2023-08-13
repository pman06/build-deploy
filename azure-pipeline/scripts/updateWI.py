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
print(os.environ)
print(os.environ['SYSTEM_ACCESSTOKEN'])
