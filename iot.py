#!/usr/bin/python

#*/5 * * * * /home/ec2-user/iot/iot.py 1
#*/5 * * * * /home/ec2-user/iot/iot.py 2
#0 * * * * /home/ec2-user/iot/iot.py 3

# -*- coding: utf-8 -*-
import sys
import requests
from influxdb import InfluxDBClient

AIRLY_INSTALLATIONS = {
    18: 'Halszki',
    58: 'Dietla',
    60: 'Racheli',
    228: 'Obozowa',
    1070: 'Geremka'
}

def get_airly(apikey, installation_id):
    headers = {'Accept': 'application/json', 'apikey': apikey}
    res = requests.get("https://airapi.airly.eu/v2/measurements/installation?installationId={}".format(installation_id),
        headers=headers)
    values = {}
    for i in res.json()['current']['values']:
        if i['name'] != 'PM1':
            values.update({i['name'].lower(): float(i['value'])})
    return [
        {
            'measurement': 'Airly',
            'time': res.json()['current']['tillDateTime'],
            'tags': {
                'installationId': AIRLY_INSTALLATIONS[installation_id],
            },
            'fields': values
        }
    ]

def get_kaiterra(apikey, device):
    res = requests.get("https://api.origins-china.cn/v1/lasereggs/{}?key={}".format(device, apikey))
    values = res.json()['info.aqi']['data']
    values['temperature'] = values.pop('temp')
    for key in values:
        values[key] = float(values[key])
    return [
        {
            'measurement': 'Kaiterra',
            #'time': res.json()['info.aqi']['ts'],
            'fields': values
        }
    ]

def wite_influxdb(points):
    client = InfluxDBClient(
        host='localhost',
        port=8086,
        database='iot')
    client.write_points(points=points, time_precision='s')

if sys.argv[1] == '1':
    wite_influxdb(get_kaiterra('NzFlMmFlYWU5NjEyNDllYWE4ZDcxZTQ0Zjc0N2Q1NGU5ZDRi', '20044aaf45ee4321b1da548f1370df13'))
if sys.argv[1] == '2':
    for installation_id in [228, 1070]:
        wite_influxdb(get_airly('HJfUiZzCISMwQpluHJlbf8E2miSzPvns', installation_id))
if sys.argv[1] == '3':
    for installation_id in [18, 58, 60]:
        wite_influxdb(get_airly('HJfUiZzCISMwQpluHJlbf8E2miSzPvns', installation_id))
