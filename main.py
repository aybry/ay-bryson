import json
import logging
import time

from flask import Flask, url_for, render_template, request
from gcloud import storage


app = Flask(__name__)

client = storage.Client()
# bucket = client.get_bucket('ay-bryson')
bucket_list = [bucket for bucket in client.list_buckets()]
bucket_path_list = [bucket.path for bucket in bucket_list]

bucket = bucket_list[bucket_path_list.index('/b/ay-bryson.appspot.com')]


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('base.html')
    
    elif request.method == 'POST':
        save_rsvp(request.form)
        return render_template('base.html', msg="Thanks for letting us know!")

        
def save_rsvp(form_data):
    rsvp = json.dumps(form_data.to_dict())
    blob = bucket.blob(f'data/{round(time.time())}.txt')
    blob.upload_from_string(rsvp)


if __name__ == '__main__':
    app.run(debug=True)