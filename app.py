from flask import Flask
import subprocess
from subprocess import check_output
 
def get_shell_script_output_using_check_output():
    stdout = check_output(['./output.sh']).decode('utf-8')
    return stdout
 
app = Flask(__name__)
 
@app.route('/',methods=['GET',])
def home():
    return '<pre>'+get_shell_script_output_using_check_output()+'</pre>'
 
app.run(debug=True)
 
if __name__ == "__main__":
  app.run()