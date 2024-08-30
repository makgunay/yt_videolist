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