from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell
from more_itertools import chunked
import os
from urllib import parse


def on_reload():
    env = Environment(
        loader=FileSystemLoader('pages/'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    books_on_pages = get_books_pages()
    pages_href = get_pages_links(len(books_on_pages))
    
    for count, books_page in enumerate(books_on_pages):
        rendered_page = template.render(
            books_metadata=list(chunked(books_page, 2)),
            pages_href=pages_href,
            previous_page_href=get_previous_page_link(count, pages_href),
            next_page_href=get_next_page_link(count, pages_href),
            page_number=count + 1,
        )
        if count == 0:
            with open('pages/index.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)
        else:
            with open(f'pages/index{count}.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)


def get_books_pages():
    global books_metadata
    return [books_metadata[i: i + 10] for i in range(0, len(books_metadata), 10)]


def get_url_quote(books):
    for count, book in enumerate(books):
        book_path = book['book_path']
        img_path = book['img_src']
        books[count]['book_path'] = parse.quote(book_path)
        books[count]['img_src'] = parse.quote(img_path)
    return books


def get_pages_links(pages_numbers):
    pages_links = []
    for num in range(pages_numbers):
        if num == 0:
            pages_links.append('index.html')
        else:
            pages_links.append(f'index{num}.html')
    return pages_links


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


if __name__ == '__main__':
    os.makedirs('pages', exist_ok=True)
    with open('books_metadata.json', 'r') as file:
        books_metadata_json = json.load(file)
    books_metadata = get_url_quote(books_metadata_json)
    
    server = Server()
    server.watch('pages/template.html', on_reload)
    server.serve(root='pages/')
