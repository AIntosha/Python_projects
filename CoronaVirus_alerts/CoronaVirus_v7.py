import pandas as pd
import datetime
import json

country_dict = dict()

worS = b'\xf0\x9f\x8c\x8d'.decode()
usaFlag = b'\xf0\x9f\x87\xba\xf0\x9f\x87\xb8'.decode()
italyFlag = b'\xf0\x9f\x87\xae\xf0\x9f\x87\xb9'.decode()
spainFlag = b'\xf0\x9f\x87\xaa\xf0\x9f\x87\xb8'.decode()
chinaFlag = b'\xf0\x9f\x87\xa8\xf0\x9f\x87\xb3'.decode()
germanyFlag = b'\xf0\x9f\x87\xa9\xf0\x9f\x87\xaa'.decode()
russiaFlag = b'\xf0\x9f\x87\xb7\xf0\x9f\x87\xba'.decode()
franceFlag = b'\xf0\x9f\x87\xab\xf0\x9f\x87\xb7'.decode()
ukFlag = b'\xf0\x9f\x87\xac\xf0\x9f\x87\xa7'.decode()
iranFlag = b'\xf0\x9f\x87\xae\xf0\x9f\x87\xb7'.decode()
turkeyFlag = b'\xf0\x9f\x87\xb9\xf0\x9f\x87\xb7'.decode()
swisFlag = b'\xf0\x9f\x87\xa8\xf0\x9f\x87\xad'.decode()
netherFlag = b'\xf0\x9f\x87\xb3\xf0\x9f\x87\xb1'.decode()
belgiumFlag = b'\xf0\x9f\x87\xa7\xf0\x9f\x87\xaa'.decode()
brazilFlag = b'\xf0\x9f\x87\xa7\xf0\x9f\x87\xb7'.decode()
portugalFlag = b'\xf0\x9f\x87\xb5\xf0\x9f\x87\xb9'.decode()
israelFlag = b'\xf0\x9f\x87\xae\xf0\x9f\x87\xb1'.decode()
indiaFlag = b'\xf0\x9f\x87\xae\xf0\x9f\x87\xb3'.decode()
peruFlag = b'\xf0\x9f\x87\xb5\xf0\x9f\x87\xaa'.decode()
pakistanFlag = b'\xf0\x9f\x87\xb5\xf0\x9f\x87\xb0'.decode()

### get yesterday date
yesterday = str(int(datetime.datetime.now().strftime('%d'))-1)
if int(yesterday) < 10:
    yesterday = "0"+str(int(datetime.datetime.now().strftime('%d'))-1)

date = datetime.datetime.now().strftime('%m-')+yesterday+'-'+datetime.datetime.now().strftime('%Y')+'.csv'

### read from pandas csv
URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+date
# URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/08-31-2020.csv"

df = pd.read_csv(URL)

### Посчитаем кол-во сл\см\вз среди нонКитая
### фильтруем строчки где написано китай
Russia = df['Country_Region'] == "Russia"
dfRussia = df[Russia]
US = df['Country_Region'] == "US"
dfUS = df[US]
UK = df['Country_Region'] == "United Kingdom"
dfUK = df[UK]
Brazil = df['Country_Region'] == "Brazil"
dfBrazil = df[Brazil]
India = df['Country_Region'] == "India"
dfIndia = df[India]

# добавляем в словарь и США и Китай
country_dict['US'] = dfUS.Active.sum()
country_dict['United Kingdom'] = dfUK.Active.sum()
country_dict['Brazil'] = dfBrazil.Active.sum()
country_dict['Russia'] = dfRussia.Active.sum()
country_dict['India'] = dfIndia.Active.sum()

### Читаем вчерашние значения и записываем их в 6 переменных
with open('data_yesterday.txt', "r") as fileRead:
    prevRusConfirmed = int(fileRead.readline().strip())
    prevRusDeaths = int(fileRead.readline().strip())
    prevRusRecovered = int(fileRead.readline().strip())
    prevConfirmed = int(fileRead.readline().strip())
    prevDeaths = int(fileRead.readline().strip())
    prevRecovered = int(fileRead.readline().strip())

### Берем нынешние значения и вчерашние и пишем процентаж
### Считаем процентаж
percentConfirmed = int(round((df.Confirmed.sum() / prevConfirmed - 1) * 100))
percentDeaths = int(round((df.Deaths.sum() / prevDeaths - 1) * 100))
percentRecovered = int(round((df.Recovered.sum() / prevRecovered - 1) * 100))

newConfirmed = df.Confirmed.sum() - prevConfirmed
newDeaths = df.Deaths.sum() - prevDeaths
newRecovered = df.Recovered.sum() - prevRecovered

### считаем процентаж России
percentRusConfirmed = int(round((dfRussia.Confirmed.sum() / prevRusConfirmed - 1) * 100))
percentRusDeaths = int(round((dfRussia.Deaths.sum() / prevRusDeaths - 1) * 100))
percentRusRecovered = int(round((dfRussia.Recovered.sum() / prevRusRecovered - 1) * 100))

newRusConfirmed = dfRussia.Confirmed.sum() - prevRusConfirmed
newRusDeaths = dfRussia.Deaths.sum() - prevRusDeaths
newRusRecovered = dfRussia.Recovered.sum() - prevRusRecovered

