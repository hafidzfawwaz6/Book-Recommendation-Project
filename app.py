from book import BookModel
from flask import Flask, jsonify, request
from flask_cors import CORS

book_model = BookModel(
    'book/filtered/Books.csv',
    'preprocessed.csv',
    'model.joblib'
)

app = Flask(__name__)
CORS(app)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')

    return jsonify(book_model.getAutocompletes(query)), 200 

@app.route('/getalltitles', methods=['GET'])
def getalltitles():
    return jsonify(book_model.getAllTitles()), 200

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')

    recommendations = book_model.getRecommendations(title=title, min=10)[1]

    if len(recommendations) == 0:
        return jsonify({'error': f"Book ' {title} ' not found"}), 404
    else:
         return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True)

