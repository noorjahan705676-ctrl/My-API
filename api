from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Neon Home Screen for Vercel
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RACK_FF | VERCEL CORE</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .box { border: 2px solid #00ff00; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 0 20px #00ff00; }
        h1 { letter-spacing: 5px; margin: 0; }
        .status { color: #fff; margin-top: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>VERCEL API</h1>
        <div class="status">STATUS: ONLINE [SERVERLESS]</div>
        <p style="font-size: 10px; color: #666;">READY FOR GLASS UI CONNECTION</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'cachedir': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "success": True, 
                "video_url": info.get('url'),
                "title": info.get('title')
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Vercel needs this
app.debug = True
