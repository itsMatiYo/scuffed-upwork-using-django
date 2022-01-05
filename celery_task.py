
"""
! Why : 
? for some sections we need a admin Token , so we should refresh admin token ...

! How it work ? 
? 1:sudo docker run -d -p 6379:6379 redis
? 2:celery -A celery_task beat
? 3:celery -A celery_task worker -B
"""

from celery import Celery
from decouple import config
import requests

BASE_AUTH = config('BASE_AUTH')
HOST = config('HOST')
REFRESH_TOKEN = config('REFRESH_TOKEN')

app = Celery('task', broker='redis://localhost:6379/0')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, change_token.s(),  # ! change it
                             name='change_token every 5 sec')


@app.task
def change_token():
    # * open file and read all lines
    with open("settings.ini", 'r') as reader:
        get_all = reader.readlines()
    # * send refresh token
    response = requests.post(
        url=HOST + "/update-token", data={"refresh_token": REFRESH_TOKEN}, headers={'auth_basic': BASE_AUTH, }
    )
    new_token = response.json()["data"]['token']
    new_refresh_token = response.json()["data"]['refresh_token']
    # * change token and refresh token value on settings.ini
    with open('settings.ini', 'w') as reader:
        for i, line in enumerate(get_all, 1):
            if i == 2:
                reader.writelines("TOKEN = "+new_token+"\n")
            elif i == 3:
                reader.writelines("REFRESH_TOKEN = "+new_refresh_token+"\n")
            else:
                reader.writelines(line)
    print("Token Updated")
