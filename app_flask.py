# ---------------INSTRUCTIONS TO EXECUTE APP ON LOCAL SERVER-------------------

"""
STEP 1: Run the Streamlit App:
First, make sure the Streamlit app is running. Open a terminal and then run:
COMMAND - streamlit run Movie_app.py

STEP 2: Run the Flask App
In a different terminal run:
COMMAND - python app_flask.py

"""



from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import requests

# Load your models and data
popular_books_df = pickle.load(open('models/popular_books.pkl', 'rb'))
similarity_scores_books = pickle.load(open('models/books_similarity_scores.pkl', 'rb'))
books = pickle.load(open('models/books.pkl', 'rb'))
pt_books = pickle.load(open('models/pt_books.pkl', 'rb'))
popular_movies_df = pickle.load(open('models/popular_movies.pkl', 'rb'))

ids = list(popular_movies_df['id'].values)
movie_images = []
for id in ids: 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=47f5dabb1b608b91fe3ef3ad90ffef57&language=en-US'.format(id))
    data = response.json()
    movie_images.append("https://image.tmdb.org/t/p/w500/" + data['poster_path'])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_books_df['Book-Title'].values),
                           book_author=list(popular_books_df['Book-Author'].values),
                           book_image=list(popular_books_df['Image-URL-M'].values),
                           book_votes=list(popular_books_df['num_ratings'].values),
                           book_rating=list(popular_books_df['avg_ratings'].values),
                           movie_name= list(popular_movies_df['title'].values),
                           movie_images= movie_images,
                           movie_runtime = list(popular_movies_df['runtime'].values),
                           movie_votes = list(popular_movies_df['vote_count'].values),
                           movie_rating = list(popular_movies_df['vote_average'].values),
                           movie_year = list(popular_movies_df['release_date'].values)                    
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/choose_recommendation', methods=['POST'])
def choose_recommendation():
    recommend_type = request.form.get('recommend_type')
    if recommend_type == 'books':
        return redirect(url_for('recommend_books_ui'))
    elif recommend_type == 'movies':
        return redirect('http://localhost:8501')  # Assuming Streamlit is running on port 8501
    return render_template('recommend.html', error="Please select an option.")

@app.route('/recommend_books_ui')
def recommend_books_ui():
    all_books = list(pt_books.index)
    return render_template('book_recommend.html', error=None, all_books=all_books)

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    all_books = list(pt_books.index)
    user_input = request.form.get('user_input')

    if not user_input:
        return render_template('book_recommend.html', error="Please select a book", all_books=all_books)

    try:
        index = np.where(pt_books.index == user_input)[0][0]
    except IndexError:
        return render_template('book_recommend.html', error="Book not found. Please try another book.", all_books=all_books)

    similar_items = sorted(list(enumerate(similarity_scores_books[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt_books.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('book_recommend.html', data=data, error=None, all_books=all_books)

if __name__ == '__main__':
    app.run(debug=True)
