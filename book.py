import pandas as pd
import joblib

class BookModel:
    def __init__(self, dir_book: str, dir_preprocessed: str, dir_model: str):
        self.df_book = BookModel.getDF(dir_book, index='Book-Title')
        self.df_preprocessed = BookModel.getDF(dir_preprocessed, index='Book-Title')
        self.model = joblib.load(dir_model)

    @staticmethod
    def getDF(dir: str, index=''):
        df = pd.read_csv(dir)
        if index != '': 
            df = df.set_index(index)
        return df

    def getAutocompletes(self, query: str):
        if query == '':
            return []
        
        titles = [title for title in self.df_preprocessed.index.tolist() if title.lower().startswith(query.lower())]
        titles.sort()

        return titles
    
    def getAllTitles(self):
        return self.df_preprocessed.index.to_list()
    
    def getRecommendations(self, title: str, min: int):
        if title not in self.df_preprocessed.index:
            print(f"The book '{title}' does not exist in the dataset.")
            return [title, []]

        book_vector = self.df_preprocessed.loc[title].values.reshape(1, -1)

        distances, indices = self.model.kneighbors(book_vector, n_neighbors=min+1)
        distances, indices = distances.flatten()[1:], indices.flatten()[1:]

        df_recommended = pd.DataFrame({
            'title': self.df_preprocessed.index[indices],
            'distance': distances
        }).set_index('title')

        df_recommended = df_recommended.join(self.df_book, how='inner').reset_index().rename(columns={
            "Book-Author": "author",
            "ISBN": "isbn",
            "Image-URL-L": "img-l",
            "Image-URL-M": "img-m",
            "Image-URL-S": "img-s",
            "Publisher": "publisher",
            "Year-Of-Publication": "year" 
        })
        recommended = df_recommended.sort_values(by='distance', ascending=True).to_dict(orient='records')

        return [title, recommended]