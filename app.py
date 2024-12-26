import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Book Recommendation")
st.header('Popular 50 Books')

# Load popular books
popular_50_books = pickle.load(open('popular_50.pkl', 'rb'))
df = pd.DataFrame(popular_50_books)

# Set up the grid dimensions
num_columns = 5
num_rows = 10

# Display the DataFrame in a grid
index = 0
for row in range(num_rows):
    cols = st.columns(num_columns)
    for col in cols:
        if index < len(df):
            # Display book details
            col.image(df.iloc[index]["IMAGE_URL_M"], width=100)  # Display book cover
            col.markdown(f"""<p style="font-size:12px;"><b>Title:</b> {df.iloc[index]['BOOK_TITLE']}</p>""", unsafe_allow_html=True)
            col.markdown(f"""<p style="font-size:12px;"><b>Author:</b> {df.iloc[index]['BOOK_AUTHOR']}</p>""", unsafe_allow_html=True)
            col.markdown(f"""<p style="font-size:12px;"><b>Rating:</b> {df.iloc[index]['AVG_RATING']:.2f}</p>""",unsafe_allow_html=True)
            index += 1
