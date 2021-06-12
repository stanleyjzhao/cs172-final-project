from flask import request, render_template
from flask import Flask
import os
import subprocess
from subprocess import check_output

def call_shell():
    os.system(" ./output.sh covid > test.txt")
    # subprocess.call(['bash','output.sh', "ucr"])
    stdout = check_output(['./output.sh']).decode('utf-8')
    
    return stdout
 
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('webpage.html')

@app.route('/', methods=['POST'])
def my_form_input():
    varinput = request.form['text']
    print (varinput)
    return varinput

@app.route('/shell',methods=['GET',])
def home():
    call_shell()

    with open("test.txt", "r") as f:
      content = f.read()
    return render_template('printed.html', content=content)
 
app.run(debug=True)
 
if __name__ == "__main__":
  app.run()