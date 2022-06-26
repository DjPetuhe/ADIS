from sklearn.feature_extraction.text import TfidfVectorizer
import collections
import pandas as p
import numpy as n
import nltk as nl
import pymorphy2
import re
import csv

def read_dataset(path, separ, en):
    return p.read_csv(path, sep = separ, encoding = en)

def drop_columns(dFrame, columns):
    for column in columns:
        dFrame = dFrame.drop(column, axis = 1)
    return dFrame

# 2) виконати токенізацію текстових елементів;
def to_tokens(dFrame):
    for i in range(dFrame.shape[0]):
        for j in range(dFrame.shape[1]):
            temp_text = dFrame.iloc[i, j]
            dFrame.iloc[i, j] = re.sub("[^А-Яа-яЁёЇїІіЄєҐґ'\-\s]", "", temp_text).split()

def csv_to_list(path, n_l, enc):
    with open(path, newline = n_l, encoding = enc) as s_w:
        return [element for sublist in list(csv.reader(s_w)) for element in sublist]

def get_stop_words(path, n_l, enc):
    stop_words = csv_to_list(path, n_l, enc)
    stop_words.remove("stopword")
    stop_words.extend(["тис", "грн", "вул", "cек", "хв", "обл", "кв", "пл", "напр", "гл", "о", "зам", "із"])
    return stop_words

# 1) провести очистку текстових даних від стоп-слів/тегів/розмітки;
def fix_porblems(dFrame, stop_words):
    for i in range(dFrame.shape[0]):
        for j in range(dFrame.shape[1]):
            for k in range(len(dFrame.iloc[i,j])):
                dFrame.iloc[i,j][k] = dFrame.iloc[i,j][k].lower()
            dFrame.iloc[i,j] = [x for x in dFrame.iloc[i,j] if (re.fullmatch("(\w+(\-|\'|\`)\w+|\w+)", x) and len(x) > 2)]
            dFrame.iloc[i,j] = [x for x in dFrame.iloc[i,j] if not (x in stop_words)]

#3) провести лематизацію текстових елементів;
def lematize(dFrame):
    uk_l = pymorphy2.MorphAnalyzer(lang='uk')
    for i in range(dFrame.shape[0]):
        for j in range(dFrame.shape[1]):
            for k in range(len(dFrame.iloc[i,j])):
                dFrame.iloc[i,j][k] = uk_l.parse(dFrame.iloc[i,j][k])[0].normal_form

# 4) порахувати метрику TF-IDF для 10 слів, що найчастіше зустрічаються в корпусі;
def get_top_words(dFrame):
    bodies = []
    for i in range(dFrame.shape[0]):
        bodies += dFrame.iloc[i]["Body"]
    return dict(collections.Counter(bodies).most_common(10))

def identity_tokenizer(text):
    return text

def df_tfidf(dFrame, topWords):
    tokenized_list = []
    for i in range(dFrame.shape[0]):
        tokenized_list.append(dFrame.iloc[i]["Body"])
    tfidf = TfidfVectorizer(tokenizer = identity_tokenizer, lowercase = False)
    vectors = tfidf.fit_transform(tokenized_list)
    feature_names = tfidf.get_feature_names_out()
    denselist = vectors.todense().tolist()
    d_l, f_n = top_n_tfidf(feature_names, denselist, topWords)
    return p.DataFrame(n.array(d_l).T.tolist(), columns = f_n)

def top_n_tfidf(feature_names, denselist, topWords):
    f_n = []
    d_l = []
    feature_names = n.array(feature_names)
    denselist = n.array(denselist)
    for i in range(len(feature_names)):
        is_there = False
        for e2 in topWords:
            if feature_names[i] == e2:
                is_there = True
        if is_there:
            f_n.append(feature_names[i])
            temp = []
            for j in range(len(denselist[:,i])):
                temp.append(denselist[j][i])
            d_l.append(temp)
    return d_l, f_n

# 5) створити та наповнити Bag of Word для всіх нормалізованих слів.
def calculateBOW(wordset, l_doc):
    tf_diz = dict.fromkeys(wordset, 0)
    for word in l_doc:
        tf_diz[word] = l_doc.count(word)
    return tf_diz

def get_wordset(dFrame):
    wordset = None
    for i in range(dFrame.shape[0]):
        if (i == 1):
            wordset = n.union1d(dFrame.iloc[0]["Body"], dFrame.iloc[1]["Body"])
        elif (i > 1):
            wordset = n.union1d(wordset, dFrame.iloc[i]["Body"])
    return wordset

def dataFrame_bowl(dFrame):
    bow = []
    wordset = get_wordset(dFrame)
    for i in range(dFrame.shape[0]):
        bow.append(calculateBOW(wordset, dFrame.iloc[i]["Body"]))
    return p.DataFrame(bow)

def main():
    dFrame = read_dataset("ukr_text.csv", ",", "utf-8")
    dFrame.info()
    dFrame.head(5)
    dFrame = drop_columns(dFrame, ["Id"])
    to_tokens(dFrame)
    dFrame.info()
    dFrame.head(5)
    stop_words = get_stop_words("stop_words_ua.csv", "", "utf-8")
    print(stop_words)
    fix_porblems(dFrame, stop_words)
    dFrame.info()
    dFrame.head(5)
    lematize(dFrame)
    dFrame.info()
    dFrame.head(5)
    top_words_dict = get_top_words(dFrame)
    print(top_words_dict)
    top_words = list(top_words_dict.keys())
    df = df_tfidf(dFrame, top_words)
    print(df)
    df_bow = dataFrame_bowl(dFrame)
    df_bow.head(10)
    df_useful = df_bow[top_words]
    df_useful.head(15)

if __name__ == "__main__":
    main()