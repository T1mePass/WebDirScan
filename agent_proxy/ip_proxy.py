import random

def get_ip_proxy():

    ip_list = [
    {"http": "http://192.168.1.1:8080"},
    {"http": "http://123.456.789.10:8888"},
    {"http": "http://210.12.34.56:3128"},
    {"http": "http://5.67.89.10:8000"},
    {"http": "http://123.45.67.89:9999"},
    {"http": "http://67.89.101.112:8080"},
    {"http": "http://45.67.89.101:8888"},
    {"http": "http://210.112.34.56:3128"},
    {"http": "http://5.67.89.102:8000"},
    {"http": "http://123.45.67.90:9999"}
    ]

    return random.choice(ip_list)

print(get_ip_proxy())
