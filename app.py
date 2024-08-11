import joblib
import pandas as pd
from flask import Flask, jsonify, request

df = pd.readcsv('Books.csv') 

app = Flask(__name__)

@app.route('/get_index', methods=['GET'])
def get_index():
    return jsonify(df.index.tolist())

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if title not in df.index:
        return jsonify({'error': f"Book '{title}' not found"}), 404
    return jsonify({'message': 'Recommendation logic here'})

if __name__ == '__main__':
    app.run(debug=True)