from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DEV_NAME = "RACK FF YT"

@app.route('/')
def home():
    return f"<body style='background:#000;color:#0f0;display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;'><h1>{DEV_NAME} API IS ONLINE</h1></body>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        # Cobalt API Request
        response = requests.post(
            "https://api.cobalt.tools/api/json",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"url": video_url, "videoQuality": "720"}
        )
        
        data = response.json()
        
        # Cobalt returns 'url' directly if it's a single video
        # or 'picker' if there are multiple options
        final_link = data.get('url') or (data.get('picker')[0].get('url') if data.get('picker') else None)

        if final_link:
            return jsonify({
                "success": True,
                "video_url": final_link,
                "owner": DEV_NAME
            })
        else:
            return jsonify({"success": False, "error": "Link extraction failed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Required for Vercel
app.debug = True    
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
