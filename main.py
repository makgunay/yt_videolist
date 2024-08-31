import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', scopes)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    channel_id = "UCW4Y4bPuafXwVEs0oly5vdw"
    
    try:
        uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
        videos = get_all_videos(youtube, uploads_playlist_id)
        save_to_csv(videos)
        print(f"Successfully saved {len(videos)} videos to youtube_videos.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_uploads_playlist_id(youtube, channel_id):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_video_details(youtube, video_ids):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    return response['items']

def get_all_videos(youtube, playlist_id):
    videos = []
    next_page_token = None
    video_ids = []

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])

        if len(video_ids) >= 50 or not response.get('nextPageToken'):
            video_details = get_video_details(youtube, video_ids)
            for video in video_details:
                video_info = {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'link': f"https://www.youtube.com/watch?v={video['id']}",
                    'publish_date': video['snippet']['publishedAt'],
                    'view_count': video['statistics'].get('viewCount', 'N/A'),
                    'like_count': video['statistics'].get('likeCount', 'N/A'),
                    'comment_count': video['statistics'].get('commentCount', 'N/A'),
                    'duration': video['contentDetails']['duration'],
                    'tags': ', '.join(video['snippet'].get('tags', [])),
                    'category_id': video['snippet']['categoryId']
                }
                videos.append(video_info)
            video_ids = []

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def save_to_csv(videos):
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'description', 'link', 'publish_date', 'view_count', 'like_count', 'comment_count', 'duration', 'tags', 'category_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for video in videos:
            writer.writerow(video)

if __name__ == "__main__":
    main()