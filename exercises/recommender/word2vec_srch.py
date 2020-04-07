from gensim.models import Word2Vec
import pandas as pd
import numpy as np


def Sort(tup):
    return sorted(tup, key=lambda x: float(x[1]), reverse=True)


def similar_tuple(exercise_name, word, model):
    return (word, model.wv.similarity(exercise_name, word))


def show_similarity_for_each_exercise(word, exercise_list, vector_val, model):
    for item in exercise_list:
        vector_val.append(similar_tuple(word, item, model))
    return vector_val


def yield_vector_list(exercises_qs, search_keyword):
    model = Word2Vec.load("./exercises/recommender/_searchTool/word2vec/my_first_model")

    # print(exercises_qs)
    # exercises_qs
    # exercise_list_without_space = [x.replace(" ", "") for x in exercises_qs]

    # print(search_keyword)
    # print(exercise_list_without_space)
    df = pd.read_csv(
        "./exercises/recommender/_searchTool/word2vec/word2vec_wrangling.csv"
    )
    exercise_list_without_space = df["exercise_name"].to_list()

    vector_val = []

    vector_list = show_similarity_for_each_exercise(
        search_keyword, exercise_list_without_space, vector_val, model
    )
    print(Sort(vector_list))
