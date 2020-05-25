# Верстаем онлайн библиотеку. Данные берем с [tululu.org](http://tululu.org)
Верстка простого сайта онлайн библиотеки книг в формате `.txt`. Для верстки используется фреймверк Bootstrap 4.
Данные скачиваются с сайта `tululu.org`. 

## Работа с кодом
Работу можно условно поделить на 2 пункта: Скраппинг книг с сайта [tululu.org](http://tululu.org), и 
выкладка онлайн библиотеки на сайте.

## Скачивание данных

#### Запуск
Должен быть установлен Python 3. Необходимые зависимости подгружаются из файла requirements.txt.

`pip3 install -r requirements.txt`

Запуск из командной строки с аргументами `$ python3 parse.py --args`.

#### Аргументы при запуске
| Аргумент      | Описание                |
| ------------- |------------------|
|`--start_page` |номер страницы, с которой начать скачивание книг.    |
|`--end_page`   |номер страницы, до которой скачивать книги.  |
|`--dest_folder`|аргумент, задающий путь, куда будут скачены книги, обложки книг и файл json.|
|`--dest_folder`|аргумент, задающий путь, куда будут скачены книги, обложки книг и файл json.|
|`--json_path`  |агрумент, задающий путь, куда будет сохранен файл с данными книг `books_metadata.json`.|
|`--skip_imgs`  |аргумент, указывающий что не будут скачены обложки книг.|
|`--skip_txt`   |аргумент, указывающий что не будут скачены книги.|

## Публикация книг на сайте

#### Верстка
Был сверстан простой сайт на фреймверке Bootstrap 4. Сайт доступен для работы локально

#### Работа с сайтом
С сайтом можно работать как онлайн, так и офлайн. Сайт опубликован на сервисе Github Pages и доступен по адресу
[https://andimeon.github.io](https://andimeon.github.io/book-lib/pages/index0.html)

Для работы офлайн необходимо скачать себе репозиторий.
Запуск библиотеки
`$ python3 render_website.py`
Скрипт запускает локальный сервер, доступный по адресу [http://127.0.0.1:5500](http://127.0.0.1:5500)

Так же можно работать с сайтом без запуска скрипта. Для этого необходимо открыть страницу `pages/index0.html` в браузере

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).