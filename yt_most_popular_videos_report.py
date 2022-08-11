# Import libraries
import pandas as pd
import numpy as np
import requests
import seaborn as sns

# Import Google libraries
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build

# Get YouTube API credentials
api_key = 'AIzaSyDTyW6xXRO6-Z8T5tXWLwKXv0SFmYlxfjI'
youtube = build('youtube', 'v3', developerKey=api_key)

def youtube_videos():
    """
    This function generates a data frame with statistics about YouTube videos.
    The values of region code and number of results are obtained via input functions.
    In any input field write 'list' to get the list of all the region codes.
    Last question will ask the user for input on adding to the data frame the statistics about the channels of the videos.
    """
    # Create an API client for the region codes
    region_list = youtube.i18nRegions().list(part="snippet")
    response = region_list.execute()
    
    # User input for the region code
    print('Enter the 2 letters of the region code. If you would like to see the whole list of region codes, please enter \'list\'')
    region_code = str(input()).upper()
    matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
    
    # Conditional statement for the region codes list
    if region_code == 'LIST':
        for i in range(len(response['items'])):
            print(response['items'][i]['snippet']['gl'] + ' ' + '-' + ' ' + response['items'][i]['snippet']['name'])
        print('Enter the 2 letters of the region code:')
        region_code = str(input()).upper()
        matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
    
    # Conditional statement for misspelled words
    while matches == 'False':
        print(f'{region_code} is not a valid region code. Please enter the 2 letters of the region code. If you would like to see the whole list of region codes, please enter \'list\'')
        region_code = str(input()).upper()
        matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
        if region_code == 'LIST': # Conditional statement for the region codes list inside the while loop
            for i in range(len(response['items'])):
                print(response['items'][i]['snippet']['gl'] + ' ' + '-' + ' ' + response['items'][i]['snippet']['name'])
            print('Enter the 2 letters of the region code:')
            region_code = str(input()).upper()
            matches = str(bool([item for item in response['items'] if(item["id"] == region_code)]))
    
    # User input for the number of results
    print('Enter the number of videos you would like to see (max 50).')
    number = int(input())
      
    # API request parameters
    search_response = youtube.videos().list(
                        part = 'snippet,contentDetails,statistics,localizations',
                        chart = 'mostPopular',
                        regionCode = region_code,
                        maxResults = number)
    response = search_response.execute() 
    
    # Create a list and add the API results
    all_data = []
    for i in range(len(response['items'])):
        try:
            data = dict(requested_region = region_code,
                        title = response['items'][i]['snippet']['title'],
                        view_count = int(response['items'][i]['statistics']['viewCount']),
                        like_count = int(response['items'][i]['statistics']['likeCount']),
                        comment_count = int(response['items'][i]['statistics']['commentCount']),
                        published_date = dt.strptime(response['items'][i]['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                        video_url = 'https://www.youtube.com/watch?v='+str(response['items'][i]['id']),
                        channel_url = 'https://www.youtube.com/channel/'+str(response['items'][i]['snippet']['channelId']),
                        channel_id = response['items'][i]['snippet']['channelId'])
        except KeyError:
            print('A KeyError %d occurred:\n%s') # For rare occasions when not all the statistcs are present

        all_data.append(data)
        
    # User input for channel statistics to be adde to the data frame
    print('Would you like to include channel info as well?')
    answer = str(input()).upper()
    
    # Conditional statement for YES answer
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
                            channel_subscribers = int(response['items'][i]['statistics']['subscriberCount']),
                            channel_views = int(response['items'][i]['statistics']['viewCount']),
                            channel_videos = int(response['items'][i]['statistics']['videoCount']),
                            channel_id = response['items'][i]['id'])
            
                channel_ids.append(data)
            
            except KeyError:
                print('A KeyError %d occurred:\n%s')
                
        # Return the merged data
        return pd.merge(pd.DataFrame(all_data), pd.DataFrame(channel_ids), on='channel_id')
    # Return the video statistics only
    else:
        return pd.DataFrame(all_data)
        
# Run the function and retrieve the database
df = youtube_videos()
df
