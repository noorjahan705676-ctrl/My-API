from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<body style='background:#000;color:#f00;display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;'><h1>RACK FF YT | API v10 LIVE</h1></body>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        # Nayi Cobalt v10 API URL aur Data
        cobalt_v10 = "https://api.cobalt.tools/api/json"
        payload = {
            "url": video_url,
            "videoQuality": "720",
            "filenamePattern": "basic"
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        r = requests.post(cobalt_v10, json=payload, headers=headers)
        data = r.json()
        
        # v10 mein status 'stream' ya 'redirect' hota hai
        if data.get('status') == 'stream' or data.get('status') == 'redirect':
            return jsonify({
                "success": True,
                "video_url": data.get('url'),
                "owner": "RACK FF YT"
            })
        elif data.get('status') == 'picker':
            # Agar multiple qualities milein
            return jsonify({
                "success": True,
                "video_url": data.get('picker')[0].get('url'),
                "owner": "RACK FF YT"
            })
        else:
            return jsonify({
                "success": False, 
                "error": data.get('text', 'API Error'),
                "full_response": data
            }), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

app.debug = True
