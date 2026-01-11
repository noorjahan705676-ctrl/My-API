from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# --- BRANDING ---
DEV_NAME = "RACK FF YT"
YT_LINK = "https://youtube.com/@rackff7"

@app.route('/')
def home():
    return f"<h1>{DEV_NAME} API IS LIVE</h1><p>Send GET request to /download?url=YOUR_URL</p>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    # Hum Cobalt API ka use karenge jo YouTube block nahi karta
    cobalt_api = "https://api.cobalt.tools/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "url": video_url,
        "videoQuality": "720", # 720p quality
        "filenamePattern": "basic"
    }

    try:
        response = requests.post(cobalt_api, json=data, headers=headers)
        res_data = response.json()
        
        if res_data.get('status') == 'stream' or res_data.get('status') == 'picker':
            # Agar 'picker' hai toh pehla link le lo, agar 'stream' hai toh direct link
            final_url = res_data.get('url')
            return jsonify({
                "success": True, 
                "video_url": final_url,
                "title": "Video Download Ready",
                "owner": DEV_NAME
            })
        else:
            return jsonify({"success": False, "error": "Could not extract link"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

app.debug = True@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "success": True, 
                "video_url": info.get('url'),
                "title": info.get('title'),
                "owner": DEV_NAME
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

app.debug = True
