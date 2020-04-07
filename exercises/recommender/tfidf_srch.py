import pandas as pd
import numpy as np

# from konlpy.tag import Okt, Mecab
from konlpy.tag import Okt
from scipy import sparse
import pickle
import warnings


class KorTokenizer:

    """ Korean Tokenizer Description """

    def tokenizer(raw):

        # position arguments: 내가 뽑아내고 싶은 형태소들
        twitter_pos = ["Noun", "Alpha", "Verb", "Number", "Adverb"]
        mecab_pos = ["NNG", "NNP", "VV", "VA", "MAG"]
        pos = twitter_pos + mecab_pos

        # accessing saved stopwords
        stopwords_dataframe = pd.read_csv(
            "./exercises/recommender/_searchTool/stopwords_dataframe.csv"
        )
        stopwords = stopwords_dataframe["stopwords"]

        # mecab module
        """
        mecab = Mecab()
        mecab_list = [
            word
            for word, tag in mecab.pos(raw, flatten=True)
            if len(word) > 1 and tag in pos and word not in stopwords
        ]
        """

        # twitter module
        twitter = Okt()
        twitter_list = [
            word
            # normalize 그랰ㅋㅋ -> 그래ㅋㅋ  # stemming 바뀌나->바뀌다
            for word, tag in twitter.pos(raw, norm=True, stem=True)
            if len(word) > 1 and tag in pos and word not in stopwords
        ]

        # combine extracted noun and verb list without overlapping
        return set(twitter_list)


class CustomUnpickler(pickle.Unpickler):

    """ Returning custom tokenizer instead of default tokenizer when loading tfidf vectorizer with pickle """

    def find_class(self, module, name):
        if name == "tokenizer":
            return KorTokenizer.tokenizer
        return super().find_class(module, name)


class TFIDFSearch:

    """ TFIDF Search Definition """

    def tfidf_srch(search_phrase):
        # ignore warnings
        warnings.filterwarnings(action="ignore", category=UserWarning, module="sklearn")

        # load feature vector
        features = pd.read_csv("./exercises/recommender/_searchTool/tfidf/features.csv")
        features = features.values[0].tolist()

        # 검색 문장에서 feature를 뽑아냄. 단, 아직 띄어쓰기 모듈은 적용이 안 되어 있음
        srch = [t for t in KorTokenizer.tokenizer(search_phrase) if t in features]
        print(srch)

        # load matrix
        X = sparse.load_npz("./exercises/recommender/_searchTool/tfidf/yourmatrix.npz")
        # print(type(X))

        # load vectorizer
        vectorizer = CustomUnpickler(
            open("./exercises/recommender/_searchTool/tfidf/tfidfvectorizer.pkl", "rb")
        ).load()

        # dtm 에서 검색하고자 하는 feature만 뽑아낸다.
        srch_dtm = np.asarray(X.toarray())[
            :,
            [
                # vectorize.vocabulary_.get 는 특정 feature 가 dtm 에서 가지고 있는 index값을 리턴한다
                vectorizer.vocabulary_.get(i)
                for i in srch
            ],
        ]

        # print(len(srch_dtm))
        score = srch_dtm.sum(axis=1)

        #  exercises' instagram hashtag crawling result data (NOT DJANGO DATA)
        df = pd.read_csv(
            "./exercises/recommender/_searchTool/200311_djangoDB_matched_instaCrawled.csv"
        )
        recommended_exercises_web = []
        for i in score.argsort()[::-1]:
            if score[i] > 0.053:
                # see each exercise's matching score
                # print((df["exercise_name"].iloc[i], score[i]))

                # compare exercise name for instagram crawling and exercise name registered on web
                # recommend_exercise_insta = df["exercise_name"].iloc[i]
                # recommend_exercise_web = df["exercise_name_web"].iloc[i]
                # print(recommend_exercise_insta, recommend_exercise_web)

                # add on list
                exercise_name_web = df["exercise_name_web"].iloc[i]
                # print(type(exercise_name_web))
                # print(exercise_name_web)

                # remove nan from recommendation result
                if isinstance(exercise_name_web, float):
                    pass
                else:
                    recommended_exercises_web.append(exercise_name_web)

        # print(recommended_exercises_web)
        # give top 21 values only
        return recommended_exercises_web[:20]
