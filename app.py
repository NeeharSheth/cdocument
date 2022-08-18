import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID= 'AC5c271bc3245ad9ed22103e45c0d628fa'
    TWILIO_SYNC_SERVICE_SID= 'IS47beac9063d41c2a89c5d50851a2ee24'
    TWILIO_API_KEY= 'SK8a9457c7d43c4c8b729ea8a6920af18a'
    TWILIO_API_SECRET= 'jBvAjfaTCXNuhFJpDVod19BNThMKjR8v'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    textfrom_notepad= request.form['text']
    with open('workfile.txt','w') as wf:
        wf.write(textfrom_notepad)
    pathto_storedtext='workfile.txt'
    return send_file(pathto_storedtext,as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5000', debug=True)
