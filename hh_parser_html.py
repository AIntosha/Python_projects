from requests_html import HTMLSession
from time import sleep
import re

session = HTMLSession()

profName = input('Введите название профессии и нажмите enter:\n')
url = "https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=" + profName + "&page=0"

page = session.get(url)

page_num = 1
withSalaryNum = 0
vacNum = ''
avgSalary = 0
salaryList = list()

### calculating total num of vacancy
vacNumPage = page.html.find(
    'body > div.HH-MainContent.HH-Supernova-MainContent > div > div > div.bloko-columns-wrapper'
    ' > div > div.bloko-column.bloko-column_xs-0.bloko-column_s-8.bloko-column_m-12.bloko-column'
    '_l-16 > div > h1')

if re.search("^По запросу", vacNumPage[0].text) != None:
    print('Такой профессии нет')
else:
    xRegex = re.compile('\d')
    allnumbers = re.findall(xRegex, vacNumPage[0].text)
    for i in allnumbers:
        vacNum += i

### calculating avg. salary
while page:
    print('Калькулируем страницу', page_num, '\\', (int(vacNum) // 50) + 1)

    items = page.html.find('.vacancy-serp-item')

    ### вывод всех зарплат

    for item in items:
        salary = item.find('.vacancy-serp-item__sidebar')

        if len(salary[0].text) < 2:
            pass
        else:
            withSalaryNum += 1
            newLine = salary[0].text
            newLine1 = ''
            newLine2 = ''

            if re.findall('^от', newLine):
                newLine = re.sub('от\s', '', newLine)
            elif re.findall('^до', newLine):
                newLine = re.sub('до\s', '', newLine)

            if re.findall('\s', newLine):
                newLine = re.sub('\s', '', newLine)

            if re.findall('руб.$', newLine):
                newLine = re.sub('руб.$', '', newLine)
                if re.findall('-', newLine):
                    newLine1 = int(re.sub('-.*', '', newLine))
                    newLine2 = int(re.sub('.*-', '', newLine))
                    salaryList.append(int(round((newLine1 + newLine2) / 2)))
                else:
                    salaryList.append(int(newLine))

            elif re.findall('USD$', newLine):
                newLine = re.sub('USD$', '', newLine)
                if re.findall('-', newLine):
                    newLine1 = int(re.sub('-.*', '', newLine))
                    newLine2 = int(re.sub('.*-', '', newLine))
                    salaryList.append(int(round((newLine1 + newLine2) * 40)))
                else:
                    salaryList.append(round(int(newLine) * 80))

    try:
        next_page = list(page.html.find('.HH-Pager-Controls-Next')[0].absolute_links)[0]
        sleep(5)
        page_num += 1
        page = session.get(next_page)
    except:
        print('Калькулирование закончено')
        print('-------------------------')
        print('Профессия:', profName)
        print('Всего вакансий:', vacNum)
        print('Вакансий с зарплатой:', withSalaryNum)

        for i in salaryList:
            avgSalary += i
        avgSalary /= len(salaryList)

        print('Средняя зарплата:', int(round(avgSalary)), 'руб')
        break
