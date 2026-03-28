import os
import requests
import feedparser

RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCshyfrLaCobJZJzhEnvMwtg"
CHAT_ID = "-1003710777199"

TOKEN = os.environ["8670459256:AAEdA6Ne9qzVj2I4gTNwYCYqYkzC3Wt2XVU"]

feed = feedparser.parse(RSS)
entry = feed.entries[0]

title = entry.title
link = entry.link

text = f"🚀 New Video or Live Stream!\n\n{title}\n\n{link}"

send = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": text}
).json()

msg_id = send["result"]["message_id"]

requests.get(
    f"https://api.telegram.org/bot{TOKEN}/pinChatMessage",
    params={"chat_id": CHAT_ID, "message_id": msg_id}
)
