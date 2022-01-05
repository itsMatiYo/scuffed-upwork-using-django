import requests
from decouple import config

BASE_AUTH = config('BASE_AUTH')
HOST = config('HOST')
TOKEN = config('TOKEN')


def update_roles():
    with open("settings.ini", 'r') as reader:
        get_all = reader.readlines()
    response = requests.post(
        url=HOST + "/admin/role", headers={'auth_basic': BASE_AUTH, 'Authorization': TOKEN, }
    )
    if response.json()['status'] == True:
        roles = response.json()['data']
        for role in roles:
            if role['name'] == "employee":
                ROLE_ID_EMPLOYEE = role['id']
            if role['name'] == "visitor":
                ROLE_ID_VISITOR = role['id']
            if role['name'] == "customer":
                ROLE_ID_CUSTOMER = role['id']
            if role['name'] == "city_admin":
                ROLE_ID_CITYADMIN = role['id']
        with open('settings.ini', 'w') as reader:
            for i, line in enumerate(get_all, 1):
                if i == 8:
                    reader.writelines("ROLE_ID_EMPLOYEE = " +
                                      ROLE_ID_EMPLOYEE+"\n")
                elif i == 9:
                    reader.writelines("ROLE_ID_VISITOR = " +
                                      ROLE_ID_VISITOR+"\n")
                elif i == 10:
                    reader.writelines("ROLE_ID_CUSTOMER = " +
                                      ROLE_ID_CUSTOMER+"\n")
                elif i == 11:
                    reader.writelines("ROLE_ID_CITYADMIN = " +
                                      ROLE_ID_CITYADMIN+"\n")
                else:
                    reader.writelines(line)
        print("************Roles Update************")
    else:
        print("************Roles not Update************")
