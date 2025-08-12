# Claude Assistant Instructions

This document contains project-specific instructions and context for Claude to effectively work with the YouTube Video List Extractor project.

## Project Overview

This is a Python tool that extracts video information from YouTube channels using the YouTube Data API v3. It saves data in both CSV and JSON formats and includes analysis tools for video statistics.

**Repository:** https://github.com/makgunay/yt_videolist  
**License:** MIT License  
**Author:** Mehmet Akgunay

## Key Commands

### Running the Application
```bash
# Extract videos from a channel
python main.py

# Analyze video durations
python analyze_duration.py
```

### Testing & Validation
```bash
# Check Python syntax
python -m py_compile main.py analyze_duration.py

# Run with sample channel (Mesele Ekonomi)
# Channel ID: UCW4Y4bPuafXwVEs0oly5vdw
```

### Dependency Management
```bash
# Install dependencies with Poetry
poetry install

# Install with pip
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Important Files & Their Purpose

- `main.py`: Core script for extracting YouTube channel videos
- `analyze_duration.py`: Analyzes video durations and statistics from JSON exports
- `client_secret.json`: Google OAuth credentials (NEVER commit to git)
- `token.json`: OAuth token for authentication (NEVER commit to git)
- `.gitignore`: Configured to exclude sensitive files and outputs

## API & Authentication Notes

1. **OAuth Flow**: First run opens browser for Google account authorization
2. **Token Management**: `token.json` stores refresh token for subsequent runs
3. **API Quotas**: YouTube Data API v3 has 10,000 units daily limit
4. **Request Cost**: Each video list request uses ~3 units

## Output File Naming Convention

- CSV: `{channel_name}_{YYYYMMDD}_{video_count}.csv`
- JSON: `{channel_name}_{YYYYMMDD}_{video_count}.json`

## Common Tasks

### Adding New Features
When adding features, consider:
- Maintain compatibility with existing CSV/JSON output formats
- Handle API quota limits gracefully
- Preserve OAuth token management logic

### Debugging Issues
- Check `token.json` validity if authentication fails
- Verify `client_secret.json` is present and valid
- Monitor API quota usage in Google Cloud Console

## Data Structure

### CSV Fields
- video_id, title, description, link, publish_date
- view_count, like_count, comment_count
- duration, tags (comma-separated), category_id

### JSON Structure
```json
{
  "channel_name": "string",
  "export_date": "YYYYMMDD",
  "video_count": number,
  "videos": [
    {
      "video_id": "string",
      "title": "string",
      "publish_date": "ISO 8601",
      "duration": "ISO 8601 duration",
      "tags": ["array"],
      // ... additional metadata
    }
  ]
}
```

## Security Reminders

- NEVER commit `client_secret.json` or `token.json`
- These files are in `.gitignore` but always double-check
- Rotate API credentials periodically
- Don't log or print sensitive tokens

## Testing Channels

- Mesele Ekonomi: `UCW4Y4bPuafXwVEs0oly5vdw` (Turkish economics channel)
- Use for testing pagination and large video libraries

## Future Improvements to Consider

- Add progress bar for large channel downloads
- Implement incremental updates (only fetch new videos)
- Add filtering options (date range, video count limits)
- Create summary statistics report
- Add export to other formats (Excel, Markdown table)

## Project Licensing

This project is licensed under the MIT License. When contributing or using this code:
- Maintain copyright notices
- Include the LICENSE file in any distributions
- Feel free to use commercially with attribution

## Error Handling

Common errors and solutions:
- `HttpError 403`: Check API quota or credentials
- `RefreshError`: Delete `token.json` and re-authenticate
- `KeyError` in video data: Some videos may lack certain fields (use `.get()`)

## Performance Notes

- Large channels (1000+ videos) may take several minutes
- API pagination returns max 50 videos per request
- Consider implementing caching for development/testing