from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>RACK FF YT | ULTRA ENGINE v5 LIVE</h1>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        # ⚡ Method: Using a High-Speed Mirror API (No Bot Error)
        # Ye server YouTube se direct link nikalta hai bina login maange
        api_url = f"https://api.deemix.biz/download?url={video_url}" 
        
        # Agar upar waali API down ho toh ye Backup:
        fallback_url = f"https://api.vkrdown.com/api/index.php?url={video_url}"

        response = requests.get(api_url, timeout=10)
        data = response.json()

        if data.get('success') or 'url' in data:
            return jsonify({
                "success": True,
                "video_url": data.get('url') or data.get('result'),
                "title": "RACK FF YT Download",
                "owner": "RACK FF YT"
            })
        else:
            # TRY BACKUP
            r2 = requests.get(fallback_url)
            d2 = r2.json()
            return jsonify({
                "success": True,
                "video_url": d2['data']['url'],
                "owner": "RACK FF YT"
            })

    except Exception as e:
        return jsonify({"success": False, "error": "Server Busy, try again in 5 seconds."}), 500

if __name__ == "__main__":
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
