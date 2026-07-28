import streamlit as st
import pickle
import requests


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)



# ==========================
# CUSTOM DESIGN
# ==========================

st.markdown("""
<style>

.stApp {

background:
linear-gradient(
rgba(0,0,0,0.80),
rgba(0,0,0,0.90)
),
url("https://wallpapercave.com/wp/wp9114115.jpg");

background-size:cover;
background-attachment:fixed;

}



h1 {

color:#FFD700;
text-align:center;
font-size:45px;

}



.subtitle {

color:white;
text-align:center;
font-size:20px;

}



.info-card {

background:rgba(255,255,255,0.08);

border:1px solid rgba(255,255,255,0.15);

padding:20px;

border-radius:15px;

color:white;

font-size:15px;

line-height:1.7;

}



.movie-card {

background:rgba(255,255,255,0.08);

padding:12px;

border-radius:15px;

text-align:center;

}



.movie-title {

color:white;

font-size:17px;

font-weight:bold;

}



</style>

""", unsafe_allow_html=True)




# ==========================
# ABOUT PROJECT FUNCTION
# ==========================

def about_project():

    st.sidebar.markdown(
    """
    <div class="info-card">

    <h2 style="color:#FFD700;">
    🎬 About Project
    </h2>


    <b>Movie Recommendation System</b>


    <br><br>


    An AI-powered movie recommendation engine
    that recommends similar movies using
    machine learning techniques.


    <br><br>


    👨‍💻 <b>Developer:</b><br>

    Vansh Sharma


    <br><br>


    🧠 <b>Machine Learning Approach:</b><br>

    • Content Based Filtering<br>
    • Cosine Similarity Algorithm


    <br><br>


    ⚙️ <b>Technology Stack:</b><br>

    • Python<br>
    • Pandas<br>
    • NumPy<br>
    • Scikit-Learn<br>
    • Streamlit<br>
    • TMDB API


    <br><br>


    ✨ <b>Features:</b><br>

    ✓ Smart movie recommendations<br>
    ✓ Similarity based prediction<br>
    ✓ Dynamic movie posters<br>
    ✓ Interactive web interface


    <br><br>


    🎯 <b>Project Objective:</b><br>

    To build an intelligent system that helps
    users discover similar movies through
    data-driven recommendations.


    </div>

    """,
    unsafe_allow_html=True
    )



# calling function

about_project()




# ==========================
# TITLE
# ==========================

st.title("🎬 Movie Recommendation System")


st.markdown(
"""
<p class="subtitle">
AI Powered Content Based Movie Recommendation Engine
</p>
""",
unsafe_allow_html=True
)




# ==========================
# LOAD FILES
# ==========================

movies = pickle.load(
    open("movie_list.pkl","rb")
)


similarity = pickle.load(
    open("similarity.pkl","rb")
)




# ==========================
# TMDB API
# ==========================

API_KEY = "01f5cb8bc241bdecc853bf1cca22e22f"


IMAGE_URL = "https://image.tmdb.org/t/p/w500"





# ==========================
# FETCH POSTER
# ==========================

@st.cache_data
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        data = response.json()


        if "poster_path" in data and data["poster_path"]:

            return IMAGE_URL + data["poster_path"]


        return "https://placehold.co/500x750?text=No+Poster"


    except Exception as e:

        print(e)

        return "https://placehold.co/500x750?text=Error"
# def fetch_poster(movie_id):


#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"


#     try:

#         response = requests.get(
#             url,
#             timeout=10,
#             headers={
#                 "User-Agent":"Mozilla/5.0"
#             }
#         )


#         if response.status_code != 200:

#             return "https://placehold.co/500x750?text=No+Poster"



#         data = response.json()


#         poster_path = data.get("poster_path")


#         if poster_path:

#             return IMAGE_URL + poster_path



#         return "https://placehold.co/500x750?text=No+Poster"



#     except requests.exceptions.RequestException:

#         return "https://placehold.co/500x750?text=Error"






# # ==========================
# # RECOMMEND FUNCTION
# # ==========================

def recommend(movie):


    movie_index = movies[
        movies["title"] == movie
    ].index[0]



    distances = similarity[movie_index]



    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]



    recommended_movies = []

    recommended_posters = []



    for i in movies_list:


        movie_id = int(
            movies.iloc[i[0]].movie_id
        )


        title = movies.iloc[i[0]].title



        recommended_movies.append(title)



        recommended_posters.append(
            fetch_poster(movie_id)
        )



    return recommended_movies, recommended_posters





# ==========================
# MAIN UI
# ==========================


selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movies["title"].values
)




if st.button("🚀 Recommend Movies"):


    names, posters = recommend(
        selected_movie
    )



    st.subheader("🔥 Recommended Movies")



    cols = st.columns(5)



    for col, name, poster in zip(
        cols,
        names,
        posters
    ):


        with col:


            st.markdown(
            """
            <div class="movie-card">
            """,
            unsafe_allow_html=True
            )


            st.image(
                poster,
                use_container_width=True
            )


            st.markdown(
            f"""
            <p class="movie-title">
            {name}
            </p>
            """,
            unsafe_allow_html=True
            )


            st.markdown(
            "</div>",
            unsafe_allow_html=True
            )