import os
from youtube_api import get_channel_videos
from file_utils import save_to_csv
import google_auth_oauthlib.flow
import googleapiclient.discovery

def main():
    # (OAuth setup code remains the same)
    
    channel_id = "@MeseleEkonomi"
    
    try:
        videos = get_channel_videos(youtube, channel_id)
        save_to_csv(videos)
        print(f"Successfully saved {len(videos)} videos to youtube_videos.csv")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()



# file_utils.py
import csv

def save_to_csv(videos):
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'description', 'link'])
        writer.writeheader()
        for video in videos:
            writer.writerow(video)