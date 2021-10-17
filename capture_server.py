from flask import Flask, request
from flask_cors import CORS
import os, subprocess
import urllib.parse

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.debug = True
PORT = 8083
CORS(app)

@app.route('/',methods=['POST'])
def camera_start():

    print("Using key: ",request.json['aws-key'])

    # Need to run the CV2 in a new instance because it glitches under a flask server
    new_process = subprocess.Popen(
        f"/bin/python3 capture_run.py {urllib.parse.quote(request.json['aws-key'])}", 
        stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    )

    r_data = request.json['aws-key']
    
    for s_out in new_process.stdout:
        print(bytearray(s_out).decode())

        if bytearray(s_out).decode() == "cancelled":
            r_data = "cancel_upload"
            
    return(r_data+".jpg",200)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=PORT)