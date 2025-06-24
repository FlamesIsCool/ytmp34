import os
import uuid
from flask import Flask, request, send_file, jsonify, send_from_directory
import yt_dlp

app = Flask(__name__, static_folder='static')

# Secret cookies file path
COOKIES_PATH = "/etc/secrets/cookies.txt"  # matches your secret file on Render

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json(force=True)
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    file_id = str(uuid.uuid4()) + ".mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_id,
        'cookiefile': COOKIES_PATH,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(file_id, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_id):
            os.remove(file_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
