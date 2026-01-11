from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<body style='background:#000;color:#0f0;display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;'><h1>RACK FF YT | YT-DLP ENGINE LIVE</h1></body>"

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    
    # Termux wala yt-dlp configuration
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'no_cache_dir': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extracting information like Termux
            info = ydl.extract_info(video_url, download=False)
            video_link = info.get('url')
            
            if video_link:
                return jsonify({
                    "success": True, 
                    "video_url": video_link,
                    "title": info.get('title'),
                    "owner": "RACK FF YT"
                })
            else:
                return jsonify({"success": False, "error": "Could not fetch direct link"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

app.debug = True                formats = res.get('data', {}).get('formats', [])
            
            # Get the first working URL
            download_link = formats[0].get('url')
            
            return jsonify({
                "success": True,
                "video_url": download_link,
                "title": res.get('data', {}).get('title', 'RACK_FF_VIDEO'),
                "owner": "RACK FF YT"
            })
        else:
            # Fallback to another secret engine if first fails
            return jsonify({"success": False, "error": "YouTube is blocking this request. Try another link."}), 403

    except Exception as e:
        return jsonify({"success": False, "error": "Server error, try again later."}), 500

app.debug = True
