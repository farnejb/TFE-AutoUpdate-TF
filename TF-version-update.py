import requests
import json
import urllib3
import os

#get env variable
admin_token = os.getenv('TFE_TOKEN')
print('TFE_TOKEN =', admin_token)
#get most current version number from checkpoint
response = requests.get('https://checkpoint-api.hashicorp.com/v1/check/terraform')

json_data = response.json() if response and response.status_code == 200 else None

current_version = json_data.get('current_version')

#query TFE for a list of available versions
headers = {'Authorization': 'Bearer ' + admin_token, 'Content-Type': 'application/vnd.api+json'}
response2 = requests.get('https://<your-server>/api/v2/admin/terraform-versions', headers=headers)

version_data = response2.json() if response2 and response2.status_code == 200 else None

#print(version_data)

#look for latest version value present in json data
for element in version_data['data']:
    if element['attributes']['version'] == current_version:
        print ('Most current version is installed', current_version)
        break
#if latest version is not present in available versions on TFE:
else: 
    print ('installing most current version', current_version)
    url = "https://releases.hashicorp.com/terraform/{0}/terraform_{0}_SHA256SUMS".format(current_version)
#grab sha256 hash from releases binary; will need to change character range for versions other than amd64
    content=requests.get(url)
    sha256 = content.text[496:560]
    print(sha256)
#update download URL and create JSON payload    
    download_url = "https://releases.hashicorp.com/terraform/{0}/terraform_{0}_linux_amd64.zip".format(current_version)

    payload = {
        "data": {
            "type": "terraform-versions",
            "attributes": {
                "version": current_version,
                "url": download_url,
                "sha": sha256,
                "official": True,
                "enabled": True,
                "beta": False
            }
        }
    }

    print(json.dumps(payload, indent=4))

    encoded_body = json.dumps(payload)

    http = urllib3.PoolManager()
#POST to TFE TF Versions API; can only be done once (and not deleted) if flagged as "official"
    r = http.request('POST', 'https://<your-server>/api/v2/admin/terraform-versions', 
        headers={'Authorization':'Bearer <token>', 'Content-Type': 'application/vnd.api+json'},
        body=encoded_body)

    print(r.status)