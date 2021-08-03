import requests
import json

def get_ip():
    r = requests.get("https://api.ipify.org?format=json'")
    g = requests.get("http://ip-api.com/json/" + r.text)
    data = dict()
    data['ip'] = r.text
    geo = json.loads(g.content)
    for key in geo.keys():
        if key not in ['status', 'query']:
            data[key] = geo[key]
    return data
