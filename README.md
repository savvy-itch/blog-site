# Blog site

This is a blog site written in Django. It uses Postgres SQL to store articles. The articles are being stored as Markdown. Users can add articles to reading list, subscribe to the blog to receive email notifications once a new article is published. Alternatively, RSS subscription is available.

## How to run
To set up the application, first install Python and pip. Then run:
```
pip3 install -r requirements.txt
```

To run the application, run:
```
py3 manage.py runserver
```

To run the tests, run:
```
py3 manage.py test
```
