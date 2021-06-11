import os
import glob
import json

files = glob.glob('htmls/*')
os.system("rm data.json")
for f in files:
    with open(f, "r") as html_file:
        html = html_file.read()
        x = {"index": "{}"}
        x2 = {"html": html}   
        
    with open("data.json", "a") as file:
        json.dump(x, file)
        file.write("\n")
        json.dump(x2, file)
        file.write("\n")
      
