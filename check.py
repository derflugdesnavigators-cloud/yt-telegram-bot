import os
import requests

TOKEN = os.environ["TOKEN"]
CHAT_ID = "-1003710777199"

text = "🚀 TEST\n\n If you see this message, Mike is a genius and made his first bot hosted on Github. Youtube Feed + Auto Post should work. Fingers crossed."

send = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    params={"chat_id": CHAT_ID, "text": text}
).json()

msg_id = send["result"]["message_id"]

requests.get(
    f"https://api.telegram.org/bot{TOKEN}/pinChatMessage",
    params={"chat_id": CHAT_ID, "message_id": msg_id}
)
