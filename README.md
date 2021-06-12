CS172 Spring 2021 Final Project

David May dmay004 
Stanley Zhao szhao050
Lindsey Young lyoun009

The code is designed to crawl through the text file containing our seed URLs, and then stop after 60 seconds, populating our htmls folder with all of the text scraped from the web. The indexer.sh file must then be run by a user, to generate the index and organize the data into documents, as well as bulk load said documents through our data.json file. The flask server app.py can then be run to launch a web application on localhost:5000. Users can submit a query and navigate to localhost:5000/shell to view the query results. 

Below are the detailed steps to run the program. 

1. run “python3 crawler.py”, or whatever your python compile command is. The crawler will exit automatically after 60 seconds.
2. run “./indexer.sh”, and then create a new index when prompted, afterwards, press “b” to bulk load the index
3. run “python3 app.py” 
4. navigate to localhost:5000 on your browser
5. submit a query in the text box
6. view the results on localhost:5000/shell
