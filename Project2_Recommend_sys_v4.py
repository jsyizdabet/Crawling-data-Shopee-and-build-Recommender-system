import streamlit as st
import pandas as pd
from gensim import corpora, models, similarities
import matplotlib.pyplot as plt
import numpy as np

# Load product data from a CSV file
@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename)
    #df=df.dropna(subset=['image'])
    #df=df[df["image"].str.contains("nan")==False]
    # Clean the product descriptions by removing non-alphabetic characters and converting to lowercase
    #df['products_wt'] = df['products_wt'].apply(lambda x: re.sub('[^a-zA-Z]', ' ', x).lower())
    return df

# Preprocess the data and train the TF-IDF model
@st.cache_data
def train_model(df):
    texts= [[text for text in x.split()] for x in df.products_wt]
    texts = [[t.lower() for t in text if not t in ['', ' ', ',', '.', '...', '-',':', ';', '?', '%', '_%' , '(', ')', '+', '/', 'g', 'ml']] for text in  texts] # ký tự đặc biệt
    dictionary = corpora.Dictionary(texts)
    #dictionary.token2id 
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    return df, dictionary, corpus, tfidf

# Define a function to recommend products based on user input
def recommend_products(query, df, dictionary, corpus, tfidf):
    
    # Preprocess the query and compute its TF-IDF vector
    query_bow = dictionary.doc2bow(query.lower().split())
    query_tfidf = tfidf[query_bow]

    # Compute the cosine similarity between the query and product descriptions
    index = similarities.MatrixSimilarity(tfidf[corpus])
    results  = index[query_tfidf]
    results  = sorted(enumerate(results), key=lambda item: -item[1])[:5]
    return results 

def recommend_products_2(query, df, dictionary, corpus, tfidf):
    
    # Preprocess the query and compute its TF-IDF vector
    query_bow = dictionary.doc2bow(query.lower().split())
    query_tfidf = tfidf[query_bow]

    # Compute the cosine similarity between the query and product descriptions
    index = similarities.MatrixSimilarity(tfidf[corpus])
    sims = index[query_tfidf]
    # Sort the products by similarity score and return the top results
    results = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:5]
    return results

   
    # Sort the products by similarity score and return the top results
    
menu = ["Business Objective", "Content-based Filtering","Collaborative Filtering"]
choice = st.sidebar.selectbox('Menu', menu)



if choice == 'Business Objective':    
    st.subheader("Business Objective")
    st.write ("""###### I.	What is a Recommender System? 
A recommender system is a system that helps customers/users discover products or services they may like. It is like a salesman of a company who knows what a customer might like based on their history and preferences.
Types of Recommender Systems
1) Content-Based Filtering
The main idea here is to suggest items based on a particular item. For example, when you are building a movie recommendation system, it would take into account a user’s preference for a movie using metrics such as ratings and then use item metadata, such as genre, director, description of the movie, cast, and crew, etc to find movies similar to the ones that a user has liked.
2) Collaborative Filtering
The collaborative filtering recommendation technique depends on finding similar users to a target user to make personalized recommendations. Collaborative filtering recommen,der systems do not require item metadata like content-based recommendation systems. It relies solely on past user-item interactions to render new recommendations""")  
    st.image("recommend sys.jpg") 
    st.write ("""###### II.	Bussiness Objective
Shopee is the leading e-commerce platform in Southeast Asia and Taiwan. Launched in 2015, the Shopee commerce platform was built to provide users with an easy, safe and fast experience when shopping online through a strong payment support and operating system, shopee.vn is the top 1 e-commerce website in Vietnam and Southeast Asia.
Shoppee wants to launch the first trial Recommend sys system on men's fashion category
""")
    st.markdown("[Link to  Shoppe app](https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567/)")
    st.image("Shopee-logo.png")
    
    #filename = "Products_ThoiTrangNam_raw_tokenize.csv"
    #df = load_data(filename)
    #sorted_df=df.groupby(['sub_category']).mean()['rating'].sort_values(ascending= False)
    #st.markdown("Men's Fashion Category")
    #st.write(sorted_df)
    #fig, ax = plt.subplots()
    #sorted_df.plot(kind='bar', ax=ax)
    #ax.set_title('Average rating by sub_category')
    #ax.set_xlabel('sub_category')
    #ax.set_ylabel('Average rating')
    #st.pyplot(fig)
elif choice == 'Content-based Filtering':
    filename = "Products_ThoiTrangNam_raw_tokenize.csv"
    df = load_data(filename)
    df, dictionary, corpus, tfidf = train_model(df)
    st.markdown("Content-based Filtering")
    
    type = st.radio("Filter data or Input data?", options=("Filter", "Input"))
    
    if type=="Input":
# Build the Streamlit app
        st.subheader("Content-based Filtering")
# Get user input query
        query = st.text_input("Enter a product name:")
        
        
# Recommend products based on the query
        if query:
            results = recommend_products(query, df, dictionary, corpus, tfidf)
            if results:
                st.write("Here are the top results:")
                for i, sim in enumerate(results ):
                    doc_index = sim[0]
                    doc_score = round(sim[1], 2)
                    st.write(f"Recommendation {i+1}: Score - {doc_score}")
                    st.write(df.loc[doc_index, 'product_name'])
                    st.image(df.loc[doc_index, 'image'])
                #st.write(df.loc[doc_index, 'link'])
                    st.write("[View on website]({})".format(df.loc[doc_index, 'link']))
            else:
                st.write('No recommendations found.')
    else:
        st.subheader("Content-based Filtering")
        product_options = df['product_name'].unique()
        selected_product__name = st.selectbox('Select Product name:', product_options)
        query=df['product_name'][df['product_name']==selected_product__name].item()
        results = recommend_products_2(query, df, dictionary, corpus, tfidf)
        if results:
            st.write("Here are the top results:")
            for i, sim in enumerate(results ):
                doc_index = sim[0]
                doc_score = round(sim[1], 2)
                st.write(f"Recommendation {i+1}: Score - {doc_score}")
                st.write(df.loc[doc_index, 'product_name'])
                st.image(df.loc[doc_index, 'image'])
                #st.write(df.loc[doc_index, 'link'])
                st.write("[View on website]({})".format(df.loc[doc_index, 'link']))
        else:    
            st.write('No recommendations found.')
 
                      
elif choice == 'Collaborative Filtering':
    st.title("Collaborative Filtering Project")
# Load and preprocess the data
    #filename = "result_final.csv"
    #df2 = load_data(filename)
    #filename = "Products_ThoiTrangNam_raw_tokenize.csv"
    #df = load_data(filename)
    #all_data_3 = pd.merge(df, df2, on='product_id')
    filename = "Products_ThoiTrangNam_raw_cleaning2.csv"
    all_data_3 = load_data(filename)
    user_options = all_data_3 ['user_id'].unique()
    selected_user_id = st.selectbox('Select User ID:', user_options)
    result=all_data_3[['user_id','user','product_id','product_name','sub_category','link','image','price']][all_data_3['user_id']==selected_user_id]
    st.write("Here are the top results:")
    def display_data(row):
        st.image(row['image'], caption=row['product_name'], width=200)
        #st.write(row['link'])
        st.write("[View on website]({})".format(row['link']))

    

# Display data for each row in the CSV file
    for index, row in result.iterrows():
        display_data(row)
