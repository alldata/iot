#!/usr/bin/python

# -*- coding: utf-8 -*-
import requests
import json
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
    #return res.json()['current']
    values = {}
    for i in res.json()['current']['values']:
        if i['name'] != 'PM1':
            values.update({i['name'].lower(): float(i['value'])})
    return [
        {
            'measurement': 'AQI',
            'time': res.json()['current']['tillDateTime'],
            'tags': {
                'installationId': AIRLY_INSTALLATIONS[installation_id],
            },
            "fields": values
        }
    ]

def get_kaiterra(apikey, device):
    res = requests.get("https://api.origins-china.cn/v1/lasereggs/{}?key={}".format(device, apikey))
    #return res.json()
    values = res.json()['info.aqi']['data']
    values['temperature'] = values.pop('temp')
    for key in values:
        values[key] = float(values[key])
    #return values
    return [
        {
            'measurement': 'Kaiterra',
            'time': res.json()['info.aqi']['ts'],
            'fields': values
        }
    ]

def wite_influxdb(points):
    client = InfluxDBClient(
        host='localhost',
        port=8086,
        database='iot')
    client.write_points(points=points, time_precision='s')

#print(json.dumps(get_airly('HJfUiZzCISMwQpluHJlbf8E2miSzPvns', 60), indent=4, sort_keys=True))
print(json.dumps(get_kaiterra('NzFlMmFlYWU5NjEyNDllYWE4ZDcxZTQ0Zjc0N2Q1NGU5ZDRi', '20044aaf45ee4321b1da548f1370df13'), indent=4, sort_keys=True))
#wite_influxdb(get_kaiterra('NzFlMmFlYWU5NjEyNDllYWE4ZDcxZTQ0Zjc0N2Q1NGU5ZDRi', '20044aaf45ee4321b1da548f1370df13'))
#for installation_id in AIRLY_INSTALLATIONS:
#wite_influxdb(get_airly('HJfUiZzCISMwQpluHJlbf8E2miSzPvns', 228))
