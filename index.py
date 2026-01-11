from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "RACK FF YT SERVER IS LIVE"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        ydl_opts = {'format': 'best', 'quiet': True, 'nocheckcertificate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "success": True, 
                "video_url": info.get('url'),
                "title": info.get('title')
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Render port binding
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
