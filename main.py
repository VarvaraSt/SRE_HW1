import sys
import yaml
import json
import api_functions
from datetime import datetime, timedelta

# Путь к файлу с информацией о командах
path = sys.argv[1]
# ip адрес и порт ip:port
url = sys.argv[2]
print("Авторизация...")
auth_r = api_functions.authentication(url, "root", "1234")
cookie = auth_r.cookies
csrf = json.loads(auth_r.content.decode('utf-8'))["csrf_token"]

with open(path, "r") as file:
    print("Чтение файла...")
    data = yaml.load(file, Loader=yaml.FullLoader)

    print("Создание графика дежурств...")
    # Создание команд
    for team in data['teams']:
        api_functions.create_team(url, cookie, csrf, team["name"], team["scheduling_timezone"], team["email"],
                                  team["slack_channel"])
        api_functions.add_roster_to_team(url, cookie, csrf, team["name"], "team_members")
        # Создание пользователей
        for user in team['users']:
            # Для успешного создания пользователей должен быть активирован режим debug
            api_functions.create_user(url, cookie, csrf, user["name"], user["full_name"], user["phone_number"],
                                      user["email"])
            api_functions.add_user_to_roster(url, cookie, csrf, team["name"], "team_members", user["name"])
            # Создание дежурств
            for event in user['duty']:
                print(datetime.strptime(event['date'], "%d/%m/%Y"))
                api_functions.create_event(url, cookie, csrf, team["name"],
                                           datetime.strptime(event['date'], "%d/%m/%Y"),
                                           datetime.strptime(event['date'], "%d/%m/%Y") + timedelta(days=1),
                                           user["name"], event["role"])

print("Готово")
