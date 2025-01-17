from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import requests
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult

ClientID = "eehg1nfgtlmyin3oxe08rqkrcq2j5x";
ClientSecret = "23b1wd8czop0h0ookhmjvhfyv39ksa";

url = "https://id.twitch.tv/oauth2/token"
platformDict = {'Switch': '130', 'PlayStation' : '48,167', 'Xbox' : '49,169', 'PC' : '6'}

querystring = {"client_id":ClientID,"client_secret":ClientSecret,"grant_type":"client_credentials"}

payload = ""
headers = {"User-Agent": "insomnia/10.3.0"}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

token = response.json()['access_token']

def members(request):
    platform = request.GET.get('platform', 'all');
    
    url = "https://api.igdb.com/v4/games/"

    querystring = {"":""}

    fields = "fields id,name,summary,cover.image_id, platforms,total_rating; "
    if (platform == 'all'):
        where = "where total_rating > 85 & total_rating_count > 100; ";
    else:
        where = "where total_rating > 85 & total_rating_count > 100 & platforms = (" + platformDict[platform] +  "); ";
    sort = "sort total_rating desc;"
    
    payload = fields + where + sort;
    
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "insomnia/10.3.0",
        "Client-ID": ClientID,
        "Authorization": "Bearer " + token
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    
    wrapper = IGDBWrapper(ClientID, token)
    
    #byte_array = wrapper.api_request(
    #        'games',
    #        payload
    #      )
    # parse into JSON however you like...

    # Protobuf API request
    byte_array = wrapper.api_request(
                'games', # Note the '.pb' suffix at the endpoint
                payload
              )
    my_new_string_value = byte_array.decode("utf-8")
    my_json = json.loads(my_new_string_value)
    myjson2 = json.dumps(my_json, indent=4, sort_keys=True)
    
    return HttpResponse(myjson2)
    
def search(request):
    query = request.GET.get('query', '');
    
    url = "https://api.igdb.com/v4/games/"

    querystring = {"":""}

    fields = "fields id,name,summary,cover.image_id, platforms,total_rating;";
    search = "search \"" + query + "\";"
    where = "";
    limit = "limit 20;"
    
    payload = fields + search + where + limit;
    
    print(payload)
    
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "insomnia/10.3.0",
        "Client-ID": ClientID,
        "Authorization": "Bearer " + token
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    
    wrapper = IGDBWrapper(ClientID, token)
    
    #byte_array = wrapper.api_request(
    #        'games',
    #        payload
    #      )
    # parse into JSON however you like...

    # Protobuf API request
    byte_array = wrapper.api_request(
                'games', # Note the '.pb' suffix at the endpoint
                payload
              )
    my_new_string_value = byte_array.decode("utf-8")
    my_json = json.loads(my_new_string_value)
    myjson2 = json.dumps(my_json, indent=4, sort_keys=True)
    
    return HttpResponse(myjson2)
    
def game(request):
    gameID = request.GET.get('id', 'all');
    
    url = "https://api.igdb.com/v4/games/"

    querystring = {"":""}

    fields = "fields *; "
    where = "where id = " + gameID + ";"
    
    payload = fields + where;
    
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "insomnia/10.3.0",
        "Client-ID": ClientID,
        "Authorization": "Bearer " + token
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    
    wrapper = IGDBWrapper(ClientID, token)
    
    # Protobuf API request
    byte_array = wrapper.api_request(
                'games', # Note the '.pb' suffix at the endpoint
                payload
              )
    my_new_string_value = byte_array.decode("utf-8")
    my_json = json.loads(my_new_string_value)
    myjson2 = json.dumps(my_json, indent=4, sort_keys=True)
    
    return HttpResponse(myjson2)