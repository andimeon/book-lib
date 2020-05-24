from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
import os
from urllib import parse
import glob

BOOTSTRAP_FILE = {
    'css': 'bootstrap.min.css',
    'jquery': 'jquery-3.4.1.slim.min.js',
    'popper': 'popper.min.js',
    'bootstrap': 'bootstrap.min.js',
}


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books_on_pages = get_books_pages()
    pages_href = get_pages_links(len(books_on_pages))
    remove_files()
    
    for count, books_page in enumerate(books_on_pages):
        rendered_page = template.render(
            bootstrap_path=BOOTSTRAP_FILE,
            books_metadata=list(chunked(books_page, 2)),
            pages_href=pages_href,
            previous_page_href=get_previous_page_link(count, pages_href),
            next_page_href=get_next_page_link(count, pages_href),
            page_number=count + 1,
        )
        
        with open(f'pages/index{count}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def get_books_pages():
    global books_metadata
    return [books_metadata[i: i + 10] for i in range(0, len(books_metadata), 10)]


def get_url_quote(books):
    for count, book in enumerate(books):
        book_path = os.path.join('../', book['book_path'])
        img_path = os.path.join('../', book['img_src'])
        books[count]['book_path'] = parse.quote(book_path)
        books[count]['img_src'] = parse.quote(img_path)
    return books


def get_pages_links(pages_numbers):
    return [f'/pages/index{num}.html' for num in range(pages_numbers)]


def get_previous_page_link(count, pages_href):
    if count != 0:
        return pages_href[count - 1]
    else:
        return None


def get_next_page_link(count, pages_href):
    if count != (len(pages_href) - 1):
        return pages_href[count + 1]
    else:
        return None


def bootstrap_file_path():
    BOOTSTRAP_FILE['css'] = os.path.join('../static', BOOTSTRAP_FILE['css'])
    BOOTSTRAP_FILE['jquery'] = os.path.join('../static', BOOTSTRAP_FILE['jquery'])
    BOOTSTRAP_FILE['popper'] = os.path.join('../static', BOOTSTRAP_FILE['popper'])
    BOOTSTRAP_FILE['bootstrap'] = os.path.join('../static', BOOTSTRAP_FILE['bootstrap'])


def remove_files():
    pages_folder = os.path.join(os.getcwd(), 'pages/*')
    files = glob.glob(pages_folder)
    for file in files:
        os.remove(file)


if __name__ == '__main__':
    os.makedirs('pages', exist_ok=True)
    with open('books_metadata.json', 'r') as file:
        books_metadata_json = json.load(file)
    books_metadata = get_url_quote(books_metadata_json)
    bootstrap_file_path()
    
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
