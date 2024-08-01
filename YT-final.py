import os
import re
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai

# Load API keys from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def fetch_comments(video_id, max_comments=1000):
    """Fetches comments from a YouTube video using the YouTube Data API v3."""
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    next_page_token = None

    print("Fetching comments...")
    with tqdm(total=max_comments, desc="Fetching comments") as pbar:
        try:
            while len(comments) < max_comments:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=min(100, max_comments - len(comments)),  # Fetch up to 100 comments per request
                    textFormat='plainText',
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    comments.append(comment)
                    pbar.update(1)
                    if len(comments) >= max_comments:
                        break
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    return comments

def generate_summary(transcript_text):
    """Generates a summary using the Gemini API."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = ("Analyze the following YouTube comments. Identify the overall sentiment."
              " Provide a short summary of the comments and any insights into the audience's reaction to the content.")
    try:
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary"

def main():
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print("Invalid YouTube URL")
        return
    
    comments = fetch_comments(video_id, max_comments=1000)  # Request up to 1000 comments

    comments_text = "\n".join(comments)
    
    print("Generating summary...")
    summary = generate_summary(comments_text)
    print(f"Summary: {summary}")

if __name__ == "__main__":
    main()
