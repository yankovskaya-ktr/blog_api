# Blog API

Тестовое задание — REST API для системы комментариев блога.

### Функционал:

- Добавление поста
- Получение всех постов
- Добавление комментария к посту
- Получение всех комментариев к посту до 3 уровня вложенности
- Добавление коментария в ответ на другой комментарий (возможна любая вложенность)
- Получение всех вложенных комментариев для любого комментария  

### Запуск проекта:
  
Клонировать репозиторий и перейти в корневую директорию:  
  
```  
> git clone git@github.com:yankovskaya-ktr/blog_api.git
> cd blog_api
``` 
Создать файл .env по шаблону .env.template:

```
> cp .env.template .env
```
Запустить приложение:

``` 
> docker-compose up -d
``` 
Провести миграции:

``` 
> docker-compose exec web python manage.py migrate --noinput
``` 

Создать суперпользователя:

``` 
> docker-compose exec web python manage.py createsuperuser
``` 

### Swagger:

После запуска документация доступна по адресу: {host}/swagger/

