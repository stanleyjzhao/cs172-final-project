#!/bin/bash

echo "Please enter name of index:"
read index

        curl -X PUT -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/cs172index?pretty" -H 'Content-Type: application/json' -d'{
        "settings": {
            "analysis": {
            "analyzer": {
                "htmlStripAnalyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase"],
                "char_filter": [ "html_strip" ]
                }
            }
            }
        },"mappings": {
            "properties": {
                "html": {
                "type": "text",
                "analyzer": "htmlStripAnalyzer"
                }
            }
        }
        }' &> log.txt

echo
if grep -Fxq "already exists" log.txt
then
    echo "${index} doesn't exist, created new index, ${index}"
else
    echo "${index} already exists, accessing ${index}"
fi

echo
echo "Commands to run indexer:"
echo

echo "c - check status (health) of instance"
echo "s - put in single document"
echo "a - retrieve all documents"
echo "r - retrieve documents with specific word"
echo "b - bulk load documents via JSON"
echo "d - delete all documents in index"
echo "q - quit"


read option
while [[ [[$option != 'q']] ]]
do
    if [[ $option == 'c' ]]; then
        echo "Checking health of cluster..."
        curl -X GET -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/_cluster/health?pretty"
        
    elif [[ $option == 's' ]]; then
        echo "Please enter in a document (ie. like \"<td><tr>test<td </tr>\" )"
        read doc
        curl -X PUT -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_doc/1" -H 'Content-Type: application/json' -d'{"html": "${doc}"}'
        
    elif [[ $option == 'a' ]]; then
        echo "Retrieving all documents from ${index}..."
        curl -X GET -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_search?pretty" -H 'Content-Type: application/json' -d'
        {
        "query": {
            "match_all": { }
        }
        }
        '
        
    elif [[ $option == 'r' ]]; then
        echo "Please enter a word you would like to retrieve by (ie. \"ucr\"): "
        read word
                                                                                                                                                                               
        curl -X GET -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_search?pretty" -H 'Content-Type: application/json' -d "{\"query\": {\"match\": {\"html\":\" $word \"}}}"
        
    elif [[ $option == 'b' ]]; then
        echo "Creating JSON file to load..."
        python3 create_json.py
        echo "Bulk loading documents into ${index}..."
        curl -X POST -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_bulk" -H "Content-Type: application/x-ndjson" --data-binary @data.json
        
    elif [[ $option == 'd' ]]; then
        echo "Deleting all documents in ${index}..."
        curl -X POST -u elastic:9GObQ236qhyZLDb3gbccg0fx "https://cs172-b03cf7.es.us-west1.gcp.cloud.es.io:9243/${index}/_delete_by_query?pretty" -H 'Content-Type: application/json' -d'
        {
        "query": {
            "match_all": {
            
            }
        }
        }
        '

    elif [[ $option == 'q' ]]; then
        echo "Quiting..."
        rm log.txt
        break
    else
    echo "not valid option, try again"
    read option
    fi

    echo
    echo "Commands to run indexer:"
    echo
    echo "c - check status (health) of instance"
    echo "s - put in single document"
    echo "a - retrieve all documents"
    echo "r - retrieve documents with specific word"
    echo "b - bulk load documents via JSON"
    echo "d - delete all documents in index"
    echo "q - quit"
    read option
done