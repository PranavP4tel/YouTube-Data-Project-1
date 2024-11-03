import pandas as pd
from googleapiclient.discovery import build
from config import API_KEY

def get_trending_videos(api_key, max_results = 200):
    #Building the youtube service
    youtube = build('youtube','v3',developerKey = api_key)

    #Creating a list to store the details
    videos = []

    #Fetch the videos
    #snippet: represents the basic details about the video
    #contentDetails: Information about the video content
    #Statistics: statistics about the video
    #Status: information about the video's uploading, processing and privacy status
    #Refer to the documentation for more properties: https://developers.google.com/youtube/v3/docs/videos#properties

    request = youtube.videos().list(
        part = 'snippet, contentDetails,statistics',
        chart='mostPopular',
        regionCode='IN',
        maxResults = 50
    )

    #Iterate through the results, append video details to our list and stop once 200 records are obtained
    while request and len(videos)<max_results:
        response = request.execute()
        for item in response['items']:
            video_details = {
                'video_id':item['id'],
                'title':item['snippet']['title'],
                'description':item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'channel_title':item['snippet']['channelTitle'],
                'category_id':item['snippet']['categoryId'],
                'tags':item['snippet'].get('tags',[]),
                'duration':item['contentDetails']['duration'],
                'caption':item['contentDetails'].get('caption','false'),
                'view_count':item['statistics'].get('viewCount',0),
                'like_count':item['statistics'].get('likeCount',0),
                'dislike_count':item['statistics'].get('dislikeCount',0),
                'favorite_count':item['statistics'].get('favouriteCount',0),
                'comment_count':item['statistics'].get('commentCount',0)
            }
            videos.append(video_details)
        
        request = youtube.videos().list_next(request, response)

    return videos[:max_results]

def save_to_csv(data, file):
    df = pd.DataFrame(data)
    df.to_csv(file, index=False)

if __name__ == '__main__':
    trending_videos = get_trending_videos(API_KEY)
    #Export file to csv
    file = 'Trending_Videos.csv'
    save_to_csv(trending_videos, file)
    print(f'Video details saved to {file}')