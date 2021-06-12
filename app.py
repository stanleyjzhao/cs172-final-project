from flask import request, render_template
from flask import Flask
import subprocess
from subprocess import check_output

def call_shell():
    subprocess.call(['bash','output.sh', my_form_input()])
    stdout = check_output(['./output.sh']).decode('utf-8')
    return stdout
 
app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('webpage.html')

@app.route('/', methods=['POST'])
def my_form_input():
    varinput = request.form['text']
    return varinput

@app.route('/',methods=['GET',])
def home():
    return '<pre>'+call_shell()+'</pre>'
 
app.run(debug=True)
 
if __name__ == "__main__":
  app.run()