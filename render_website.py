from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
import os
from urllib import parse
import glob

BOOTSTRAP_FILE_PATH = {
    'css': '../static/bootstrap.min.css',
    'jquery': '../static/jquery-3.4.1.slim.min.js',
    'popper': '../static/popper.min.js',
    'bootstrap': '../static/bootstrap.min.js',
}


def render_website_pages():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books_on_pages = list(chunked(BOOKS_METADATA, 10))
    pages_href = [f'../pages/index{num}.html' for num in range(len(books_on_pages))]
    remove_files()
    
    # ниже в цикле задействованы обе переменные функции enumerate: count, books_on_page
    for count, books_on_page in enumerate(books_on_pages):
        rendered_page = template.render(
            bootstrap_path=BOOTSTRAP_FILE_PATH,
            books_metadata=list(chunked(books_on_page, 2)),
            pages_href=pages_href,
            previous_page_href=get_previous_page_link(count, pages_href),
            next_page_href=get_next_page_link(count, pages_href),
            page_number=count + 1,
        )
        
        with open(f'pages/index{count}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def quote_url(books):
    for count, book in enumerate(books):
        book_path = os.path.join('../', book['book_path'])
        img_path = os.path.join('../', book['img_src'])
        books[count]['book_path'] = parse.quote(book_path)
        books[count]['img_src'] = parse.quote(img_path)
    return books


def get_previous_page_link(count, pages_href):
    if not count:
        return pages_href[count - 1]
    else:
        return None


def get_next_page_link(count, pages_href):
    if count != len(pages_href) - 1:
        return pages_href[count + 1]
    else:
        return None


def remove_files():
    pages_folder = os.path.join(os.getcwd(), 'pages/*')
    files = glob.glob(pages_folder)
    for file in files:
        os.remove(file)


if __name__ == '__main__':
    os.makedirs('pages', exist_ok=True)
    with open('books_metadata.json', 'r') as file:
        books_metadata_json = json.load(file)

    BOOKS_METADATA = quote_url(books_metadata_json)
    
    render_website_pages()
    server = Server()
    server.watch('template.html', render_website_pages)
    server.serve(root='.')
