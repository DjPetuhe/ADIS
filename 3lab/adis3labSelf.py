import matplotlib.pyplot as pyp
import pandas as p

#-----ЗАВДАННЯ ДЛЯ САМОПЕРЕВІРКИ-----

# Зчитування даних із .csv-файлу по заданому шляху
def read_dataset(path):
    return p.read_csv(path, sep=';', encoding='cp1252')

#Дослідження файлу
def getInfo(data):
    data.info()

# Виводимо перші n рядків
def print_first_n_rows(data, n):
    print(f'\nFirst{n} rows:')
    print(data.head(n))

# Виводимо останні n рядків
def print_last_n_rows(data, n):
    print(f'\nLast{n} rows:')
    print(data.tail(n))

# Видалення стовпчику "column"
def remove_column(data, column):
    return data.drop(column, axis = 1)

# Додавання нового стовпчику
def remove_column(data, column):
    return data.drop(column, axis = 1)

# Конвертація стовпчика column у float.
def convert_column_to_float(data, column):
    data[column] = data[column] .str.replace(',', '.').astype(float)

# Додавання нового стовпчику
def add_column(data, column, condition):
    data[column] = condition

# Заміна пропущенних значень нулями.
def replace_blank_with_zeros(dataset):
    return dataset.replace(' ', 0)

# Побудова діаграми розмаху для GDP per capita.
def gdp_per_capita_boxplot(data):
    pyp.figure()
    pyp.title('Діаграма розмаху для GDP per capita')
    pyp.boxplot(data['GDP per capita'])

# Побудова графіку залежності High-technology exports від GDP.
def plot_tech_exports_from_gdp_dependency(data):
    pyp.figure()
    pyp.title('Залежність High-technology exports від GDP per capita')
    pyp.xlabel('GDP per capita')
    pyp.ylabel('High-technology exports')
    pyp.plot(
        data['GDP per capita'],
        data['High-technology exports'],
        '*'
    )

# Завдання для самоперевірки
def main():
    dFrame = read_dataset("Data1.csv")
    dFrame.info()
    print_first_n_rows(dFrame, 5)
    print_last_n_rows(dFrame, 6)
    dFrame = remove_column(dFrame, 'ISO')
    convert_column_to_float(dFrame, 'Population')
    add_column(dFrame, 'Total GDP', dFrame['Population'] * dFrame['GDP per capita'])
    dFrame = replace_blank_with_zeros(dFrame)
    print(dFrame.describe())
    gdp_per_capita_boxplot(dFrame)
    convert_column_to_float(dFrame, 'High-technology exports')
    plot_tech_exports_from_gdp_dependency(dFrame)
    pyp.show()

if __name__ == '__main__':
    main()