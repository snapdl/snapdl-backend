from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Taaki tera Vercel wala frontend isse easily connect ho sake

@app.route('/getInfo', methods=['POST'])
def get_info():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Extract required details
            title = info.get('title', 'Unknown Title')
            thumbnail = info.get('thumbnail', '')
            duration = info.get('duration_string', 'N/A')
            
            # Formats / direct download links gathering
            formats_data = []
            for f in info.get('formats', []):
                if f.get('url') and f.get('ext') == 'mp4' and f.get('height'):
                    formats_data.append({
                        'resolution': f'{f.get("height")}p',
                        'url': f.get('url'),
                        'filesize': f'{round(f.get("filesize", 0) / (1024*1024), 1)} MB' if f.get('filesize') else 'Unknown'
                    })

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'duration': duration,
                'formats': formats_data[:6] # Top formats send karenge
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
