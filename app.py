import joblib
import pandas as pd
from flask import Flask, jsonify, request
import re

model = joblib.load('book_recommender_model.joblib')

df = pd.read_csv('preprocessed_book_data.csv')  
books_df = pd.read_csv('book\Books.csv')

df.set_index('Book-Title', inplace=True)  

app = Flask(__name__)

@app.route('/get_index', methods=['GET'])
def get_index():
    return jsonify(df.index.tolist())

def normalize_title(title):
    """Normalize the book title by stripping spaces, lowercasing, and removing special characters."""
    return re.sub(r'\W+', '', str(title).strip().lower())

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title').strip().lower().replace("'", '')

    normalized_title = normalize_title(title)

    try:
        normalized_index = df.index.to_series().apply(normalize_title)
        matching_index = normalized_index.index[normalized_index == normalized_title][0]
    except IndexError:
        return jsonify({'error': f"Book '{title}' not found"}), 404

    recommended_titles = []

    if not pd.isnull(matching_index):
        title = df.index[matching_index]
        book_vector = df.loc[title].values.reshape(1, -1)
        distances, indices = model.kneighbors(book_vector, n_neighbors=6)

        recommended_titles = df.index[indices.flatten()][1:].tolist()

        books_info = []
        for rec_title in recommended_titles:

            normalized_rec_title = normalize_title(rec_title)

            try:
                book_info = books_df.loc[books_df.index.to_series().apply(normalize_title) == normalized_rec_title]
                book_info = book_info.iloc[0]  
                books_info.append({
                    'title': rec_title,
                    'author': book_info['Book-Author'],
                    'year': book_info['Year-Of-Publication'],
                    'publisher': book_info['Publisher']
                })
            except IndexError:
                print(f"Book '{rec_title}' not found in the books DataFrame.")

        return jsonify({'recommended_titles': recommended_titles, 'books_info': books_info})
    else:
        return jsonify({'error': f"Book '{title}' not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

