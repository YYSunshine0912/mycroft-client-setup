import requests 
import os
from datetime import datetime
import re

import json

from util.auth_cookies import save_cookies, load_cookies


ACCESS_TOKEN_COOKIE_KEY = 'seleneAccess'
REFRESH_TOKEN_COOKIE_KEY = 'seleneRefresh'


#Step 1 manually enter the URL below to get the github token in browser
#https://github.com/login/oauth/authorize?scope=user:email&client_id=0d6cc5d42fb4158ccaba&state=1

#Step 2 enter the latest token which is got in step1 in 'github_token' variable

#Step 3 run this 'test_federated_github.py' then it can implement federated login using github account

github_token=''

   


def call_validate_federated_endpoint():
    cookies = dict()  
    response = requests.post('http://42.60.37.128:5002/api/validate-federated',data=json.dumps(dict(platform='GitHub', token=github_token)),headers = {'Content-Type':'application/json'})  
   
    cookies=get_cookies(response)
    save_cookies(cookies)

def call_get_account_endpoint():
    cookies = load_cookies()
    print('Loaded cookies info is:')
    print(json.dumps(cookies))  
    response = requests.get('http://42.60.37.128:5001/api/account',cookies=cookies,headers = {'Content-Type':'application/json'})
    
    print('Current account info is:')
    print(response.content)
  
    

def get_cookies(response) -> dict:
    token_cookies = dict()  
    #print(response.headers['Set-Cookie'])
    cookies=re.sub('(Expires=...),',r'\1',response.headers['Set-Cookie'])
    #print(cookies)
    
    for cookie in cookies.split(', '):
        #print(cookie)
        ingredients = parse_cookie(cookie)
        ingredient_names = list(ingredients.keys())
        if ACCESS_TOKEN_COOKIE_KEY in ingredient_names:
            token_cookies[ACCESS_TOKEN_COOKIE_KEY] = ingredients[ACCESS_TOKEN_COOKIE_KEY]
            if ingredients['Max-Age']=='0':
                print('access token is expired')
        elif REFRESH_TOKEN_COOKIE_KEY in ingredient_names:
            token_cookies[REFRESH_TOKEN_COOKIE_KEY] = ingredients[REFRESH_TOKEN_COOKIE_KEY]
            if ingredients['Max-Age']=='0':
                print('refresh token is expired')       
  
    return token_cookies
     
def parse_cookie(cookie: str) -> dict:
    ingredients = {}
    for ingredient in cookie.split('; '):        
        if '=' in ingredient:
            key, value = ingredient.split('=')
            ingredients[key] = value
        else:
            ingredients[ingredient] = None

    return ingredients

def main(): 
   
    call_validate_federated_endpoint()
    call_get_account_endpoint()
 

if __name__ == "__main__":
    main()



  
