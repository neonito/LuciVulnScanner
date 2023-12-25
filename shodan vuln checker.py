import threading
import requests
import subprocess

url_template = 'https://internetdb.shodan.io/{}'
num_threads = 10
def make_request(ip):
    url = url_template.format(ip)
    response = requests.get(url)
    print(f'Response for {ip}: {response.status_code}')
    if 'CVE' in response.text:
        with open('vuln.txt', 'a') as f:
            f.write(ip + '\n')
with open('ip.txt', 'r') as f:
    ip_list = f.read().splitlines()
threads = []
for ip in ip_list:
    thread = threading.Thread(target=make_request, args=(ip,))
    threads.append(thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
api_key = ''
url = f'https://api.ipdata.co/'
with open('vuln.txt', 'r') as f:
    ip_addresses = f.read().splitlines()
def get_country(ip):
    response = requests.get(url + ip + '?api-key=' + api_key)
    if response.status_code == 200:
        return response.json()['country_name']
    else:
        return "unknown"
with open('country_ip_output.txt', 'w') as f:
    for ip in ip_addresses:
        try:
            country = get_country(ip)
            print(f"{ip} ({country})")
            f.write(f"{ip} ({country})\n")
        except Exception as e:
            print(f"{ip} - error: {e}")
            f.write(f"{ip} (unknown)\n")