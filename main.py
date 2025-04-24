
# victor_watchlist_bot

import os
import openai
import requests
import logging
import telegram
import gspread
from datetime import datetime
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SHEET_ID = os.getenv("SHEET_ID")

# Setup Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Setup OpenAI
openai.api_key = OPENAI_API_KEY

def get_watchlist():
    return [name.strip() for name in sheet.col_values(1) if name.strip()]

def fetch_news(company):
    url = f"https://www.google.com/search?q={company}+news&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [a.text for a in soup.select("h3")[:3]]
    return headlines

def summarize_news(company, headlines):
    prompt = f"Give a short professional summary of the following news headlines for {company}:\n" + "\n".join(headlines)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        logging.error(f"Error summarizing news: {e}")
        return f"Could not summarize news for {company}."

def generate_daily_report():
    watchlist = get_watchlist()
    summaries = []
    for company in watchlist:
        headlines = fetch_news(company)
        if headlines:
            summary = summarize_news(company, headlines)
            summaries.append(f"\n📰 *{company}*\n{summary}")
        else:
            summaries.append(f"\n📰 *{company}*\nNo recent news found.")
    return "\n".join(summaries)

def send_daily_report():
    report = f"📊 *Victor's Watchlist Daily Briefing* ({datetime.now().strftime('%Y-%m-%d')})\n" + generate_daily_report()
    bot.send_message(chat_id=USER_ID, text=report, parse_mode=telegram.ParseMode.MARKDOWN)

if __name__ == "__main__":
    send_daily_report()
