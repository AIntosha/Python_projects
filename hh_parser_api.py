import requests
import statistics

vacancy = input('Введите название вакансии:\n')

usdrate = 80
vacancywithSalary = 0
avgsalarylist = list()


def responce(page, per_page, text=vacancy):
    responce = requests.get('https://api.hh.ru/vacancies/',
                            headers={'User-Agent': 'Python (fuoff@gmail.com)'},
                            params={
                                'text': text,
                                'page': page,
                                'per_page': per_page
                            })
    return responce.json()


for x in range(responce(page=0, per_page=100)['pages']):
    templist = responce(page=x, per_page=100)['items']
    for i in templist:
        if i['salary'] is None:
            continue
        else:
            vacancywithSalary += 1
            if i['salary']['currency'] == 'RUR':
                if i['salary']['from'] is None and i['salary']['to'] is not None:
                    avgsalarylist.append(i['salary']['to'])
                elif i['salary']['from'] is not None and i['salary']['to'] is None:
                    avgsalarylist.append(i['salary']['from'])
                elif i['salary']['from'] is not None and i['salary']['to'] is not None:
                    avgsalarylist.append(int(round((i['salary']['from'] + i['salary']['to']) / 2)))
                else:
                    print('ERRRRRORRRR')
            # USD
            else:
                if i['salary']['from'] is None and i['salary']['to'] is not None:
                    avgsalarylist.append(i['salary']['to'] * usdrate)
                elif i['salary']['from'] is not None and i['salary']['to'] is None:
                    avgsalarylist.append(i['salary']['from'] * usdrate)
                elif i['salary']['from'] is not None and i['salary']['to'] is not None:
                    avgsalarylist.append(int(round(((i['salary']['from'] + i['salary']['to']) / 2) * usdrate)))
                else:
                    print('ERRRRRORRRR')

print('Профессия:', vacancy)
print('Всего вакансий:', responce(page=0, per_page=1)['pages'])
print('Вакансий с ценой:', vacancywithSalary)
print('Средняя зарплата:', int(round(statistics.median(avgsalarylist))), 'руб')
