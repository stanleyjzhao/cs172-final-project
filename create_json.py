import os
import glob
import json

files = glob.glob('htmls/*')
os.system("rm data.json")
count = 1
for f in files:
    with open(f, "r") as html_file:
        firstLine = html_file.readline()
        firstLine = firstLine.rstrip()
        print(firstLine)
        html = html_file.read()
        # remove whitespace & unicode before placing in json:
        html = html.encode("ascii", "ignore")
        html = html.decode()
        html = html.rstrip()
        html = html.lstrip()
        html = html.strip("\n\t\r")
        html = html.replace("\n\t\t\t", "")
        html = html.replace("\n", " ")

        # print(html)
        x = {"index": {"_id": "" + str(count) + ""}}
        x2 = {"link": firstLine, "html": html} 
        
    with open("data.json", "a") as file:
        json.dump(x, file)
        file.write("\n")
        json.dump(x2, file)
        file.write("\n")
    count += 1

file = open("data.json", "a")
file.write('\n')
file.close()
      
