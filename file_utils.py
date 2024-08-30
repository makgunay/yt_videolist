import csv

def save_to_csv(videos):
    with open('youtube_videos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'description', 'link'])
        writer.writeheader()
        for video in videos:
            writer.writerow(video)

