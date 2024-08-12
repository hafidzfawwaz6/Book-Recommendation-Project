import joblib
import pandas as pd
from flask import Flask, jsonify, request

model = joblib.load('book_recommender_model.joblib')

df = pd.read_csv('preprocessed_book_data.csv')  

df.set_index('Book-Title', inplace=True)  

app = Flask(__name__)

@app.route('/get_index', methods=['GET'])
def get_index():
    return jsonify(df.index.tolist())

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    title = "I'll be Seeing You".strip().lower().replace("'", '')

    # Find the index of the matching title (if it exists)
    matching_index = df.index.str.strip().str.lower().str.replace("'", '').get_loc(title)

    if not pd.isnull(matching_index):
        title = df.index[matching_index]
        book_vector = df.loc[title].values.reshape(1, -1)
        distances, indices = model.kneighbors(book_vector, n_neighbors=6)

        recommended_books = pd.DataFrame({
            'title': df.index[indices.flatten()][1:],  
            'distance': distances.flatten()[1:]       
        })
        return jsonify(recommended_books.to_dict(orient='records'))
    
    else:
        return jsonify({'error': f"Book '{title}' not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

