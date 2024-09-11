import pandas as pd
import joblib

class BookModel:
    def __init__(self, dir_book: str, dir_preprocessed: str, dir_model: str):
        self.df_book = BookModel.getDF(dir_book, index='Book-Title')
        self.df_preprocessed = BookModel.getDF(dir_preprocessed, index='ISBN')
        self.model = joblib.load(dir_model)

    @staticmethod
    def getDF(dir: str, index=''):
        df = pd.read_csv(dir)
        if index != '': 
            df.set_index(index, inplace=True)
        return df

    def getIsbns(self, title: str):
        if title in self.df_book.index:
            return self.df_book.loc[title, 'ISBN'].values
        else:
            return []

    def getAutocompletes(self, query: str):
        if query == '':
            return []
        
        titles = [title for title in self.df_preprocessed.index.tolist() if title.lower().startswith(query.lower())]
        titles.sort()

        return titles

    def getRecommendations(self, title: str):
        isbns = self.getIsbns(title)
        if len(isbns) == 0 or not any(isbn in self.df_preprocessed.index for isbn in isbns):
            print(f"The book '{title}' does not exist in the dataset.")
            return [title, []]

        isbn = isbns[0]

        book_vector = self.df_preprocessed.loc[isbn].values.reshape(1, -1)

        distances, indices = self.model.kneighbors(book_vector, n_neighbors=6)
        distances, indices = distances.flatten()[1:], indices.flatten()[1:]

        isbns = self.df_preprocessed.index[indices]

        df_recommended = pd.DataFrame({
            'isbn': self.df_preprocessed.index[indices],
            'distance': distances
        }).set_index('isbn')
        
        self.df_book.set_index('ISBN', inplace=True)
        df_recommended = df_recommended.join(self.df_book, how='inner').reset_index().rename(columns={
            "Book-Author": "author",
            "Book-Title": "title",
            "Image-URL-L": "img-l",
            "Image-URL-M": "img-m",
            "Image-URL-S": "img-s",
            "Publisher": "publisher",
            "Year-Of-Publication": "year" 
        })
        self.df_book.set_index('Book-Title', inplace=True)
        recommended = df_recommended.sort_values(by='distance', ascending=True).to_dict(orient='records')

        return [title, recommended]