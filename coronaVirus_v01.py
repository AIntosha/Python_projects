import pandas as pd
import datetime

eurS = b'\xf0\x9f\x8c\x8e'.decode()
worS = b'\xf0\x9f\x8c\x8d'.decode()
rusS = b'\xf0\x9f\x87\xb7\xf0\x9f\x87\xba'.decode()

### get yesterday date
yesterday = str(int(datetime.datetime.now().strftime('%d'))-1)
if int(yesterday) < 10:
    yesterday = "0"+str(int(datetime.datetime.now().strftime('%d'))-1)

date = datetime.datetime.now().strftime('%m-')+yesterday+'-'+datetime.datetime.now().strftime('%Y')+'.csv'

### read from pandas csv
# URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+date
URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/03-31-2020.csv"
df = pd.read_csv(URL)
# print(frame)

### count total confirmed\deaths\recovered
# print('Подтвержденных случаев:', frame.Confirmed.sum())
# print('Смертей:', frame.Deaths.sum())
# print('Выздоровели:', frame.Recovered.sum())

### Читаем вчерашние значения и записываем их в 6 переменных
with open('data.txt', "r") as fileRead:
    prevConfirmed = int(fileRead.readline().strip())
    prevDeaths = int(fileRead.readline().strip())
    prevRecovered = int(fileRead.readline().strip())

    prevNonConfirmed = int(fileRead.readline().strip())
    prevNonDeaths = int(fileRead.readline().strip())
    prevNonRecover = int(fileRead.readline().strip())

    prevRusConfirmed = int(fileRead.readline().strip())
    prevRusDeaths = int(fileRead.readline().strip())
    prevRusRecover = int(fileRead.readline().strip())

### Берем нынешние значения и вчерашние и пишем процентаж
### Считаем процентаж
percentConfirmed = int(round((df.Confirmed.sum() / prevConfirmed - 1) * 100))
percentDeaths = int(round((df.Deaths.sum() / prevDeaths - 1) * 100))
percentRecovered = int(round((df.Recovered.sum() / prevRecovered - 1) * 100))

### Посчитаем кол-во сл\см\вз среди нонКитая
### фильтруем строчки где написано китай
nonChina = df['Country_Region'] != "China"
Russia = df['Country_Region'] == "Russia"
dfnonChina = df[nonChina]
dfRussia = df[Russia]

### считаем процентаж НОНкитай и России
percentNonConfirmed = int(round((dfnonChina.Confirmed.sum() / prevNonConfirmed - 1) * 100))
percentNonDeaths = int(round((dfnonChina.Deaths.sum() / prevNonDeaths - 1) * 100))
percentNonRecovered = int(round((dfnonChina.Recovered.sum() / prevNonRecover - 1) * 100))

percentRusConfirmed = int(round((dfRussia.Confirmed.sum() / prevRusConfirmed - 1) * 100))
if prevRusDeaths == 0:
    percentRusDeaths = 0
else:
    percentRusDeaths = int(round((dfRussia.Deaths.sum() / prevRusDeaths - 1) * 100))
percentRusRecovered = int(round((dfRussia.Recovered.sum() / prevRusRecover - 1) * 100))

### Пишем итоговые данные по Нонкитаю
print('-------- '+datetime.datetime.now().strftime('%d-%m-%Y')+' --------')
print('---', eurS, 'nonChina', eurS, '---')
print('Confirmed:', dfnonChina.Confirmed.sum(), '(+'+str(percentNonConfirmed)+'%)')
print('Deaths:', dfnonChina.Deaths.sum(), '(+'+str(percentNonDeaths)+'%)')
print('Recovered:', dfnonChina.Recovered.sum(), '(+'+str(percentNonRecovered)+'%)')
### Пишем итоговые данные по миру
print('---', worS, 'World', worS, '---')
print('Confirmed:', df.Confirmed.sum(), '(+'+str(percentConfirmed)+'%)')
print('Deaths:', df.Deaths.sum(), '(+'+str(percentDeaths)+'%)')
print('Recovered:', df.Recovered.sum(), '(+'+str(percentRecovered)+'%)')
### Пишем итоговые данные по России
print('---', rusS, 'Russia', rusS, '---')
print('Confirmed:', dfRussia.Confirmed.sum(), '(+'+str(percentRusConfirmed)+'%)')
print('Deaths:', dfRussia.Deaths.sum(), '(+'+str(percentRusDeaths)+'%)')
print('Recovered:', dfRussia.Recovered.sum(), '(+'+str(percentRusRecovered)+'%)')

### Заменяем данные в нашем файле прошлого дня
with open('data.txt', 'w') as fileWrite:
    fileWrite.write(str(df.Confirmed.sum())+"\n")
    fileWrite.write(str(df.Deaths.sum())+"\n")
    fileWrite.write(str(df.Recovered.sum())+"\n")
    fileWrite.write(str(dfnonChina.Confirmed.sum())+"\n")
    fileWrite.write(str(dfnonChina.Deaths.sum())+"\n")
    fileWrite.write(str(dfnonChina.Recovered.sum())+"\n")
    fileWrite.write(str(dfRussia.Confirmed.sum())+"\n")
    fileWrite.write(str(dfRussia.Deaths.sum())+"\n")
    fileWrite.write(str(dfRussia.Recovered.sum()))

### запишем новый файл для хранения истории понадобится для бекапов
with open('history.txt', 'a') as fileWrite:
    fileWrite.write(datetime.datetime.now().strftime('%m-')+yesterday+'-'+datetime.datetime.now().strftime('%Y')+"\n")
    fileWrite.write(str(df.Confirmed.sum())+"\n")
    fileWrite.write(str(df.Deaths.sum())+"\n")
    fileWrite.write(str(df.Recovered.sum())+"\n")
    fileWrite.write(str(dfnonChina.Confirmed.sum())+"\n")
    fileWrite.write(str(dfnonChina.Deaths.sum())+"\n")
    fileWrite.write(str(dfnonChina.Recovered.sum())+"\n")
    fileWrite.write(str(dfRussia.Confirmed.sum())+"\n")
    fileWrite.write(str(dfRussia.Deaths.sum())+"\n")
    fileWrite.write(str(dfRussia.Recovered.sum())+"\n"+"\n")
