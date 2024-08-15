from book import BookModel
from flask import Flask, jsonify, request

book = BookModel(
    'book/filtered/Books.csv',
    'preprocessed.csv',
    'model.joblib'
)

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')

    recommendations = book.getRecommendations(title)[1]

    if len(recommendations) == 0:
        return jsonify({'error': f"Book ' {title} ' not found"}), 404
    else:
         return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

