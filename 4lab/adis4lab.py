import matplotlib.pyplot as pyp
import pandas as p
import math
import scipy.stats as st

#--------ОСНОВНЕ ЗАВДАННЯ----------

# 1. Записати дані у data  frame
def read_dataset(path):
    return p.read_csv(path, sep=";", encoding='cp1252')

# 2. Дослідити структуру
def getInfo(dFrame):
    dFrame.info()

# 3. Виправити помилки в даних + середні значення
def remove_errors(dFrame):
    dFrame.rename(columns={'Populatiion' : 'Population'}, inplace = True)
    set_column_type_float(dFrame,'GDP per capita')
    set_column_type_float(dFrame,'CO2 emission')
    set_column_type_float(dFrame,'Area')
    change_values(dFrame)

def change_values(dFrame):
    index = dFrame.index
    dFrame.iloc[index[dFrame['Country Name'] == 'Eritrea'], dFrame.columns.get_loc('Population')] = 3662244
    remove_negatives(dFrame, 'GDP per capita')
    remove_negatives(dFrame, 'Area')
    fill_empty_fields(dFrame, 'GDP per capita')
    fill_empty_fields(dFrame, 'CO2 emission')

def remove_negatives(dFrame, column):
    dFrame[column] = dFrame[column].abs()

def fill_empty_fields(dFrame, column):
    dFrame[column].fillna(dFrame[column].mean(), inplace = True)

def set_column_type_float(dFrame, column):
    dFrame[column] = dFrame[column].str.replace(',', '.').astype(float)

# 4. Перевірка стовпців на нормальність розподілу
def check_normal_distribution(dFrame):
    print('\nNormal destribution by Kolmogorov–Smirnov test:')
    print('CO2 emission:', kolm_smirn_check(dFrame, "CO2 emission"))
    print('{0:<13}'.format('Area:'), kolm_smirn_check(dFrame, 'Area'))
    print('{0:<13}'.format('Population:'), kolm_smirn_check(dFrame, "Population"))
    print('\nNormal destribution by D\'Agostino\'s K-squared test:')
    print('CO2 emission:', pearson_check(dFrame, "CO2 emission"))
    print('{0:<13}'.format('Area:'), pearson_check(dFrame, 'Area'))
    print('{0:<13}'.format('Population:'), pearson_check(dFrame, "Population"))

def kolm_smirn_check(dFrame, column):
    ks_statistic, p_value = st.kstest(dFrame[column], 'norm')
    if p_value > 0.05: return True
    return False

def pearson_check(dFrame, column):
    statistic, p_value = st.normaltest(dFrame[column])
    if p_value > 0.05: return True
    return False

# 5. Перевірити середні та медіани на значимість
def signif_check(dFrame):
    print('\nThe null hepotesis for:')
    print('{0:<16}'.format('Area is:'), hypothesis_testing_two_tailed(dFrame, 'Area'))
    print('{0:<16}'.format('Population is:'), hypothesis_testing_two_tailed(dFrame, 'Population'))
    print('CO2 emission is:', hypothesis_testing_two_tailed(dFrame, 'CO2 emission'))

def hypothesis_testing_two_tailed(dFrame, column):
    s_mean = dFrame[column].mean()
    s_dev = dFrame[column].std()
    med_null = dFrame[column].median()
    size = len(dFrame[column])
    test_statistic = ((s_mean - med_null)/(s_dev/math.sqrt(size)))
    p_value = 2*(1 - st.t.cdf(test_statistic, size - 1))
    if p_value < 0.05: return False
    return True

# 6. Вказати, в якому регіоні розподіл викидів СО2 найбільш близький до нормального
def most_normal_destributed_region (dFrame):
    regs = p.unique(dFrame['Region'])
    most_normal = ""
    best_p = 0.0
    for reg in regs:
        regCO2 = (dFrame.loc[dFrame['Region'] == reg])['CO2 emission'].values
        if len(regCO2) > 8:
            stat, p_value = st.normaltest(regCO2)
            if p_value > best_p:
                most_normal = reg
                best_p = p_value
    return most_normal

#7. Побудувати кругову діаграму населення по регіонам
def population_diagram(dFrame, by, column):
    dFrame.groupby(by)[column].sum().plot(kind='pie', figsize=(10,10), autopct='%1.2f%%')
    pyp.ylabel(' ')
    pyp.show()

def main():
    dFrame= read_dataset('Data2.csv')
    getInfo(dFrame)
    remove_errors(dFrame)
    check_normal_distribution(dFrame)
    signif_check(dFrame)
    print(f'\nDestribution is closest to normal in {most_normal_destributed_region(dFrame)} region')
    population_diagram(dFrame, 'Region', 'Population')


if __name__ == '__main__':
    main()