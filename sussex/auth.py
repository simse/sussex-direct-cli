import os
import pickledb
import requests
from pathlib import Path

try:
    os.makedirs(str(Path.home() / '.sussex'))
except(FileExistsError):
    pass

db = pickledb.load(str(Path.home() / '.sussex' / '.auth'), False)

def save_session_id(sessid):
    db.set('session_id', sessid)
    db.dump()


def read_session_id():
    if not db.get('session_id'):
        save_session_id(get_new_session_id())
    else:
        return db.get('session_id')

def clear_session_id():
    if db.get('session_id'):
        db.rem('session_id')


def get_new_session_id():
    session = requests.Session()
    session.get('https://direct.sussex.ac.uk')
    return session.cookies.get_dict()['PHPSESSID']


def save_login(username, password):
    db.set('sussex_username', username)
    db.set('sussex_password', password)
    db.dump()

    return True


def verify_login_status():
    login()

    if make_get('https://direct.sussex.ac.uk/page.php?realm=home').history:
        return False
    else:
        return True


def login():
    requests.post('https://direct.sussex.ac.uk/login.php', data = {
        'username': db.get('sussex_username'),
        'password': db.get('sussex_password'),
        'QUERY_STRING': None,
        'js_enabled': 0
    }, cookies = {
        'PHPSESSID': read_session_id()
    }, headers={
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Origin': 'https://direct.sussex.ac.uk',
        'Referer': 'https://direct.sussex.ac.uk/login.php',
        'Upgrade-Insecure-Requests': '1'
    })


def make_get(url, payload=None):
    return requests.get(
        url, 
        data = payload,
        cookies = {
            'PHPSESSID': read_session_id()
        }
    )


def make_post(url):
    pass
