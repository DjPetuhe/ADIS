from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cluster import KMeans
from kneed import KneeLocator

import matplotlib.pyplot as pyp
import plotly.express as px
import pandas as p
import numpy as n

#--------ОСНОВНЕ ЗАВДАННЯ----------

# Завантаження даних
def read_dataset(path, separ, dec, en):
    return p.read_csv(path, sep = separ, decimal = dec, encoding = en)

#Зміна стовпчиків на тип даних строки
def set_columns_type_str(dFrame, columns):
    for column in columns:
        dFrame[column] = dFrame[column].astype(str)

#Видалення стовпчиків
def drop_columns(dFrame, columns):
    for column in columns:
        dFrame = dFrame.drop(column, axis = 1)
    return dFrame

#Перевірка на пусті значення
def check_emptyness(dFrame):
    print("Columns with empty values (percentage):")
    percents = []
    for column in dFrame.columns:
        percents.append((round(dFrame[column].isnull().sum() / len(dFrame[column])* 100, 2), dFrame.columns.get_loc(column)))
    percents.sort(key = lambda tup: tup[0], reverse = True)
    nothing = True
    for percent in percents:
        if (percent[0] > 0):
            print(f"{dFrame.columns[percent[1]]}: {percent[0]}%")
            nothing = False
    if (nothing): print("There is any empty values!")

#Заповнення пустих значень стовпчика модою
def fill_mode(dFrame, columns):
    for column in columns:
        dFrame[column] = dFrame[column].fillna(dFrame[column].mode()[0])
    return dFrame

#Розділ даних на тестові та тренувлаьні
def split_data(x, y):
    return train_test_split(x, y, test_size=0.3)

#Побудова моделей пов'язаних с деревами :)
def build_tree_method(type, x_train, y_train, depth):
    tree = type(max_depth = depth)
    tree.fit(x_train, y_train)
    return tree

#Побудова моделей пов'язаних с бустінгом :)
def build_boosting_method(type, x_train, y_train, l_rate):
    boost = type(learning_rate = l_rate)
    boost.fit(x_train, y_train)
    return boost

#Отримання оцінок моделей
def get_scores(method, x_train, y_train, x_test, y_test):
    cv_score = cross_val_score(method, x_train, y_train, cv = 5)
    score = method.score(x_test, y_test)
    return cv_score, score

#Виведення результатів
def print_res(method, cvs, s):
    print(f"{method} method:")
    print("Cross validation score: ", cvs.mean())
    print("Score: ", s)

#Виведення найкращого метода
def print_best_method(methods, scores):
    min_i = n.argmax(scores)
    print("Best model is:")
    print(f"{methods[min_i]} method with {scores[min_i]} score")

def main():
    dFrame = read_dataset("titanic.csv", ",", ".", "cp1252")
    dFrame.info()
    dFrame.head(5)
    set_columns_type_str(dFrame, ["Pclass"])
    dFrame = drop_columns(dFrame, ["PassengerId", "Name", "Ticket"])
    dFrame.info()
    dFrame.head(5)
    check_emptyness(dFrame)
    dFrame = drop_columns(dFrame, ["Cabin"])
    dFrame = fill_mode(dFrame, ["Age", "Embarked"])
    check_emptyness(dFrame)
    dFrame = p.get_dummies(dFrame)
    x_train, x_test, y_train, y_test = split_data(dFrame.drop(columns = "Survived"), dFrame["Survived"])
    methods = ["Decision tree", "Random forest", "Extra trees", "Ada boost", "Gradient boosting"]
    #Decision tree
    dt = build_tree_method(DecisionTreeClassifier, x_train, y_train, 5)
    dt_cvs, dt_s = get_scores(dt, x_train, y_train, x_test, y_test)
    print_res(methods[0], dt_cvs, dt_s)
    #Random forest
    rf = build_tree_method(RandomForestClassifier, x_train, y_train, 5)
    rf_cvs, rf_s = get_scores(rf, x_train, y_train, x_test, y_test)
    print_res(methods[1], rf_cvs, rf_s)
    #Extra trees
    et = build_tree_method(ExtraTreesClassifier, x_train, y_train, 5)
    et_cvs, et_s = get_scores(et, x_train, y_train, x_test, y_test)
    print_res(methods[2], et_cvs, et_s)
    #Ada boost
    ab = build_boosting_method(AdaBoostClassifier, x_train, y_train, 0.5)
    ab_cvs, ab_s = get_scores(ab, x_train, y_train, x_test, y_test)
    print_res(methods[3], ab_cvs, ab_s)
    #Gradient boosting
    gb = build_boosting_method(GradientBoostingClassifier, x_train, y_train, 0.5)
    gb_cvs, gb_s = get_scores(gb, x_train, y_train, x_test, y_test)
    print_res(methods[4], ab_cvs, ab_s)
    print_best_method(methods, [dt_s, rf_s, et_s, ab_s, gb_s])

