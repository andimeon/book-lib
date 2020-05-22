import requests
from requests import HTTPError
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
import argparse
import datetime


def get_book(url, soup, books_folder):
    response = get_response(url)
    selector = '.ow_px_td h1'
    headers_tags = soup.select_one(selector).text
    header = headers_tags.split("::")
    title, author = header
    timestamp = round(datetime.datetime.now().timestamp(), 3)
    book_name = sanitize_filename(title.strip())
    filename = f'{timestamp}_{book_name}.txt'
    full_filename = os.path.join(books_folder, filename)
    save_book(full_filename, response)
    return {'title': title.strip(), 'author': author.strip(), 'book_path': full_filename}


def save_book(full_filename, response):
    with open(full_filename, 'w') as file:
        file.write(response.text)


def get_image(url, soup, images_folder):
    selector = '.bookimage img'
    img_link = soup.select_one(selector)['src']
    img_url = urljoin(url, img_link)
    response = get_response(img_url)
    image_name = img_url.split('/')[-1]
    timestamp = round(datetime.datetime.now().timestamp(), 3)
    filename = f'{timestamp}_{image_name}'
    full_filename = os.path.join(images_folder, filename)
    save_image(full_filename, response)
    return full_filename


def save_image(full_filename, response):
    with open(full_filename, 'wb') as file:
        file.write(response.content)


def parse_url(url):
    response = get_response(url)
    return BeautifulSoup(response.text, 'lxml')


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.history:
        raise requests.exceptions.HTTPError
    return response


def get_comments(soup):
    selector = '.texts'
    comments_tags = soup.select(selector)
    return [comment_tag.select_one('.black').text for comment_tag in comments_tags]


def get_genres(soup):
    genres = soup.select('span.d_book a')
    return [genre.text for genre in genres]


def create_parser():
    parser = argparse.ArgumentParser(
        description='Download books from http://tululu.org/'
    )
    parser.add_argument('--start_page', help='from what page to start downloading(', default=1, type=int)
    parser.add_argument('--end_page', help='until what page downloading', default=702, type=int)
    parser.add_argument('--dest_folder', help='folder for downloading books, images, JSON')
    parser.add_argument('--json_path', help='folder for downloading JSON')
    parser.add_argument('--skip_imgs', help='skip downloading images', action='store_const', const=True, default=False)
    parser.add_argument('--skip_txt', help='skip downloading books', action='store_const', const=True, default=False)
    
    return parser


def rewrite_json(data, filename):
    books_metadata = []
    try:
        with open(filename) as json_file: 
            books_metadata = json.load(json_file)
    except Exception:
        print('First data')
    
    books_metadata.append(data)
    with open(filename,'w', encoding='utf8') as file: 
        json.dump(books_metadata, file, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    pages_range = range(args.start_page, args.end_page)
    skip_txt = args.skip_txt
    skip_images = args.skip_imgs
    
    if args.dest_folder is None:
        books_folder = 'books'
        images_folder = 'images'
        json_full_path = 'books_metadata.json'
    else:
        books_folder = os.path.join(args.dest_folder, 'books')
        images_folder = os.path.join(args.dest_folder, 'images')
        json_full_path = os.path.join(args.dest_folder, 'books_metadata.json')
    if args.json_path is not None:
        json_full_path = os.path.join(args.json_path, 'books_metadata.json')
    
    os.makedirs(books_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    
    for page in pages_range:
        page_url = f'http://tululu.org/l55/{page}/'
        print(page_url)
        try:
            page_soup = parse_url(page_url)
        except HTTPError:
            print(f'Страница {page_url} не отвечает')
            print('Переход к следующей странице')
            continue
        
        book_tags = page_soup.select('.d_book')
        
        for book_tag in book_tags:
            book_metadata = {}
            book_link_tag = book_tag.select_one('a')['href']
            book_url = urljoin(page_url, book_link_tag)
            print(book_url)
            try:
                book_soup = parse_url(book_url)
                book_txt_link = book_soup.select_one('a[href^="/txt"]')['href']
                book_txt_url = urljoin(page_url, book_txt_link)
                
                if not skip_txt:
                    book_metadata = get_book(book_txt_url, book_soup, books_folder)
                if not skip_images:
                    book_metadata['img_src'] = get_image(page_url, book_soup, images_folder)
                book_metadata['comments'] = get_comments(book_soup)
                book_metadata['genre'] = get_genres(book_soup)
            except HTTPError:
                print(f'Страница {book_url} не отвечает')
                continue
            except TypeError:
                print('Нет книги в формате txt')
                continue
            rewrite_json(book_metadata, json_full_path)
