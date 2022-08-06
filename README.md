# Youtube Data Analysis Project

## Purpose
The idea behind this project is to allow to extract data from YouTube using an API key. The data is related to the most popular videos in a specific country.

## Perequisites
- The pip package management tool

- The Google APIs Client Library for Python:

> pip install --upgrade google-api-python-client

- The google-auth, google-auth-oauthlib, and google-auth-httplib2 for user authorization.

> pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

## Setting up your project and running code samples

### Get a YouTube API Key

i. Log in to Google Developers Console.
ii. Create a new project.
iii. On the new project dashboard, click Explore & Enable APIs.
iv. In the library, navigate to YouTube Data API v3 under YouTube APIs.
v. Enable the API.
vi. Create a credential.
vii. A screen will appear with the API key.

### Create a project in the API Console and set up credentials for a web application. Set the authorized redirect URIs as appropriate.

- Save the API key and add it to the code line saying "YOUR API KEY".

## YouTube API methods used

1. youtube.videos().list()
Returns a list of videos that match the API request parameters. More details [here](https://developers.google.com/youtube/v3/docs/videos/list).

2. youtube.channels().list()
Returns a collection of zero or more `channel` resources that match the request criteria. More details [here](https://developers.google.com/youtube/v3/docs/channels/list).

## Updates
The code will be updated constantly, therefore, please keep in mind this is not the final version.
