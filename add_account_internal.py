import requests 
from datetime import datetime

from binascii import b2a_base64
import json


new_account_request= dict(
        termsOfUse=True,
        privacyPolicy=True,
        
        login=dict(
            federatedPlatform=None,
            federatedToken=None,
            email=b2a_base64(b"yangyangyy@outlook.com").decode(),
            password=b2a_base64(b"nustest").decode(),
        ),
    )

data=json.dumps(new_account_request)
print(data)
response = requests.post('http://42.60.37.128:5002/api/account',data=json.dumps(new_account_request),headers = {'Content-Type':'application/json'})

print(response.content)
#Add open_dataset agreement for STT google cloud API
#insert into account.account_agreement(account_id, agreement_id, accept_date) values('d214b11c-cf7a-4c5f-8b53-f8cc3b4e31fb','0b83ae2d-9b5e-4993-ae55-d9036ee79af6',CURRENT_DATE);
  
