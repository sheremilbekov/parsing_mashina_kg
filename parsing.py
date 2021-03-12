import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    otvet = requests.get(url)
    return otvet.text

def get_vse_stranicy(html):
    soup = BeautifulSoup(html, 'lxml')
    stranicy_ul = soup.find('ul', class_ = "pagination")
    posled_stranica = stranicy_ul.find_all('li')[-1]
    total_pages = posled_stranica.find('a').get('href').split('=')[-1]
    return int(total_pages)


def zapisat_v_csv(data):
    with open('cars_mashina.csv', 'a+') as csv_file:
        writer = csv.writer(csv_file, delimiter = '/')
        writer.writerow((data['marka'], data['cena'], data['opisanie'], data['photo']))


def poluchit_dannye_stranicy(html):
    soup = BeautifulSoup(html, "lxml")
    spisok_mashin = soup.find('div', class_ = "table-view-list")
    total_mashiny = spisok_mashin.find_all('div', class_ = "list-item")

    for cars in total_mashiny:
        try:
            photo = [i.get('data-src') for i in cars.find_all('img')]
        except:
            photo = ''

        try:
            marka = cars.find('h2', class_ = 'name').text.strip()
        except:
            marka = ''

        try:
            cena = cars.find('strong').text.strip()
        except:
            cena = ''
        try:
            d1 = cars.find('div',class_="item-info-wrapper").find('p', class_='year-miles').text.replace('\n','').replace(' ', '')
            d2 = cars.find('div',class_="item-info-wrapper").find('p', class_='body-type').text.replace('\n','').replace(' ', '')
            d3 = cars.find('div',class_="item-info-wrapper").find('p', class_='volume').text.replace('\n','').replace(' ', '')
            opisanie = f'{d1}, {d2}, {d3}'
        except:
            opisanie = ''

    data = {'marka': marka, 'cena': cena, 'opisanie': opisanie, 'photo': photo}
    zapisat_v_csv(data)



def main():
    mashina_url = "https://www.mashina.kg/search/all/"
    stranicy = "?page="
    get_vse_stranicy(get_html(mashina_url))
    # get_vse_stranicy(mashina_url)

    for stroka in range(1, 30):
        url_dlya_str = mashina_url + stranicy + str(stroka)
        html = get_html(url_dlya_str)
        poluchit_dannye_stranicy(html)

main()