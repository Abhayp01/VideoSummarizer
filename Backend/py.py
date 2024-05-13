import google.generativeai as genai
import pandas as pd 
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string

def summarize_text(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    
    # Preprocess all sentences
    filtered_sentences = []
    for sentence in sentences:
        # Lowercase, remove punctuation, and remove stop words
        words = [word.lower() for word in nltk.word_tokenize(sentence) if word.lower() not in stop_words and word not in string.punctuation]
        filtered_sentences.append(' '.join(words))
    
    # Implement your sentence scoring logic here (e.g., TF-IDF)
    # This is a placeholder for now, assigning equal scores to all sentences
    sentence_scores = [1 for _ in sentences]
    
    # Sort sentences based on scores (descending order)
    sorted_sentences_scores = sorted(zip(filtered_sentences, sentence_scores), key=lambda x: x[1], reverse=True)
    
    # Extract sorted sentences from the sorted tuples
    sorted_sentences = [sentence for sentence, score in sorted_sentences_scores]
    
    # Join the preprocessed sentences back into a summary
    summary = ' '.join(sorted_sentences)
    return summary


# Configure Gemini API access
genai.configure(api_key="AIzaSyBc9QNEpWjPn-V6btBV__ZAcLUexxu_WOI")

# Set up the model
generation_config = {
  "temperature": 0.7,  # Lower for precise, focused content
  "top_p": 0.95,       # Slightly reduced to focus on more relevant tokens
  "top_k": 50,         # Increased to accommodate technical terms and concepts
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
  # Preprocess and summarize the text
  summary = summarize_text(message)  # Get a 3-sentence summary

  prompt = f"provide notes for the lecture explain in detail: {summary}"
  response = model.generate_content(prompt)

  return f"Sure, here's a summary of what you provided: {response.text}."

while True:
  user_message = input("You: ")
  bot_response = handle_user_message(user_message)
  print(bot_response)


