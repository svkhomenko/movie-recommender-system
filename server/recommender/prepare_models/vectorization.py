import numpy as np
import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sqlmodel import Session, select
import models


def fetch_movies_data_for_vectorization(session: Session):
    statement = select(models.Movie)
    movies = session.exec(statement).all()

    movie_data = []

    for movie in movies:
        genres_list = [genre.name for genre in movie.genres]

        crew_list = []
        for mc in movie.movie_crew:
            crew_list.append(mc.crew.full_name)

        movie_data.append(
            {
                "id": movie.id,
                "title": movie.title,
                "overview": movie.overview,
                "keywords": movie.keywords,
                "release_date": movie.release_date,
                "vote_average": movie.vote_average,
                "genres": genres_list,
                "crew": crew_list,
            }
        )

    return pd.DataFrame(movie_data)


def convert_to_proper_types(movies_df):
    if movies_df["release_date"].dtype == "object":
        movies_df["release_date"] = pd.to_datetime(
            movies_df["release_date"], errors="coerce"
        ).dt.date

    years = movies_df["release_date"].apply(lambda x: x.year)
    years_conditions = [years < 1980, (years >= 1980) & (years < 2000), years >= 2000]
    years_choices = ["veryoldfilm", "oldfilm", "newfilm"]
    movies_df["age"] = np.select(years_conditions, years_choices, default="unknown")

    votes_average = movies_df["vote_average"]
    votes_conditions = [
        votes_average <= 4,
        (votes_average > 4) & (votes_average <= 7),
        votes_average > 7,
    ]
    votes_choices = ["badvote", "averagevote", "goodvote"]
    movies_df["review"] = np.select(votes_conditions, votes_choices, default="unknown")

    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    stop_words = nlp.Defaults.stop_words

    def preprocess_text_spacy(text):
        if isinstance(text, str):
            doc = nlp(text)
            processed_tokens = []
            for token in doc:
                if (
                    not token.is_punct
                    and not token.is_space
                    and token.lower_ not in stop_words
                ):
                    processed_tokens.append(token.lemma_)
            return " ".join(processed_tokens)
        return ""

    movies_df["overview"] = movies_df["overview"].apply(preprocess_text_spacy)
    movies_df["keywords"] = movies_df["keywords"].apply(preprocess_text_spacy)

    movies_df["tags_for_cv"] = movies_df["genres"] + movies_df["crew"]
    movies_df["tags_for_cv"] = movies_df["tags_for_cv"].apply(
        lambda x: [i.replace(" ", "") for i in x]
    )
    movies_df["tags_for_cv"] = movies_df["tags_for_cv"].apply(lambda x: " ".join(x))
    movies_df["tags_for_cv"] = movies_df["tags_for_cv"].apply(lambda x: x.lower())
    movies_df["tags_for_cv"] = (
        movies_df["tags_for_cv"] + " " + movies_df["age"] + " " + movies_df["review"]
    )

    movies_df["tags_for_doc2vec"] = movies_df["overview"] + " " + movies_df["keywords"]

    return movies_df


def vectorization(movies_df):
    tagged_documents_doc2vec = []
    for index, row in movies_df.iterrows():
        tagged_document = TaggedDocument(row["tags_for_doc2vec"], [str(index)])
        tagged_documents_doc2vec.append(tagged_document)

    movies_df["tags_for_doc2vec"] = tagged_documents_doc2vec

    doc2vec_model = Doc2Vec(
        tagged_documents_doc2vec,
        vector_size=300,
        window=5,
        min_count=5,
        epochs=20,
        dm=0,
        workers=4,
    )

    doc2vec_vectors = [doc2vec_model.dv[str(i)] for i in range(len(movies_df))]

    count_vectorizer = CountVectorizer(max_features=3000, binary=True)
    vector_cv = count_vectorizer.fit_transform(movies_df["tags_for_cv"])

    n_components_optimal = 800
    optimal_svd = TruncatedSVD(n_components=n_components_optimal, random_state=42)
    reduced_matrix = optimal_svd.fit_transform(vector_cv)

    combined_features = np.concatenate(
        (np.array(doc2vec_vectors), reduced_matrix), axis=1
    )

    normalized_combined_features = normalize(combined_features, axis=1)
    return (
        movies_df,
        normalized_combined_features,
        doc2vec_model,
        count_vectorizer,
        optimal_svd,
    )
