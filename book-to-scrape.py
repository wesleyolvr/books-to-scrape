import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import re


def save_books_csv(list_info_books):
    file_name = 'books.csv'
    df = pd.DataFrame(list_info_books)
    df.to_csv(file_name, index=False,sep=';')
    print('Arquivo criado com sucesso!')

def has_next_page(soup):
    next_page = soup.find('li', class_='next')
    return True if next_page else False

def get_link_url(soup):
    next_url_href = soup.find(class_='next').find('a')['href']
    if 'cata' in next_url_href:
        url = 'http://books.toscrape.com/' + next_url_href
        print('Proxima pagina: {}'.format(url))
    else:
        url = 'http://books.toscrape.com/catalogue/' + next_url_href
        print('Proxima pagina: {}'.format(url))
        
    return url
    
def extractor_books():
    url = 'http://books.toscrape.com/'
    list_info_books = []
    while True:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article')
            for book in books:
                title = book.find('h3').find('a')['title']
                title = re.sub('[!@#$*]', '', title)
                in_stock = 'in stock' if book.find(class_='icon-ok') else 'out stock'
                price = book.find(class_='price_color').string[1:]
                info_book = {
                    'Title': title,
                    'In_stock': in_stock,
                    'Price': price,
                    'Link': book.find('h3').find('a')['href'],
                    'Image': book.find('img')['src'],
                    'Rating': book.find(class_='star-rating')['class'][-1],
                }
                list_info_books.append(info_book)
                pprint(info_book)
            if has_next_page(soup):
                url = get_link_url(soup)
            else:
                print('Fim da pagina.')
                break
        except Exception as e:
            print(e)
            break
    return list_info_books

def run():
    list_info_books = extractor_books()
    save_books_csv(list_info_books)
     
if __name__ == '__main__':
    run()        

    

