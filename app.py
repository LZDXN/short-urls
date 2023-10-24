from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/urlshortener"
mongo = PyMongo(app)

@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.json.get('url')
    custom_short_code = request.json.get('short_code')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    if custom_short_code:
        if mongo.db.urls.find_one({"short_code": custom_short_code}):
            return jsonify({'error': 'Short code already in use'}), 400
        short_code = custom_short_code
    else:
        # Generate a unique short code
        short_code = ...  # your code for generating a short code

    new_url = {"original_url": url, "short_code": short_code}
    mongo.db.urls.insert_one(new_url)

    domain = os.getenv('DOMAIN_NAME')
    return jsonify({'short_url': f'http://{domain}/{short_code}'})

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    url = mongo.db.urls.find_one({"short_code": short_code})
    if not url:
        return jsonify({'error': 'URL not found'}), 404
    return redirect(url['original_url'], code=302)

if __name__ == '__main__':
    app.run(debug=True)
