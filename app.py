from flask import Flask,request
import subprocess
from bash import bash

app = Flask(__name__)


@app.route('/reset', methods=["POST"])
def reset():
    password = str(request.form['resetpassword'])
    valuer1  = str(request.form['activity'])
    bash('sudo systemctl stop readservice.service')
    cmd2 = f'python3 /home/karthik/NFCserver/writecard.py {password} {valuer1}'
    process = subprocess.Popen(['/bin/bash', '-c', cmd2], stdout=subprocess.PIPE)
    out = list(process.communicate())
    bash('sudo systemctl start readservice.service')
    return out[0].decode()
    

@app.route('/register', methods=["POST"])
async def register():
    rpassword = str(request.form['registerpassword'])
    valuel1 = str(request.form['activity'])
    bash('sudo systemctl stop readservice.service')
    cmd3 = f'python3 /home/karthik/NFCserver/writecard.py {rpassword} {valuel1}'
    process1 = subprocess.Popen(['/bin/bash', '-c', cmd3], stdout=subprocess.PIPE)
    out1 = list(process1.communicate())
    bash('sudo systemctl start readservice.service')
    return str(out1[0].decode())