#--------ДОДАТКОВЕ ЗАВДАННЯ----------

#Видалення помилок з набору даних
def remove_errors(dFrame):
    dFrame.rename(columns={'Populatiion' : 'Population'}, inplace = True)
    index = dFrame.index
    dFrame.iloc[index[dFrame['Country Name'] == 'Eritrea'], \
                dFrame.columns.get_loc('Population')] = 3662244
    remove_negatives(dFrame, 'GDP per capita')
    remove_negatives(dFrame, 'Area')
    fill_empty_fields(dFrame, 'GDP per capita')
    fill_empty_fields(dFrame, 'CO2 emission')

#Прибирання негативних значень
def remove_negatives(dFrame, column):
    dFrame[column] = dFrame[column].abs()

#Заповненя пустих комірок середнім значенням по стовпчику
def fill_empty_fields(dFrame, column):
    dFrame[column].fillna(dFrame[column].mean(), inplace = True)

#Додавання стовпичка
def add_column(dFrame, column, condition):
    dFrame[column] = condition

#Знаходження суми квадратних помилок
def get_se_sum(f, arguments):
    se_sum = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **arguments)
        kmeans.fit(f)
        se_sum.append(kmeans.inertia_)
    return se_sum

#Побудова графіку для локтя
def elbow_plot(se_sum):
    pyp.figure(figsize=(10, 7))
    pyp.plot(range(1, 11), se_sum)
    pyp.xticks(range(1, 11))
    pyp.ylabel('Sum of the squared Euclidean distances')
    pyp.xlabel('Number of Clusters')
    pyp.grid(linestyle='-')
    pyp.show()

#Знаходження точки локтя
def knee_point(se_sum):
    knee = KneeLocator(range(1, 11), se_sum, curve="convex", direction="decreasing")
    return knee.elbow

#Візуалізуємо кластери
def cluster_plot(dFrame, x_c, y_c, hv_d, f):
    km = KMeans(init = 'random', n_clusters = 3)
    km.fit(f)
    fig = px.scatter(dFrame, 
                     x = x_c,
                     y = y_c,
                     color = km.labels_,
                     hover_data = hv_d)
    fig.update(layout_coloraxis_showscale=False)
    fig.show()

#Виведення гістограм циклом
def plot_bars(dFrame, columns):
    fig, axes = pyp.subplots(2, 3, figsize=(20,15))
    for i in range(2):
        for j in range(3):
            axes[i][j].set_title(columns[(i*j) + j])
            axes[i][j].hist(dFrame[columns[(i*j) + j]])
    fig.delaxes(axes[1][2])
    pyp.show()

#Виведення гістограми по регіонам
def bar_columns(dFrame, column):
    dFrame[column].value_counts().plot(kind = "bar", figsize = (15, 10))
    pyp.show()

#Функція, що перевіряє лінійну залежність
def LinearDependence(first, second):
    return abs(n.corrcoef(first, second)[0,1]) > 0.8

def main2():
    dFrame = read_dataset("Data2.csv", ";", ",", "windows-1252")
    dFrame.info()
    dFrame.head(5)
    remove_errors(dFrame)
    dFrame.info()
    dFrame.head(5)
    add_column(dFrame, "Population density", dFrame["Population"] / dFrame["Area"])
    dFrame.info()
    dFrame.head(5)
    f = dFrame[['GDP per capita','Population density']]
    arguments = {'init': 'random', 'n_init': 10, 'max_iter': 300,}
    se_sum = get_se_sum(f, arguments)
    elbow_plot(se_sum)
    print(f"Elbow point: {knee_point(se_sum)}")
    cluster_plot(dFrame, "GDP per capita", "Population density", ["Country Name","Region"], f)
    plot_bars(dFrame, dFrame.columns[2:])
    bar_columns(dFrame, "Region")
    x = n.random.randint(0, 100, 100)
    y =  5 * x + n.random.normal(0, 10, 100)
    y2 = n.random.normal(0, 10, 100)
    print(LinearDependence(x, y))
    print(LinearDependence(x, y2))

if __name__ == '__main__':
    main()
    main2()