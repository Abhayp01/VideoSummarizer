from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import pandas as pd 
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string
import re

app = Flask(__name__)
CORS(app)
def summarize_text(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_sentences = []
    for sentence in sentences:
        words = [word.lower() for word in nltk.word_tokenize(sentence) if word.lower() not in stop_words and word not in string.punctuation]
        filtered_sentences.append(' '.join(words))
    
    sentence_scores = [1 for _ in sentences]
    sorted_sentences_scores = sorted(zip(filtered_sentences, sentence_scores), key=lambda x: x[1], reverse=True)
    
    sorted_sentences = [sentence for sentence, score in sorted_sentences_scores]
    
    summary = ' '.join(sorted_sentences)
    return summary



genai.configure(api_key="AIzaSyBc9QNEpWjPn-V6btBV__ZAcLUexxu_WOI")

generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,     
  "top_k": 50,        
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
def handle_user_message(message):
  summary = summarize_text(message)

  prompt = f"provide notes for the lecture explain in detail: {summary}"
  response = model.generate_content(prompt)

  return f"\n {response.text}."


def extract_video_id(url):
    
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|u/\w/)?([^#&?]*)'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

@app.route('/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    video_url = data['url']
    video_id = extract_video_id(video_url)

    if video_id:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ''.join([entry['text'] for entry in transcript])
            summary = handle_user_message(transcript_text)

            return jsonify({'transcript': transcript_text, 'summary': summary})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid YouTube URL'}), 400


if __name__ == '__main__':
    app.run()