from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# A simple in-memory database
database = {}

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Create a simple hash of the URL
    short_code = hashlib.md5(url.encode()).hexdigest()[:6]
    database[short_code] = url
    return jsonify({'short_url': f'http://your-domain.com/{short_code}'})

@app.route('/<short_code>', methods=['GET'])
def redirect(short_code):
    url = database.get(short_code)
    if not url:
        return jsonify({'error': 'URL not found'}), 404
    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(debug=True)
