from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>RACK FF YT API IS ONLINE</h1>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        # Cobalt API Request
        payload = {
            "url": video_url,
            "videoQuality": "720",
            "audioFormat": "mp3",
            "downloadMode": "default"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        r = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
        data = r.json()
        
        # Checking for the download link
        final_url = data.get('url')
        
        if final_url:
            return jsonify({
                "success": True,
                "video_url": final_url,
                "owner": "RACK FF YT"
            })
        else:
            return jsonify({"success": False, "error": "Could not find stream URL", "details": data}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
