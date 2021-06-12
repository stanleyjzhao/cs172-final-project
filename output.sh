#!/bin/bash

echo $1

curl -X GET -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_search?pretty" -H 'Content-Type: application/json' -d "{\"query\": {\"match\": {\"html\":\"$1\"}}}"

