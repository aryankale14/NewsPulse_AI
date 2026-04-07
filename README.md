<div align="center">
  <h1>⚡ NewsPulse AI</h1>
  <p>An intelligent, autonomous Telegram Bot delivering highly personalized daily news briefings powered by Google Gemini and Google Search Grounding.
    Live Bot: https://t.me/Aryan_ka_news_bot
  </p>

  ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
  ![Telegram API](https://img.shields.io/badge/python--telegram--bot-v21+-blue.svg)
  ![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange.svg)
  ![License](https://img.shields.io/badge/License-MIT-green.svg)
</div>

---

## 🚀 Overview

**NewsPulse AI** acts as your personal AI news anchor. Rather than scrolling blindly through massive news feeds, NewsPulse utilizes the `gemini-2.5-flash` LLM—actively grounded in real-time Google Search results—to bypass static knowledge cutoffs and fetch verified, high-quality, up-to-the-minute global headlines. 

The bot runs 24/7, silently compiling the world's most critical stories during the day, and deploying them to subscribers every morning (9:00 AM) and evening (5:30 PM) based solely on their custom category preferences.

---

## ✨ Key Features

- **🌐 AI-Driven Fact-Based Sourcing**: Pulls high-quality, real-time summaries automatically verified via Google Search Grounding to avoid AI hallucinations.
- **🎛️ 10 Interactive Categories**: Users can toggle subscriptions for specific topics right from their chat:
  - Top Stories / Trending | World News | India National | Indian Politics | Sports | Business & Economy | Tech | Health | Science | Entertainment.
- **⚙️ Automated Cron Scheduling**: Built on APScheduler (`JobQueue`), triggering automated fetching and background broadcasts without any server delays.
- **🧠 Zero "Groundhog Day" Deduplication**: Injects an intelligent contextual cache parameter into the evening prompt, explicitly ordering the AI to find fresh twilight headlines so users don't read the same stories twice in one day.
- **💾 SQLite Persistent Storage**: Uses a lightweight, portable `subscribers.db` to permanently track users and their granular notification settings.
- **☁️ Cloud-Ready Architecture**: Built to deploy flawlessly on ephemeral container platforms like **Railway** (incorporating built-in volume mounting via the `DB_PATH` env variable).

---

## 🛠️ Prerequisites

Before you launch the bot, ensure you have the following:

- **Python 3.10+**
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

---

## 💻 Local Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/NewsPulse-AI.git
   cd NewsPulse-AI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**  
   Create a file named `.env` in the root directory and add your secret keys:
   ```env
   TELEGRAM_BOT_TOKEN="your_telegram_token"
   GEMINI_API_KEY="your_gemini_token"
   ADMIN_CHAT_ID="your_personal_telegram_chat_id" # Used for crash alerts and admin commands
   ```

4. **Launch the Engine**
   ```bash
   python tele_news.py
   ```

---

## ☁️ Deploying to Railway.app

This bot is fully configured for 1-click cloud deployment.

1. **Push to GitHub**: Upload this repository excluding your `.env` and `*.db` files (handled by the included `.gitignore`).
2. **Deploy**: Go to [Railway](https://railway.app/), start a New Project, and attach your GitHub repo.
3. **Set Variables**: In the Railway Variables tab, enter your `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, and `ADMIN_CHAT_ID`.
4. **Persistent Database Volume** *(Crucial)*:
   - Go to your Railway Service **Settings**.
   - Scroll down to **Volumes** and click "Add Volume".
   - Set the Mount Path to `/data`.
   - Go back to Variables and add `DB_PATH=/data/subscribers.db`.
5. Railway handles the provided `Procfile` natively. Once variables are loaded, the bot will initialize and run perpetually!

---

## 🤖 Bot Commands

### Standard Users
- `/start` - Boot up the bot, register to the database, and receive the menu.
- `/change_category` - Opens the Inline Keyboard to toggle news categories.
- `/stop` - Instantly wipes the user out of the database and halts daily broadcasts.

### Admin Exclusive
- `/stats` - Returns a current metric of active unique subscribers.
- `/prefetch` - Manually triggers the Gemini search engine to rebuild the local cache.
- `/broadcast` - Bypasses the schedule and instantly spams all active users with the cached news.

---

> _**Disclaimer**: This bot aggregates news from the open internet via Google APIs. It is subject to Google Gemini rate limits and standard Telegram Bot broadcasting quotas._
