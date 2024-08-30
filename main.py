import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import csv

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    channel_id = "ENTER_CHANNEL_ID_HERE"
    
    try:
        videos = get_channel_videos(youtube, channel_id)
        save_to_csv(videos)
        print(f"Successfully saved {len(videos)} videos to youtube_videos.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_channel_videos(youtube, channel_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date",
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def save_to_csv(videos):
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'description', 'link'])
        writer.writeheader()
        for video in videos:
            writer.writerow(video)

if __name__ == "__main__":
    main()