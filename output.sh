#!/bin/bash

echo "test"

curl -X GET -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/ucr/_search?pretty" -H 'Content-Type: application/json' -d "{\"query\": {\"match\": {\"html\":\"Riverside\"}}}"