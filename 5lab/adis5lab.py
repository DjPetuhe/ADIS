from gettext import dgettext
import matplotlib.pyplot as pyp
from scipy import rand
import scipy.stats as st
import pandas as p
import numpy as n
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#--------ОСНОВНЕ ЗАВДАННЯ----------

# Завантаження даних
def read_dataset(path, separ, en):
    return p.read_csv(path, sep = separ, encoding = en)

# 1. Дослідити дані, підготувати їх для побудови регресійної моделі
def kolm_smirn_check(dFrame, column):
    ks_statistic, p_value = st.kstest(dFrame[column], 'norm')
    if p_value > 0.05: return True
    return False

def pearson_check(dFrame, column):
    statistic, p_value = st.normaltest(dFrame[column])
    if p_value > 0.05: return True
    return False

def data_check(dFrame):
    dFrame.info()
    print(f"Is there any nan: {dFrame.isnull().values.any()}")
    print(f"Is there any negative: {(dFrame < 0).values.any()}")
    print("#1 test - Kolmagorov-Smirnov test,\n#2 test - Pearson test\n")
    for c in dFrame.columns:
        print('{0:<23}'.format(c + ":"),f"#1 test - {kolm_smirn_check(dFrame, c)}, #2 test - {pearson_check(dFrame, c)};")
    dFrame.corr()

# 2. Розділити дані на навчальну та тестову вибірки
def split_data(dFrame):
    first = dFrame.iloc[:, :11]
    second = dFrame['quality']
    return train_test_split(first, second, test_size=0.33, random_state = 10)

# 3. Побудувати декілька регресійних моделей для прогнозу якості вина
def make_r_models(f_train, s_train):
    r_models = [LinearRegression().fit(f_train, s_train)]
    for i in range(2, 5):
        r_models.append(make_pipeline(PolynomialFeatures(degree=i) , LinearRegression()))
        r_models[i - 1].fit(f_train, s_train)
    return r_models

# 4. Використовуючи тестову вибірку, з'ясувати яка з моделей краща
def find_best(r_models, f_test, s_test):
    mse = []
    r_2 = []
    for r_model in r_models:
        predict = r_model.predict(f_test)
        mse.append(mean_squared_error(s_test, predict))
        r_2.append(r2_score(s_test, predict))
    rse_s = []
    r_2_s = []
    for r_model in r_models:
        rse_s.append(((n.sum(n.square(s_test - r_model.predict(f_test))))/(len(s_test) - 2)) ** 0.5)
        r_2_s.append(r2_score(s_test, r_model.predict(f_test)))
    print('Best rse index: ', n.argmin(rse_s) + 1)
    print('Best r_2 index: ', n.argmax(r_2_s) + 1)

def main():
    dFrame = read_dataset("winequality-red.csv", ',', 'cp1252')
    data_check(dFrame)
    f_train, f_test, s_train, s_test = split_data(dFrame)
    r_modles = make_r_models(f_train, s_train)
    find_best(r_modles, f_test, s_test)

#--------ДОДАТКОВЕ ЗАВДАННЯ----------

def set_column_type_float(dFrame, column):
    dFrame[column] = dFrame[column].str.replace(',', '.').astype(float)

def data_fix(dFrame):
    dFrame = read_dataset("Data4.csv", ';', 'cp1251')
    dFrame.columns.values[0] = "Country"
    for i in range(3,7):
        set_column_type_float(dFrame, dFrame.columns[i])
    dFrame.info()
    dFrame.head(5)
    return dFrame

# 1. Дослідити дані, сказати чи є мультиколінеарність, побудувати діаграми розсіювання
def data_check_add(dFrame):
    dFrame.corr()
    p.plotting.scatter_matrix(dFrame, figsize=(15, 15))
    pyp.show()

# 2. Побудувати декілька регресійних моделей (використати лінійну регресію та поліноміальну регресію обраного вами виду)
def make_r_models_add(dFrame, par, by):
    Y = dFrame[by]
    lin = []
    pol = []
    for i in range(len(par)):
        pol.append(make_pipeline(PolynomialFeatures(degree = 2), LinearRegression()))
        if i < 3: 
            lin.append(LinearRegression().fit(dFrame[par[i]].to_numpy().reshape(-1, 1), Y))
            pol[i].fit(dFrame[par[i]].to_numpy().reshape(-1, 1), Y)
        else :
            lin.append(LinearRegression().fit(dFrame[par[i]], Y))
            pol[i].fit(dFrame[par[i]], Y)
    return lin, pol

# 3. Використовуючи тестову вибірку з файлу Data4t.csv, з'ясувати яка з моделей краща
def predict_by(dFrame_t, par, prediction, s):
    for i in range(len(par)):
        if i < 3:
            prediction.append(s[i].predict(dFrame_t[par[i]].to_numpy().reshape(-1, 1)))
        else:
            prediction.append(s[i].predict(dFrame_t[par[i]]))
    return prediction

def find_best_add(dFrame_t, par, lin, pol):
    prediction = []
    prediction = predict_by(dFrame_t, par, prediction, lin)
    prediction = predict_by(dFrame_t, par, prediction, pol)
    min_i = n.sum((n.array(prediction)- dFrame_t['Cql'].to_numpy())**2,axis = 1).argmin()
    print("Best model is:")
    if (min_i < 6):
        print(f"linear model by {par[min_i]} params")
    else:
        print(f"polynomial model by {par[min_i - 7]} params")

def main2():
    dFrame = read_dataset("Data4.csv", ";", "cp1251")
    dFrame = data_fix(dFrame)
    data_check_add(dFrame)
    par = ["Ie", "Is", "Iec", ["Ie", "Is"], ["Ie", "Iec"], ["Is", "Iec"], ["Ie", "Is", "Iec"]]
    lin, pol = make_r_models_add(dFrame, par, "Cql")
    dFrame_t = read_dataset("Data4t.csv", ";", "cp1251")
    dFrame_t = data_fix(dFrame)
    find_best_add(dFrame_t, par, lin, pol)

if __name__ == '__main__':
    main()
    main2()