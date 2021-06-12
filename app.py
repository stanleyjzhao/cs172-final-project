from flask import request, render_template
from flask import Flask
import os
import subprocess
from subprocess import check_output

def call_shell():
    # my_form_input('text')
    with open("formInput.txt", "r") as f:
        input = f.read()
    print(input)
    os.system(" ./output.sh {var} > test.txt".format(var = input))
    return

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('webpage.html')

@app.route('/', methods=['POST'])
def my_form_input():
    varinput = request.form['text']
    with open("formInput.txt", "w") as f:
        f.write(varinput)
        f.close()
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