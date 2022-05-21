import matplotlib.pyplot as pyp
import pandas as p

#-----ОСНОВНІ ТА ДОДАТКОВІ ЗАВДАННЯ-----

# 1. Записати дані у data  frame
def openDF(path):
    return p.read_csv(path, sep=";", encoding='cp1252')

# 2. Дослідити структуру
def getInfo(data):
    data.info()

# 3. Виправити помилки в даних + середні значення
def remove_errors(dataSet):
    dataSet.rename(columns={'Populatiion' : 'Population'}, inplace = True)
    set_column_type_float(dataSet,'GDP per capita')
    set_column_type_float(dataSet,'CO2 emission')
    set_column_type_float(dataSet,'Area')
    change_values(dataSet)

def change_values(dataSet):
    index = dataSet.index
    dataSet.iloc[index[dataSet['Country Name'] == 'Eritrea'], dataSet.columns.get_loc('Population')] = 3662244
    remove_negatives(dataSet, 'GDP per capita')
    remove_negatives(dataSet, 'Area')
    fill_empty_fields(dataSet, 'GDP per capita')
    fill_empty_fields(dataSet, 'CO2 emission')

def remove_negatives(dataSet, column):
    dataSet[column] = dataSet[column].abs()

def fill_empty_fields(dataSet, column):
    dataSet[column].fillna(dataSet[column].mean(), inplace = True)

def set_column_type_float(dataSet, column):
    dataSet[column] = dataSet[column].str.replace(',', '.').astype(float)

# 4. Побудування діаграм розмаху та гістограм
def build_hist_and_boxplot(dataSet):
    do_boxplot(dataSet,'Діаграма розмаху для CO2 emmision', 'CO2 emission')
    do_boxplot(dataSet,'Діаграма розмаху для Population', 'Population')
    do_boxplot(dataSet,'Діаграма розмаху для Area', 'Area')
    pyp.show()
    do_hist(dataSet, 'Area')
    do_hist(dataSet, 'CO2 emission')
    do_hist(dataSet, 'Population')
    do_hist(dataSet, 'GDP per capita')

def do_boxplot(data, title, column):
    pyp.figure()
    pyp.title(title)
    pyp.boxplot(data[column])

def do_hist(dataSet, column):
    pyp.hist(dataSet[column])
    pyp.show()

# 5. Додати стовпчик із щільністю населення
def add_column(data, column, condition):
    data[column] = condition

# 6. Яка країна має найбільший ВВП на людину (GDP per capita)? Яка має найменшу площу?
def best_dgp_worst_area(dataSet):
    print('\nНайбільший ВВП по ППС у країни:')
    print(dataSet['Country Name'][dataSet['GDP per capita'].idxmax()])
    print('\nНайменьша площа у країни:')
    print(dataSet['Country Name'][dataSet['Area'].idxmin()])

# 7. В якому регіоні середня площа країни найбільша?
def best_area_region(dataSet):
    print('\nРегіон, в якому середня площа країн найбільша:')
    print(dataSet.groupby(['Region']).mean()['Area'].idxmax())

# 8. З яким населенням найчастіше зустрічаються країни у світі? У Європі?
def most_population_world_europe(dataSet):
    print('\nКраїна з чиїм найчастіше зустрічаються найчастіше у світі:')
    print(dataSet['Country Name'][dataSet['Population'].idxmax()])
    print('\nКраїна з чиїм найчастіше зустрічаються найчастіше у Європі:')
    dataSetEurope = dataSet.loc[dataSet['Region'] == "Europe & Central Asia"]
    print(dataSetEurope['Country Name'][dataSetEurope['Population'].idxmax()])

# 9. Чи співпадає в якомусь регіоні середнє та медіана ВВП?
def median_and_mean_gdp_region(dataSet):
    means = dataSet.groupby(['Region']).mean()['GDP per capita']
    medians = dataSet.groupby(['Region']).median()['GDP per capita']
    print('Чи співпадає в якомусь регіоні середнє та медіанне ВВП?:')
    print(p.merge(means, medians).any(axis=None))


# 10. Вивести топ 5 країн та 5 останніх країн по ВВП та кількості СО2 на душу населення.
def top_5_gdp_co2_per_capita(dataSet):
    print('\nТоп 5 найкращіх країн по ВВП по ППС:')
    print(dataSet.sort_values(by=['GDP per capita'], ascending = False).head(5)['Country Name'])
    print('\nТоп 5 найгірших країн по ВВП по ППС:')
    print(dataSet.sort_values(by=['GDP per capita']).head(5)['Country Name'])
    add_column(dataSet, 'CO2 emission per capita', dataSet['CO2 emission'] / dataSet['Population'])
    print('\nТоп 5 найкращіх країн по кількості CO2 на душу населення:')
    print(dataSet.sort_values(by=['CO2 emission per capita'], ascending = False).head(5)['Country Name'])
    print('\nТоп 5 найгірших країн по кількості CO2 на душу населення:')
    print(dataSet.sort_values(by=['CO2 emission per capita']).head(5)['Country Name'])


def main():
    dFrame= openDF('Data2.csv')
    getInfo(dFrame)
    remove_errors(dFrame)
    build_hist_and_boxplot(dFrame)
    add_column(dFrame, 'Population density', dFrame['Population'] / dFrame['Area'])
    best_dgp_worst_area(dFrame)
    best_area_region(dFrame)
    most_population_world_europe(dFrame)
    median_and_mean_gdp_region(dFrame)
    top_5_gdp_co2_per_capita(dFrame)



if __name__ == '__main__':
    main()