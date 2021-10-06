import requests

def get_C2_info(url):
    r = requests.get(url)
    ip = r.text.split(':')[0]
    port = r.text.split(':')[1]
    return ip, int(port)
