### Здесь есть функции:

- `upload_file_url(url, expires, secret)`: Загрузка файла через ссылку, url=ссылка, expires=время хранения файла в часах(можно оставить пустым), secret=удлинняет ссылку(можно оставить пустым).
- `upload_file_path(path, expires, secret)`: Тоже самое что и upload_file_url, только нужно указывать путь к файлу.
- `delete_file(token, url)`: Удаляет файл, token=токен, url=ссылкана файл в 0x0.
- `change_expires(url, expires, token)`: Изменяет время хранения файла, token=токен, url=ссылка на файл в 0x0, expires=новое время хранение файла в часах.