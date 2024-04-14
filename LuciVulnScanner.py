import threading
import requests
import json

api_ipdata = ''

def shodan_request(ip):
    resp = requests.get(f'https://internetdb.shodan.io/{ip}')
    return resp

def ipdata_request(ip):
    resp = requests.get(f'https://api.ipdata.co/{ip}?api-key={api_ipdata}')
    return resp

def ip_info(ip, columns, summary):
    resp_shodan = shodan_request(ip)
    honeypot = "none"
    vulns = "none"
    is_tor = "none"
    is_vpn = "none"
    is_proxy = "none"
    is_datacenter = "none"
    is_anonymous = "none"
    is_known_attacker = "none"
    is_known_abuser = "none"
    is_threat = "none"
    country_name = "none"
    
    if resp_shodan.status_code == 200:
        data = resp_shodan.json()
        vulns = data.get("vulns", [])
        if not vulns:
            vulns = "not found"
        else:
            summary["vulns"] += len(vulns)
        honeypot = "yes" if "honeypot" in data.get("tags", []) else "no"
        is_vpn = "yes" if "vpn" in data.get("tags", []) else "no"
    
    resp_ipdata = ipdata_request(ip)
    
    if resp_ipdata.status_code == 200:
        data = resp_ipdata.json()
        country_name = data.get("country_name", "unknown")
        is_tor = "yes" if data["threat"].get("is_tor", False) else "no"
        is_proxy = "yes" if data["threat"].get("is_proxy", False) else "no"
        is_datacenter = "yes" if data["threat"].get("is_datacenter", False) else "no"
        is_anonymous = "yes" if data["threat"].get("is_anonymous", False) else "no"
        is_known_attacker = "yes" if data["threat"].get("is_known_attacker", False) else "no"
        is_known_abuser = "yes" if data["threat"].get("is_known_abuser", False) else "no"
        is_threat = "yes" if data["threat"].get("is_threat", False) else "no"

    columns.append({
        "ip": ip,
        "country_name": country_name,
        "vulns": vulns,
        "honeypot": honeypot,
        "tor": is_tor,
        "vpn": is_vpn,
        "proxy": is_proxy,
        "datacenter": is_datacenter,
        "anonymous": is_anonymous,
        "attacker": is_known_attacker,
        "abuser": is_known_abuser,
        "threat": is_threat
    })

    summary["vulns"] += len(vulns)
    summary["honeypot"] += 1 if honeypot == "yes" else 0
    summary["tor"] += 1 if is_tor == "yes" else 0
    summary["vpn"] += 1 if is_vpn == "yes" else 0
    summary["proxy"] += 1 if is_proxy == "yes" else 0
    summary["datacenter"] += 1 if is_datacenter == "yes" else 0
    summary["anonymous"] += 1 if is_anonymous == "yes" else 0
    summary["attacker"] += 1 if is_known_attacker == "yes" else 0
    summary["abuser"] += 1 if is_known_abuser == "yes" else 0
    summary["threat"] += 1 if is_threat == "yes" else 0

try:
    with open('ip.txt', 'r') as f:
        headers = ["ip", "country_name", "vulns", "honeypot", "tor", "vpn", "proxy", "datacenter", "anonymous", "attacker", "abuser", "threat"]
        columns = []
        summary = {
            "vulns": 0,
            "honeypot": 0,
            "tor": 0,
            "vpn": 0,
            "proxy": 0,
            "datacenter": 0,
            "anonymous": 0,
            "attacker": 0,
            "abuser": 0,
            "threat": 0
        }
        threads = []
        
        for ip in f.read().splitlines():
            thread = threading.Thread(target=ip_info, args=(ip, columns, summary,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        with open("output.json", "w") as json_file:
            json.dump({"summary": summary, "ip_details": columns}, json_file, indent=2)

        print(f"Summary:")
        print(f"Total Vulns: {summary['vulns']}")
        print(f"Honeypot: {summary['honeypot']}")
        print(f"TOR: {summary['tor']}")
        print(f"VPN: {summary['vpn']}")
        print(f"Proxy: {summary['proxy']}")
        print(f"Datacenter: {summary['datacenter']}")
        print(f"Anonymous: {summary['anonymous']}")
        print(f"Attacker: {summary['attacker']}")
        print(f"Abuser: {summary['abuser']}")
        print(f"Threat: {summary['threat']}")
        print(f"Total IPs with Vulns: {len([ip for ip_detail in columns if ip_detail['vulns'] != 'not found' and len(ip_detail['vulns']) > 0])}")

except FileNotFoundError:
    print("no 'ip.txt' file")
