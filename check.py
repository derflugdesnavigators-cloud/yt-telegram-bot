import os
from pathlib import Path

import feedparser
import requests

RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCshyfrLaCobJZJzhEnvMwtg"
CHAT_ID = "-1003710777199"
STATE_FILE = Path("last_video_id.txt")

TOKEN = os.environ["TOKEN"]


def load_last_video_id():
    if STATE_FILE.exists():
        return STATE_FILE.read_text(encoding="utf-8").strip()
    return ""


def save_last_video_id(video_id):
    STATE_FILE.write_text(video_id, encoding="utf-8")


def telegram(method, data):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    response = requests.post(url, data=data, timeout=30)
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error in {method}: {result}")
    return result


def main():
    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("No feed entries found.")
        return

    entry = feed.entries[0]
    video_id = entry.get("yt_videoid", "") or entry.link
    title = entry.title
    link = entry.link

    last_id = load_last_video_id()

    # Erster Start: nur merken, noch nichts posten
    if not last_id:
        save_last_video_id(video_id)
        print(f"Initialized with latest video: {video_id}")
        return

    # Kein neues Video / kein neuer Stream
    if video_id == last_id:
        print("No new video.")
        return

    text = f"🚀 New video or livestream\n\n{title}\n\n👉 {link}"

    sent = telegram("sendMessage", {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": "false",
    })

    message_id = sent["result"]["message_id"]

    telegram("pinChatMessage", {
        "chat_id": CHAT_ID,
        "message_id": str(message_id),
        "disable_notification": "true",
    })

    save_last_video_id(video_id)
    print(f"Posted and pinned new video: {video_id}")


if __name__ == "__main__":
    main()
