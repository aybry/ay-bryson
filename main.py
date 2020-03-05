import json
import logging
import time
import os
import urllib3
import string
import random

from flask import Flask, flash, url_for, render_template, request, redirect
from gcloud import storage
from pprint import pprint
from urllib.parse import quote


app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_letters) for i in range(24))


@app.route('/', methods=['GET', 'POST'])
def home():
    user_lang = get_language(request)

    static_photo_urls = [
        url_for('static', filename=f'photos/{photo_fn}') for photo_fn in sorted(os.listdir(
            os.path.join(os.getcwd(), 'static', 'photos')
        ))
    ]
    context = {
        'static_photo_urls': static_photo_urls,
        'n_photos': len(static_photo_urls),
        'loc': LOC,
        'lang': user_lang,
    }
    return render_template('base.html', **context)


@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    user_lang = get_language(request)

    if request.method == 'GET':

        context = {
            'loc': LOC,
            'lang': user_lang,
        }

        return render_template('rsvp.html', **context)

    elif request.method == 'POST':
        rsvp_worked = process_rsvp(request.form)

        rsvp_messages = {
            'rsvp-success': {
                'en': 'Thanks! We will be in touch closer to the date.',
                'de': 'Danke! Wir melden uns zu einem späteren Zeitpunkt.',
                'cat': 'mu mu-pass mu-green',
            },
            'rsvp-nosuccess': {
                'en': 'Something didn\'t quite work there... Please try again or send us an email.',
                'de': 'Das hat nicht geklappt... Bitte versuche es nochmal, oder schicke uns eine Email.',
                'cat': 'mu mu-fail mu-red',
            }
        }

        context = {}

        if rsvp_worked:
            message = (rsvp_messages['rsvp-success'][user_lang],
                       rsvp_messages['rsvp-success']['cat'])
            flash(*message)
        else:
            message = (rsvp_messages['rsvp-nosuccess'][user_lang],
                       rsvp_messages['rsvp-nosuccess']['cat'])
            flash(*message)

        return redirect(url_for('home'))


@app.route('/btc', methods=['GET', 'POST'])
def btc():
    user_lang = get_language(request)

    context = {
        'loc': LOC,
        'lang': user_lang,
    }

    return render_template('btc.html', **context)


def process_rsvp(form_data):
    try:
        rsvp = form_data.to_dict()

        save_rsvp(rsvp)
        send_notification(rsvp)

        return True

    except:
        return False


def save_rsvp(rsvp):
    ts = round(time.time())
    try:
        last_name = rsvp.get('name').split()[-1]
    except:
        last_name = 'No_Name'
    rsvp_fp = f'data/{ts}_{last_name}.txt'

    if PRODUCTION:
        blob = bucket.blob(rsvp_fp)
        blob.upload_from_string(json.dumps(rsvp))
    else:
        with open(rsvp_fp, 'w+') as rsvp_f:
            json.dump(rsvp, rsvp_f, indent=4)

def send_notification(rsvp):
    if PRODUCTION:
        chat_id = '-361617952'
    else:
        chat_id = '474539046'

    message = get_message(rsvp)

    notify_bot_token = '527000621:AAGvB7oAC-TMcPqQKDNX0vcYZ2_HTpmwVzk'
    notify_bot_site = f'https://api.telegram.org/bot{notify_bot_token}'
    url = f'{notify_bot_site}/sendmessage?chat_id={chat_id}&text={message}&parse_mode=Markdown'
    http = urllib3.PoolManager()
    http.request('GET', url)


def get_bucket():
    client = storage.Client()
    bucket_list = [bucket for bucket in client.list_buckets()]
    bucket = bucket_list[[bucket.path for bucket in bucket_list].index(
        '/b/ay-bryson.appspot.com')]
    return client, bucket


def get_message(form_data):
    name = form_data['name']
    email = form_data['email']
    attending = ('Yes (' + form_data['attendees'] + ')') if form_data['attending'] == '1' else 'No'
    message = form_data['message']
    notification = f'*Name:* {name}\n*Email:* {email}\n*Attending:* {attending}'
    if message != '':
        notification += f'\n*Message:* {message}'
    return quote(notification)


def get_language(request):
    we_speak = ['en', 'de']
    try:
        options = request.headers.get('Accept-Language').split(',')
    except AttributeError:
        return 'en'

    options_first = [option.split('-')[0] for option in options]

    for option_f in options_first:
        if option_f in we_speak:
            return option_f
        elif option_f == 'tr':
            return 'de'

    return 'en'


def parse_strings():
    with open('./static/locale/strings.txt', 'r') as loc_f:
        str_lines = loc_f.readlines()

    loc = {}

    for line, l_en, l_de in zip(str_lines[::4], str_lines[1::4], str_lines[2::4]):
        loc[line.replace('\n', '')] = {
            'en': l_en[3:].replace('\n', ''),
            'de': l_de[3:].replace('\n', ''),
        }

    return loc


if '__non_prod__.txt' in os.listdir():
    PRODUCTION = False
    if 'data' not in os.listdir():
        os.mkdir('data')
else:
    PRODUCTION = True
    client, bucket = get_bucket()


LOC = parse_strings()


if __name__ == '__main__':
    if PRODUCTION:
        app.run()
    else:
        app.run(
            debug=True,
            host='0.0.0.0',
        )