### Пишем итоговые данные по России
print('**—— '+datetime.datetime.now().strftime('%d-%m-%Y')+' ——')
print('—', russiaFlag, 'Россия', russiaFlag, '—')
print('Всего случаев:', dfRussia.Confirmed.sum(), '**`(+'+str(newRusConfirmed)+' +'+str(percentRusConfirmed)+'%)`')
print('**Смертей:', dfRussia.Deaths.sum(),        '**`(+'+str(newRusDeaths)+' +'+str(percentRusDeaths)+'%)`')
print('**Выздоровело:', dfRussia.Recovered.sum(), '**`(+'+str(newRusRecovered)+' +'+str(percentRusRecovered)+'%)`')
### Пишем итоговые данные по миру
print('**—', worS, 'Мир', worS, '—')
print('Всего случаев:', df.Confirmed.sum(), '**`(+'+str(newConfirmed)+' +'+str(percentConfirmed)+'%)`')
print('**Смертей:', df.Deaths.sum(), '**`(+'+str(newDeaths)+' +'+str(percentDeaths)+'%)`')
print('**Выздоровело:', df.Recovered.sum(), '**`(+'+str(newRecovered)+' +'+str(percentRecovered)+'%)`')
print('**— Рейтинг по активным зараженным —**')
print('  —( Без умерших и выздоровевших )—')

### Заменяем данные в нашем файле прошлого дня
with open('data_yesterday.txt', 'w') as fileWrite:
    fileWrite.write(str(dfRussia.Confirmed.sum())+"\n")
    fileWrite.write(str(dfRussia.Deaths.sum())+"\n")
    fileWrite.write(str(dfRussia.Recovered.sum())+"\n")
    fileWrite.write(str(df.Confirmed.sum())+"\n")
    fileWrite.write(str(df.Deaths.sum())+"\n")
    fileWrite.write(str(df.Recovered.sum()))

### запишем новый файл для хранения истории понадобится для бекапов
with open('history.txt', 'a') as fileWrite:
    fileWrite.write(datetime.datetime.now().strftime('%m-')+yesterday+'-'+datetime.datetime.now().strftime('%Y')+"\n")
    fileWrite.write(str(dfRussia.Confirmed.sum())+"\n")
    fileWrite.write(str(dfRussia.Deaths.sum())+"\n")
    fileWrite.write(str(dfRussia.Recovered.sum())+"\n")
    fileWrite.write(str(df.Confirmed.sum())+"\n")
    fileWrite.write(str(df.Deaths.sum())+"\n")
    fileWrite.write(str(df.Recovered.sum())+"\n"+"\n")

### Блок рейтинга
# Выведем df без США и без Китая
df = df[df.Country_Region != "China"]
df = df[df.Country_Region != "US"]
df = df[df.Country_Region != "United Kingdom"]
df = df[df.Country_Region != "Brazil"]
df = df[df.Country_Region != "Russia"]
df = df[df.Country_Region != "India"]


# Выведем топ без США и без Китая
sorted_list = df.sort_values(by=["Confirmed"], ascending=False)

# В словарь вкинуть 10 топ стран
for i in range(10):
    country_dict[sorted_list.iloc[i]['Country_Region']] = sorted_list.iloc[i]['Confirmed']

for i in range(len(df)):
    country_dict[df.iloc[i]['Country_Region']] = df.iloc[i]['Active']

# yesterday load
with open('yesterday.json', 'r') as file:
    yest_dict = json.load(file)

# yesterday dump
import numpy as np
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

with open('yesterday.json', "w") as file:
    json.dump(country_dict, file, cls=NpEncoder)


# вывести топ5 из словаря
for i in range(6):
    maximum = max(country_dict, key=country_dict.get)
    percenttemp = int(round(((country_dict[maximum] / yest_dict[maximum]) - 1) * 100))
    new = int(country_dict[maximum] - yest_dict[maximum])

    if maximum == "US":
        print(str('`')+str(i+1)+'.` **'+ usaFlag +' USA -', int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Italy":
        print(str('`')+str(i+1)+'.` **'+ italyFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Spain":
        print(str('`')+str(i+1)+'.` **'+ spainFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "China":
        print(str('`')+str(i+1)+'.` **'+ chinaFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Germany":
        print(str('`')+str(i+1)+'.` **'+ germanyFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "France":
        print(str('`')+str(i+1)+'.` **'+ franceFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "United Kingdom":
        print(str('`')+str(i+1)+'.` **'+ ukFlag +' UK -', int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Iran":
        print(str('`')+str(i+1)+'.` **'+ iranFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Turkey":
        print(str('`')+str(i+1)+'.` **'+ turkeyFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Switzerland":
        print(str('`')+str(i+1)+'.` **'+ swisFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Netherlands":
        print(str('`')+str(i+1)+'.` **'+ netherFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Belgium":
        print(str('`')+str(i+1)+'.` **'+ belgiumFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Brazil":
        print(str('`')+str(i+1)+'.` **'+ brazilFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Portugal":
        print(str('`')+str(i+1)+'.` **'+ portugalFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Israel":
        print(str('`')+str(i+1)+'.` **'+ israelFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "India":
        print(str('`')+str(i+1)+'.` **'+ indiaFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Peru":
        print(str('`')+str(i+1)+'.` **'+ peruFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Pakistan":
        print(str('`')+str(i+1)+'.` **'+ pakistanFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    elif maximum == "Russia":
        print(str('`')+str(i+1)+'.` **'+ russiaFlag, maximum, "-", int(country_dict[maximum]), str('**'), end='')
    else:
        print(str('`')+str(i+1)+'.`**',maximum, "-", country_dict[maximum], str('**'))

    if percenttemp < 0:
        print('`(' + str(new) + ' ' + str(percenttemp) + '%)`')
    elif percenttemp > 0:
        print('`(+' + str(new) + ' +' + str(percenttemp) + '%)`')
    else:
        if new > 0:
            print('`(+' + str(new) + ' ' + str(percenttemp) + '%)`')
        else:
            print('`(' + str(new) + ' ' + str(percenttemp) + '%)`')

    del country_dict[maximum]