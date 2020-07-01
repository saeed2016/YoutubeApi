# https://developers.google.com/youtube/v3/docs
# document by
from googleapiclient.discovery import build
import os
# using RegEx(regulare expression)
import re
from datetime import timedelta
api_key = "AIzaSyCwZ9DO370bjZLJ_xFdjnFS8d1-7yC8p1M"
youtube = build('youtube', 'v3', developerKey=api_key)
# by default only 5 playlists return .I use pagetoken to get all of the results in  one page at time then use while to loop throught it.
nextPageToken = None
# as duration in json file show like PT23M31S
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')
totalseconds=0
while True:
   pl_request = youtube.playlistItems().list(
      part='contentDetails',
      playlistId='PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU',
      maxResults=50,
      pageToken=nextPageToken
   )
   pl_response = pl_request.execute()
   vid_id=[]
   for item in pl_response['items']:
      vid_id.append(item['contentDetails']['videoId'])
   vd_requeset = youtube.videos().list(
      part="contentDetails",
      id=','.join(vid_id)
      )
   vd_response = vd_requeset.execute()
   # print(vd_response['items'][0]['contentDetails']['duration'])
   # print()
   #print(vd_response['items'][0])
   video_seconds_list=[]
   for item in vd_response['items']:
      duration = item['contentDetails']['duration']
      hours=hours_pattern.search(duration)
      minutes=minutes_pattern.search(duration)
      seconds=seconds_pattern.search(duration)

      hours=int(hours.group(1)) if hours else 0
      minutes=int(minutes.group(1)) if minutes else 0
      seconds=int(seconds.group(1)) if seconds else 0
      #using timedelta to convert time to seconds
      video_seconds=timedelta(
         hours=hours,
         minutes=minutes,
         seconds=seconds
      ).total_seconds()
      totalseconds+=video_seconds
      #print(video_seconds)
   nextPageToken = pl_response.get('nextPageToken')

   if not nextPageToken:
      break
totalseconds=int(totalseconds)
print(timedelta(seconds=totalseconds))
print(totalseconds)
minutes, seconds = divmod(totalseconds, 60)
print(minutes)
print(seconds)
hours, minutes = divmod(minutes, 60)
print(hours)
print(minutes)
print(f'{hours}:{minutes}:{seconds}')
print("%d:%02d:%02d" % (hours, minutes, seconds))
