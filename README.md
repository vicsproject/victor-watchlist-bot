
# Victor's Watchlist Bot

This bot sends you daily news summaries via Telegram for companies listed in your Google Sheet.

## 🛠 Setup

1. **Clone or Download this Repo**
2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up `.env`**
   Copy `.env.example` to `.env` and fill in your tokens:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   USER_ID=your_telegram_user_id
   OPENAI_API_KEY=your_openai_api_key
   SHEET_ID=your_google_sheet_id
   ```

4. **Google Sheets API**
   - Go to Google Cloud Console → APIs & Services
   - Enable “Google Sheets API” and “Google Drive API”
   - Create service account and download `credentials.json`
   - Share your sheet with the service account email

5. **Test the Bot**
   ```bash
   python main.py
   ```

## ☁ Deployment

Use Render or any cloud platform to run the script daily at 6am using cron or scheduler.

