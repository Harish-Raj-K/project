import pandas as pd
import streamlit as st

# Load the datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
df = ratings.merge(movies, on="movieId")
df['genres'] = df['genres'].str.replace('|', ' ', regex=False)

# Recommendation Function
def recommend_movies_by_title(movie_title):
    matched = movies[movies['title'].str.contains(movie_title, case=False, na=False)]
    if matched.empty:
        return None, None, None

    selected_movie = matched.iloc[0]
    genre = selected_movie['genres']
    title = selected_movie['title']
    movie_id = selected_movie['movieId']
    avg_rating = ratings[ratings['movieId'] == movie_id]['rating'].mean()

    same_genre_movies = movies[(movies['genres'] == genre) & (movies['movieId'] != movie_id)]
    merged = ratings.merge(same_genre_movies, on='movieId')
    top_movies = (
        merged.groupby(['movieId', 'title'])
        .agg({'rating': 'mean', 'userId': 'count'})
        .reset_index()
    )
    top_movies = top_movies[top_movies['userId'] > 10]
    top_movies = top_movies.sort_values(by='rating', ascending=False)

    return title, round(avg_rating, 2), top_movies.head(5)

# Streamlit UI
st.title("🎬 Movie Recommendation System")

movie_input = st.text_input("Enter a movie name:")
if movie_input:
    title, avg_rating, recommendations = recommend_movies_by_title(movie_input)
    if title:
        st.write(f"**🎬 Selected Movie:** {title}")
        st.write(f"**⭐ Average Rating:** {avg_rating}")
        st.subheader("🎯 Top 5 Recommended Movies from Same Genre:")
        for i, row in recommendations.iterrows():
            st.write(f"🎥 {row['title']} — ⭐ {round(row['rating'], 2)}")
    else:
        st.error("❌ Movie not found. Try another title.")
