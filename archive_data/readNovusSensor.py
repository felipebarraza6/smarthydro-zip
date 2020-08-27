# script de ejemplo para mostrar como se extrae el último dato envíado por un device al servidor de novus

import requests as rq 
import json

url = "http://m2.exosite.com/onep:v1/rpc/process"
sensorCik = "608becd63fd7bfef1bb683248d8839c6bc135440" 
dataAlias = "3GRECUC1V"
payload = {
	"auth": {
		"cik": sensorCik},
	"calls":[
		{
			"procedure":"read",
			"arguments":[
				{
					"alias": dataAlias
				},
				{}],
			"id": 0
		}]
}

payload = json.dumps(payload)
headers = {
    'content-type': "application/json; charset=utf-8",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)