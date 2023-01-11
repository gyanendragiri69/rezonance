from numpy.lib.function_base import insert
import requests
import json
import os
import time
import pandas as pd

# CLIENT_ID = os.environ["CLIENT_ID"]
# CLIENT_SECRET = os.environ["CLIENT_SECRET"]


CLIENT_ID="74acfc9e9923439a8bed446412182632"
CLIENT_SECRET="67e18108d844498ba024070c6b9b1869"


AUTH_URL = "https://accounts.spotify.com/api/token"

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()


# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


main_df = pd.DataFrame(columns=["name", "spotify_id", "popularity"])
ctr = 0


for off in range(1, 2001):
    try:
        req_param = "type=track&q=year:2001&limit=50&offset={itr}".format(itr = off)
        res = requests.get("https://api.spotify.com/v1/search?{q}".format(q = req_param), headers=headers).json()

        list_dicts = []

        for i, item in enumerate(res['tracks']['items']):
            temp_dict = {
                "name": item['name'],
                "spotify_id": item['id'],
                "popularity": item['popularity']
            }
            list_dicts.append(temp_dict)

        df = pd.DataFrame(list_dicts)
        main_df = main_df.append(df, ignore_index=True)

    except:
        print("breaking")
        main_df.to_csv("raw/songs_2001.csv")
        print(len(main_df))
        break

    ctr += 50
    # print("Fetched ", ctr, " songs till now.")

    if(ctr % 1000 == 0):
        print("sleeping after fetching ", ctr, " songs.")
        time.sleep(1)
    
main_df.to_csv("raw/songs_2001.csv")
