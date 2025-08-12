import json
from datetime import datetime, timedelta
import re

# Load the JSON file
with open('Mesele Ekonomi_20250812_2138.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get the date one year ago from today (timezone-aware)
from datetime import timezone as tz
one_year_ago = datetime.now(tz.utc) - timedelta(days=365)

# Function to parse ISO 8601 duration to seconds
def parse_duration(duration_str):
    """Parse ISO 8601 duration string (e.g., PT4M33S) to total seconds"""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds

# Filter videos from the past year and calculate total duration
total_seconds = 0
video_count = 0

for video in data['videos']:
    # Parse the publish date
    publish_date = datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00'))
    
    # Check if video is from the past year
    if publish_date >= one_year_ago:
        video_count += 1
        duration_seconds = parse_duration(video['duration'])
        total_seconds += duration_seconds

# Convert total seconds to readable format
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

print(f"Videos from the past year (since {one_year_ago.strftime('%Y-%m-%d')}): {video_count}")
print(f"Total duration: {hours} hours, {minutes} minutes, {seconds} seconds")
print(f"Total duration in days: {total_seconds / 86400:.2f} days")