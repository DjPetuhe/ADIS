import matplotlib.pyplot as pyp
import matplotlib.image as im
import geopy.distance as d
import geopandas as gp
import pandas as p
import numpy as n
import math

#--------ДОДАТКОВЕ ЗАВДАННЯ----------

# 1. Завантажити карту України  Ukraine.jpg
def read_img(path):
    return im.imread(path)

def read_dataset(path):
    return (p.read_csv(path, encoding='cp1251', sep=';', decimal=',', header=1))

# 2. Розмістити бульбашки, що відповідають їх населенню, на довільних 5 містах 
def c_scatter(ua_img, c_cords, c_pops):
    pyp.figure(figsize=(15, 15))
    pyp.axis('off')
    pyp.imshow(ua_img)
    pyp.scatter(c_cords[:, 0], c_cords[:, 1], s = c_pops / 3000, c = 'red')
    pyp.show()

# 3. Знайти найбільшу відстань між містами в пікселях та кілометрах
def biggest_dist_c(c_cords, c_names):
    c_lat_lon = (p.read_csv('ukr_plata.csv', encoding='cp1251', sep=','))
    our_lat_lon = c_lat_lon[c_lat_lon['city'].isin(c_names)]
    find_biggest_dist_km(our_lat_lon)
    find_biggest_dist_corrds(c_cords)

def find_biggest_dist_km(our_lat_lon):
    our_lat_lon = our_lat_lon.reset_index()
    max_dist = -1
    max_index_i = 0
    max_index_j = 0
    for index, row in our_lat_lon.iterrows():
        for index2, row2 in our_lat_lon.iterrows():
            dist = d.geodesic((row['Lat'], row['Lon']), (row2['Lat'], row2['Lon'])).km
            if max_dist < dist:
                max_dist = dist
                max_index_i = index
                max_index_j = index2
    print('Найбільша відстань між містами {0} та {1}'.format(our_lat_lon['city'][max_index_i], our_lat_lon['city'][max_index_j]))
    print('Відстань в км: ', round(max_dist, 4))

def find_biggest_dist_corrds(c_coords):
    max_dist = -1
    for coord in c_coords:
        for coord2 in c_coords:
            dist = math.dist(coord, coord2)
            if max_dist < dist:
                max_dist = dist
    print('Відстань в пикселях: ', round(max_dist, 4))

# 4. Завантажити shape-файл с областями України.
def read_shp(path):
    return gp.read_file(path)

# 5.Побудувати картограми для прибутку населення на 1 особу і ВВП по регіонам за 2016 рік.
def draw_dpp_map_2016(u_shp, dpp):
    geo_dpp = gp.GeoDataFrame(u_shp.merge(dpp, on = ['Name']))
    geo_dpp.plot(column = '2016',
                 legend = True,
                 legend_kwds = {'label': "Прибуток населення на 1 особу за 2016 рік"},
                 missing_kwds = {"color": "gray"},
                 figsize = (17, 10),
                 cmap = 'summer',
                 edgecolor = 'green')
    pyp.axis('off')

def draw_gdp_map_2016(u_shp, gdp):
    gdp_map = gp.GeoDataFrame(u_shp.merge(gdp, on = ['Name']))
    gdp_map.plot(column='2016', \
                 legend=True, \
                 legend_kwds={'label': "ВВП за 2016 рік"}, \
                 missing_kwds = {"color": "gray"}, \
                 figsize=(17, 10), \
                 cmap='summer', \
                 edgecolor='green')
    pyp.axis('off')

# 6. По даним за 2006-2015 роки для кожного регіону розрахувати коефіцієнт кореляції між прибутком населення на 1 особу та ВВП.
# Відобразити на картограмі.
def cor_calculate(first, second, names):
    correlations = p.DataFrame();
    correlations['correlation'] = first.corrwith(second, axis = 1)
    correlations['Name'] = names
    return correlations

def draw_cor_map(u_shp, cor):
    cor_map = p.merge(u_shp, cor, on=['Name'])
    cor_map.plot(column = 'correlation', \
                 legend = True, \
                 legend_kwds = {'label': 'Кореляція між прибутком та ВВП'}, \
                 missing_kwds = {'color': 'gray'}, \
                 figsize = (17, 10), \
                 cmap = 'YlGn', \
                 edgecolor = 'green')
    pyp.axis('off')
    pyp.show()

def main():
    ua_img = read_img('Ukraine.jpg')
    c_cords = [(22, 269), (787, 275), (394, 416), (424, 79), (386, 145)]
    c_pop = [115500, 424113, 1017022, 295670, 2868702]
    c = ['Ужгород', 'Луганськ', 'Одеса', 'Чернігів', 'Київ']
    c_scatter(ua_img, n.array(c_cords), n.array(c_pop))
    biggest_dist_c(n.array(c_cords), c)
    u_shp = read_shp('UKR_ADM1.shp.zip')
    dpp =  read_dataset('ukr_DPP.csv')
    gdp = read_dataset('ukr_GDP.csv')
    draw_dpp_map_2016(u_shp, dpp)
    draw_gdp_map_2016(u_shp, gdp)
    cor = cor_calculate(dpp.iloc[: , 6:], gdp.iloc[: , 6:], gdp['Name'])
    print(cor)
    draw_cor_map(u_shp, cor)

if __name__ == '__main__':
    main()