import requests
import json
from datetime import datetime
import time


def authentication(url, username, password):
    """
    Авторизация админа

    :param url: сокет
    :param username: имя главного пользователя
    :param password: пароль
    :return: результат запроса
    """
    return requests.post("http://{}/login".format(url), data={'username': username, 'password': password})


def create_team(url, cookie, csrf, name, timezone, email, slack):
    """
    Создание команды в oncall

    :param url: сокет
    :param cookie: cookie авторизованного пользователя
    :param csrf: csrf-токен
    :param name: имя команды
    :param timezone: часовой пояс команды
    :param email: email команды
    :param slack: slack команды (#...)
    :return: результат запроса
    """
    return requests.post("http://{}/api/v0/teams".format(url), headers={"x-csrf-token": csrf},
                         data=json.dumps({"name": name, "scheduling_timezone": timezone, "email": email,
                                          "slack_channel": slack}),
                         cookies=cookie)


def create_user(url, cookie, csrf, name, full_name, phone_number, email):
    """
    Создание пользователя, добавление данных о пользователе.
    Возможно только в режиме debug

    :param url: сокет
    :param cookie: cookie авторизованного пользователя
    :param csrf: csrf-токен
    :param name: имя пользователя
    :param full_name: полное имя
    :param phone_number: номер телефона
    :param email: email пользователя
    :return: результат запросов
    """
    req1 = requests.post("http://{}/api/v0/users".format(url), headers={"x-csrf-token": csrf},
                         data=json.dumps({"name": name}), cookies=cookie)
    req2 = requests.put("http://{}/api/v0/users/{}".format(url, name), headers={"x-csrf-token": csrf},
                        data=json.dumps({"name": name, "full_name": full_name, "contacts": {"call": phone_number,
                                                                                            "sms": phone_number,
                                                                                            "email": email}}),
                        cookies=cookie)
    return [req1, req2]


def add_roster_to_team(url, cookie, csrf, team_name, roster_name):
    """
    Добавление списка сотрудников в команду

    :param url: сокет
    :param cookie: cookie авторизованного пользователя
    :param csrf: csrf-токен
    :param team_name: название команды
    :param roster_name: название списка сотрудников
    :return: результат запроса
    """
    return requests.post("http://{}/api/v0/teams/{}/rosters".format(url, team_name), headers={"x-csrf-token": csrf},
                         data=json.dumps({"name": roster_name}), cookies=cookie)


def add_user_to_roster(url, cookie, csrf, team_name, roster_name, user_name):
    """
    Добавление пользователя в список сотрудников команды

    :param url: сокет
    :param cookie: cookie авторизованного пользователя
    :param csrf: csrf-токен
    :param team_name: название команды
    :param roster_name: название списка членов команды
    :param user_name: имя пользователя
    :return: результат запроса
    """
    return requests.post("http://{}/api/v0/teams/{}/rosters/{}/users".format(url, team_name, roster_name),
                         headers={"x-csrf-token": csrf}, data=json.dumps({"name": user_name}), cookies=cookie)


def create_event(url, cookie, csrf, team_name, start_time, end_time, user_name, role):
    """
    Создание дежурства

    :param url: сокет
    :param cookie: cookie авторизованного пользователя
    :param csrf: csrf-токен
    :param team_name: название команды, в которой проходит дежурство
    :param start_time: начало дежурства
    :param end_time: окончание дежурства
    :param user_name: имя дежурящего
    :param role: роль дежурного
    :return: результат запроса
    """
    return requests.post("http://{}/api/v0/events".format(url), headers={"x-csrf-token": csrf},
                         data=json.dumps({"start": time.mktime(start_time.timetuple()),
                                          "end": time.mktime(end_time.timetuple()), "user": user_name,
                                          "team": team_name, "role": role}), cookies=cookie)