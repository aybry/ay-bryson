import json
import logging
import time
import os

from flask import Flask, url_for, render_template, request
from gcloud import storage


app = Flask(__name__)
SECRET_KEY = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')
    

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if request.method == 'GET':
        return render_template('rsvp.html')

    elif request.method == 'POST':
        save_rsvp(request.form)
        return render_template('base.html')

        
def save_rsvp(form_data):
    rsvp = form_data.to_dict()
    ts = round(time.time())
    rsvp_fp = f'data/{ts}.txt'

    if PRODUCTION:
        blob = bucket.blob(rsvp_fp)
        blob.upload_from_string(json.dumps(rsvp))
    else:
        with open(rsvp_fp, 'w+') as rsvp_f:
            json.dump(rsvp, rsvp_f, indent=4)


def get_bucket():
    client = storage.Client()
    bucket_list = [bucket for bucket in client.list_buckets()]
    bucket = bucket_list[[bucket.path for bucket in bucket_list].index('/b/ay-bryson.appspot.com')]
    return client, bucket


if '__non_prod__.txt' in os.listdir():
    PRODUCTION = False
    if 'data' not in os.listdir():
        os.mkdir('data')
else:
    PRODUCTION = True
    client, bucket = get_bucket()


if __name__ == '__main__':
    debug = not PRODUCTION
    app.run(
        debug=debug,
        host='0.0.0.0'
    )