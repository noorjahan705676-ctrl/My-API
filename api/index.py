from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# --- YOUR PERSONAL BRANDING ---
DEV_NAME = "RACK FF YT"
YT_LINK = "https://youtube.com/@rackff7"
ABOUT = "Advanced Python Developer & Gaming Content Creator. Specializing in Automation Tools."

# --- NEON DASHBOARD UI ---
DASHBOARD_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{DEV_NAME} | CORE API</title>
    <style>
        :root {{ --neon: #ff0055; --bg: #050505; }}
        body {{ background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; overflow: hidden; }}
        .card {{ width: 350px; background: rgba(20,20,20,0.8); border: 1px solid var(--neon); padding: 30px; border-radius: 25px; text-align: center; backdrop-filter: blur(15px); box-shadow: 0 0 40px rgba(255,0,85,0.2); position: relative; }}
        .card::before {{ content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px; background: var(--neon); border-radius: 25px; z-index: -1; opacity: 0.1; }}
        .profile-img {{ width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--neon); margin-bottom: 15px; box-shadow: 0 0 15px var(--neon); }}
        h1 {{ font-size: 24px; margin: 10px 0; letter-spacing: 2px; text-shadow: 0 0 10px var(--neon); }}
        p {{ color: #888; font-size: 13px; line-height: 1.5; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; border-top: 1px solid #222; pt: 15px; }}
        .stat-box h4 {{ color: var(--neon); margin: 0; font-size: 16px; }}
        .stat-box span {{ font-size: 10px; color: #555; }}
        .btn {{ display: block; background: var(--neon); color: #fff; text-decoration: none; padding: 12px; border-radius: 12px; font-weight: bold; transition: 0.4s; margin-top: 15px; box-shadow: 0 5px 15px rgba(255,0,85,0.4); }}
        .btn:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px rgba(255,0,85,0.6); }}
        .endpoint {{ margin-top: 20px; font-family: monospace; font-size: 11px; color: #555; background: #111; padding: 8px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="card">
        <div style="font-size: 40px; margin-bottom: 10px;">🔥</div>
        <h1>{DEV_NAME}</h1>
        <p>{ABOUT}</p>
        
        <div class="stats">
            <div class="stat-box"><h4>ACTIVE</h4><span>STATUS</span></div>
            <div class="stat-box"><h4>V1.0</h4><span>VERSION</span></div>
            <div class="stat-box"><h4>FAST</h4><span>SPEED</span></div>
        </div>

        <a href="{YT_LINK}" target="_blank" class="btn">VISIT MY CHANNEL</a>
        
        <div class="endpoint">
            GET /download?url=[link]
        </div>
        <div style="margin-top: 15px; font-size: 9px; color: #444;">© 2026 RACK FF YT | ALL RIGHTS RESERVED</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML)

@app.route('/download')
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
