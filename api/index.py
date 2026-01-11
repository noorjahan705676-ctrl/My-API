from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<body style='background:#000;color:#0f0;display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;text-align:center;'><div><h1>RACK FF YT | API v2.0</h1><p>STATUS: ONLINE</p></div></body>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    try:
        # Using a much more stable API bypass
        # Ye API direct video info nikalne ke liye design ki gayi hai
        api_url = f"https://api.vkrdown.com/api/index.php?url={video_url}"
        
        response = requests.get(api_url)
        data = response.json()
        
        # Check if we got the data
        if data.get('status') == 'success' or 'data' in data:
            # Different APIs have different formats, finding the best link
            video_info = data.get('data', {})
            download_url = video_info.get('url') or video_info.get('main_url')
            
            return jsonify({
                "success": True,
                "video_url": download_url,
                "title": video_info.get('title', 'Video Download'),
                "owner": "RACK FF YT"
            })
        else:
            return jsonify({"success": False, "error": "Extraction Failed", "details": data}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

app.debug = True
