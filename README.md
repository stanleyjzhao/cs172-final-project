# CS172 - Assignment 1 (Tokenization)

## Team member 1 - David May dmay004
## Team member 2 - Stanley Zhao szhao050

###### Provide a short explanation of your design
###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 

Uses dict variables to store the tokenized words, where the key is the ID of the word and the value contains the token, and information about the token, such as frequency, position, and associated documents. 

Document IDs and names are stored in similar dictionaries, and the user-inputted arguments will pull data from specific parts of each relevant dictionary.

The read_index.py file uses the python library sys in order to make use of the sys.argv[] built-in function that allows us to access the passed in arguments. 

Language: Python 3
read_index.py is runnable with query arguments in the form --term TERM or --doc DOCUMENT or both.

Ex:
python3 .\read_index.py --term said --doc ap890101-0001

We did not attempt the extra credit.