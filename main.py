import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import csv
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

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

    channel_id = input("Enter the YouTube channel ID: ")
    
    try:
        channel_info = get_channel_info(youtube, channel_id)
        videos = get_all_videos(youtube, channel_info['uploads_playlist_id'])
        save_to_files(videos, channel_info['channel_name'])
        print(f"Successfully saved {len(videos)} videos from channel '{channel_info['channel_name']}' to CSV and JSON")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="contentDetails,snippet",
        id=channel_id
    )
    response = request.execute()
    channel = response['items'][0]
    return {
        'uploads_playlist_id': channel['contentDetails']['relatedPlaylists']['uploads'],
        'channel_name': channel['snippet']['title']
    }

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
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'link': f"https://www.youtube.com/watch?v={video['id']}",
                    'publish_date': video['snippet']['publishedAt'],
                    'view_count': video['statistics'].get('viewCount', 'N/A'),
                    'like_count': video['statistics'].get('likeCount', 'N/A'),
                    'comment_count': video['statistics'].get('commentCount', 'N/A'),
                    'duration': video['contentDetails']['duration'],
                    'tags': video['snippet'].get('tags', []),  # Keep as list for JSON
                    'category_id': video['snippet']['categoryId']
                }
                videos.append(video_info)
            video_ids = []

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def save_to_files(videos, channel_name):
    current_date = datetime.now().strftime('%Y%m%d')
    # Replace any characters that might be invalid in filenames
    safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in (' ', '-', '_')).strip()
    base_filename = f"{safe_channel_name}_{current_date}_{len(videos)}"
    
    # Save to CSV
    csv_filename = f"{base_filename}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['video_id', 'title', 'description', 'link', 'publish_date', 'view_count', 'like_count', 'comment_count', 'duration', 'tags', 'category_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for video in videos:
            # Convert tags list to comma-separated string for CSV
            video_csv = video.copy()
            video_csv['tags'] = ', '.join(video['tags'])
            writer.writerow(video_csv)
    
    # Save to JSON
    json_filename = f"{base_filename}.json"
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump({
            'channel_name': channel_name,
            'export_date': current_date,
            'video_count': len(videos),
            'videos': videos
        }, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
