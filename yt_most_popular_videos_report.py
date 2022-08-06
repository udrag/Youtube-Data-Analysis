# import libraries
import pandas as pd
import numpy as np
import requests
import seaborn as sns

# google libraries
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build

# insert the api key
api_key = "YOU API KEY"

# create the youtube service
youtube = build('youtube', 'v3', developerKey=api_key)

def youtube_videos():
    
    region_list = youtube.i18nRegions().list(part="snippet")
    response = region_list.execute()
    
    print('Enter the 2 letters of the region code. If you would like to see the whole list of region codes, please enter \'list\'')
    region_code = str(input()).upper()
    matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
       
    if region_code == 'LIST':
        for i in range(len(response['items'])):
            print(response['items'][i]['snippet']['gl'] + ' ' + '-' + ' ' + response['items'][i]['snippet']['name'])
        print('Enter the 2 letters of the region code:')
        region_code = str(input()).upper()
        matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
        
    while matches == 'False':
        print(f'{region_code} is not a valid region code. Please enter the 2 letters of the region code. If you would like to see the whole list of region codes, please enter \'list\'')
        region_code = str(input()).upper()
        matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
        if region_code == 'LIST':
            for i in range(len(response['items'])):
                print(response['items'][i]['snippet']['gl'] + ' ' + '-' + ' ' + response['items'][i]['snippet']['name'])
            print('Enter the 2 letters of the region code:')
            region_code = str(input()).upper()
            matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
    
    
    print('Enter the number of videos you would like to see (max 50).')
    number = int(input())
      
      
    search_response = youtube.videos().list(
                        part = 'snippet,contentDetails,statistics,localizations',
                        chart = 'mostPopular',
                        regionCode = region_code,
                        maxResults = number)
    response = search_response.execute() 
    
    all_data = []
    for i in range(len(response['items'])):
        try:
            data = dict(requested_region = region_code,
                        title = response['items'][i]['snippet']['title'],
                        view_count = response['items'][i]['statistics']['viewCount'],
                        like_count = response['items'][i]['statistics']['likeCount'],
                        comment_count = response['items'][i]['statistics']['commentCount'],
                        published_date = response['items'][i]['snippet']['publishedAt'],
                        video_url = 'https://www.youtube.com/watch?v='+str(response['items'][i]['id']),
                        channel_url = 'https://www.youtube.com/channel/'+str(response['items'][i]['snippet']['channelId']),
                        channel_id = response['items'][i]['snippet']['channelId'])
        except KeyError:
            print('A KeyError %d occurred:\n%s')

        all_data.append(data)
    
    print('Would you like to include channel info as well?')
    answer = str(input()).upper()
    
    if answer == 'YES':
        channel_list = list((pd.DataFrame(all_data))['channel_id'])
                
        request = youtube.channels().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(channel_list))
        response = request.execute()
        
        channel_ids = []      
        for i in range(len(response['items'])):
            try:
                data = dict(channel_name = response['items'][i]['snippet']['title'],
                            channel_subscribers = response['items'][i]['statistics']['subscriberCount'],
                            channel_views = response['items'][i]['statistics']['viewCount'],
                            channel_videos = response['items'][i]['statistics']['videoCount'],
                            channel_id = response['items'][i]['id'])
            
                channel_ids.append(data)
            
            except KeyError:
                print('A KeyError %d occurred:\n%s')
                
        
        return pd.merge(pd.DataFrame(all_data), pd.DataFrame(channel_ids), on='channel_id')
    else:
        return pd.DataFrame(all_data)
        
  # run the function and retrieve the database
df = youtube_videos()
df
