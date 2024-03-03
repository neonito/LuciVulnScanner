# neonito-vuln-checker.py

## Description

The script collect information about IP addresses from the `ip.txt` file using queries to shodan and ipdata.co services. It then generates a JSON file with the data and displays a summary on the console. Additionally, the script checks for vulnerabilities (CVEs) associated with each IP address, as well as other characteristics such as honeypot, tor, vpn, etc. And includes this comprehensive information in the output.

## Instructions

- Text file named `ip.txt` filled with an IP-addresses
- Required API from `ipdata.co`

## How To Run

```bash
python3 neonito-vuln-checker.py
```

## Result

IP and Country in the log are not real, only are examples of the script result.

```json
{
  "summary": {
    "vulns": 2,
    "honeypot": 0,
    "tor": 0,
    "vpn": 1,
    "proxy": 0,
    "datacenter": 1,
    "anonymous": 1,
    "attacker": 0,
    "abuser": 0,
    "threat": 0
  },
  "ip_details": [
    {
      "ip": "123.124.125.126",
      "country_name": "United States",
      "vulns": ["CVE-2021-1234", "CVE-2021-5678"],
      "honeypot": "No",
      "tor": "No",
      "vpn": "Yes",
      "proxy": "No",
      "datacenter": "Yes",
      "anonymous": "Yes",
      "attacker": "No",
      "abuser": "No",
      "threat": "No"
    }
  ]
}
```
