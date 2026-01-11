from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<body style='background:#000;color:#0ff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;text-align:center;'><div><h1>RACK FF YT | ULTRA API V3</h1><p>STATUS: ACTIVE (INVIDIOUS CORE)</p></div></body>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    # Extract Video ID
    video_id = ""
    if "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    elif "v=" in video_url:
        video_id = video_url.split("v=")[1].split("&")[0]
    else:
        video_id = video_url.split("/")[-1].split("?")[0]

    # Invidious Instances (Agar ek down ho toh dusra kaam kare)
    instances = [
        "https://invidious.snopyta.org",
        "https://yewtu.be",
        "https://invidious.kavin.rocks"
    ]

    for instance in instances:
        try:
            api_url = f"{instance}/api/v1/videos/{video_id}"
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                # Sabse best quality wala format dhundna
                formats = data.get('formatStreams', [])
                if formats:
                    # Sabse upar wala (best) format le lo
                    best_video = formats[0].get('url')
                    return jsonify({
                        "success": True,
                        "video_url": best_video,
                        "title": data.get('title'),
                        "owner": "RACK FF YT"
                    })
        except:
            continue

    return jsonify({"success": False, "error": "All backup servers are busy. Try again in 1 min."}), 500

app.debug = True
