import requests
import streamlit as st
import json
from groq import Groq
import uuid
from datetime import datetime, timedelta, timezone
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ROUTER_PROMPT = """
You are a router for a market copilot.

Given a user query, classify it into ONE of the following tools:
- social_media_chatbot
- analysts_chatbot
- market_news_chatbot

Return ONLY valid JSON with:
{
  "tool": "...",
  "symbols": [...],
  "reason": "short explanation"
}

User query:
{query}
"""

def market_copilot(query):
    route = route_query(query)
    tool = route["tool"]
    if tool == "social_media_chatbot":
        return reddit_news_chatbot(query)

    return "I’m not sure how to handle that yet."

def groq_generate(prompt):
    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return completion.choices[0].message.content
  
def route_query(query):
    response = groq_generate(ROUTER_PROMPT.format(query=query))
    return json.loads(response.text)

def reddit_news_chatbot(query):
    url = "https://rm96-reddit-market-agent.hf.space/query"
    
    payload = {
        "question": query,
        "lookback_hours": 24
    }
    
    r = requests.post(url, json=payload)
    
    return r


question = st.chat_input("Type your question and press Enter...")
st.write("Questions or feedback? Email hello@stockdoc.biz.")

if question:
  response=market_copilot(question)
  st.write(response)
