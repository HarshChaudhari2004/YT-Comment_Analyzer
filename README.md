# YT-Comment_Analyzer

`YT-Comment_Analyzer` is a Python script that takes a YouTube video URL as input, fetches comments using the YouTube Data API, and analyzes them to provide a summary using the Gemini API.

## Features

- Extracts comments from a YouTube video.
- Analyzes comments and provides a summary.
- Identifies overall sentiment and audience reactions.

## Requirements

To run this project, you'll need Python 3.6 or later. You also need API keys for the YouTube Data API and the Gemini API.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/YT-Comment_Analyzer.git
   cd YT-Comment_Analyzer

2. **Execution**
   
   make .env file and paste API's
   ```bash
   YOUTUBE_API_KEY="your_youtube_api_key_here"
   GEMINI_API_KEY="your_gemini_api_key_here" ```

Install requirements:
   ```bash
   pip install -r requirements.txt ```

Run the Code:
   ```bash
   python YT-final.py
