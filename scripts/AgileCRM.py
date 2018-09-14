import requests
import json
from urllib.parse import urljoin


APIKEY = "ik7g8dqbga417hago0raim5mqm"   # Your API KEY
EMAIL = "austinblock@protonmail.com"  # Your API EMAIL
DOMAIN = "austintest"  # Your DOMAIN
BASE_URL = "https://" + DOMAIN + ".agilecrm.com/dev/api/"



# Function definition is here
def agileCRM(nextURL,method,data,contenttype):

   url = BASE_URL + nextURL

   headers = {
        'Accept': 'application/json',
        'content-type': contenttype,
    }

   if ( method  == "GET" ) :
       
       response = requests.get(
        url,
        headers=headers,
        auth=(EMAIL, APIKEY)
        )
       return response.text
    
   if ( method  == "POST" ) :
       
       response = requests.post(
        url,
        data=json.dumps(data),
        headers=headers,
        auth=(EMAIL, APIKEY)
        )
       return response.text
    
   if ( method  == "PUT" ) :
       response = requests.put(
        url,
        data=json.dumps(data),
        headers=headers,
        auth=(EMAIL, APIKEY)
        )
       return response.text

   if ( method  == "DELETE" ) :
       response = requests.delete(
        url,
        headers=headers,
        auth=(EMAIL, APIKEY)
        )
       return response

   if ( method  == "POSTFORM" ) :
       
       response = requests.post(
        url,
        data=data,
        headers=headers,
        auth=(EMAIL, APIKEY)
        )
       return response.text

   
   return "Wrong method provided"

