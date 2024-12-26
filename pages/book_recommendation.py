import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Book Recommendation")
st.header('Book Recommendation')

# Load popular books
pt = pickle.load(open('pt.pkl', 'rb'))  # Pivot table or similar structure
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))  # DataFrame with book info

# Recommendation function
def book_recommend_web(book_name):
    # Check if the book exists in the index
    if book_name not in pt.index:
        st.error(f"The book '{book_name}' is not available in the dataset.")
        return pd.DataFrame()

    # Fetch the index of the selected book
    index = np.where(pt.index == book_name)[0][0]

    # Find similar items
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:8]

    # Prepare DataFrame with recommended books
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['BOOK_TITLE'] == pt.index[i[0]]]
        if not temp_df.empty:
            item.extend(list(temp_df.drop_duplicates('BOOK_TITLE')['BOOK_TITLE'].values))
            item.extend(list(temp_df.drop_duplicates('BOOK_TITLE')['BOOK_AUTHOR'].values))
            item.extend(list(temp_df.drop_duplicates('BOOK_TITLE')['IMAGE_URL_M'].values))
        else:
            continue
        data.append(item)

    # If no recommendations, return empty DataFrame
    if not data:
        st.error("No recommendations could be found.")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["BOOK_TITLE", "BOOK_AUTHOR", "IMAGE_URL_M"])
    return df

# Extract book titles
book_list = books['BOOK_TITLE'].drop_duplicates().values

# Select a book
selected_book_name = st.selectbox("Select a Book for recommendations:", pt.index)

# Recommend books
if st.button("Recommend"):
    try:
        recommend_book_df = book_recommend_web(selected_book_name)
        if not recommend_book_df.empty:
            # Display recommended books
            cols = st.columns(len(recommend_book_df))
            for idx, col in enumerate(cols):
                with col:
                    st.image(recommend_book_df['IMAGE_URL_M'][idx])
                    st.text(recommend_book_df['BOOK_TITLE'][idx])

    except Exception as e:
        st.error(f"An error occurred: {e}")
