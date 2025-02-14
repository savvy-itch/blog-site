# Blog site

This is a blog site written in Django. It uses Postgres SQL to store articles. The articles are being stored as Markdown. Users can subscribe to the blog to receive email notifications once a new article is published. The unsubscribe feature is also implemented.

## Distinctiveness and Complexity
The project is sufficiently distinct from the course's projects as the blog concept doesn't have much overlap with either wiki, search, mail or network projects. The blog implements several unique features that aren't covered in either of the course's projects, such as dark mode, email subscription, RSS feed subscription, adding articles to reading list. It also utilizes tools and practices that were not required in other projects such as unit testing, GitHub actions and PostgreSQL database usage.

The complexity of the project is expressed in the amount of features it provides both on the front-end and the back-end. The blog allows the admin to post article by submitting Markdown text of them through the admin page. By using `Markdown` package that allows adding CSS classes to Markdown elements, I was able to maintain consistent styling across all articles. To support code highlighting in the code blocks of the articles, I used `Pygments` package.

The blog utilizes PostgreSQL for storing data. I chose it over SQLite because Postgres is more suitable for production.

The main page supports filtering by article tags. It displays paginated article cards with short descriptions for each article. The blog is fully responsive.

Each article page includes dynamically calculated read time. There's also an "Edit" button visible only to admin (or any other authenticated user with "change" permission) that redirects him to the admin page of that article where it can be edited. At the bottom of each article there's a "Share" button and a section with similar articles.

Visitors can subscribe to blog to receive email notifications when new articles get published. These emails also include obligatory unsubscribe link that expires after 3 days. In order to make it work, I had to change the default behaviour of saving articles in the db. I also didn't want the unsubscribe link to expose the email of the user, and so I decided to encode it using a special token.

There's also another subscribtion option, via RSS. Clicking on the respective link will allow to add the blog to the user's feed and display the latest 10 articles there.

Users can also save articles to their reading lists. The IDs of those articles are being stored in browser's local storage.

Other small UX feature includes "Go Up" button when the page gets too long. It only gets displayed past a certain Y-axis scroll value.

The blog adheres to best practices such as test-driven development. The application is thoroughly tested using `unittest`. Furthermore, as shown in a lecture, I implemented GitHub action to run unit test on every code push.

+ estimated read time
+ admin-only article edit button
+ share button
+ similar articles 
+ email subscription
+ go up button
+ RSS feed
+ unit testing
+ GitHub actions

## Structure

`.github/workflows/ci.yml` - contains jobs for GitHub Actions, namely unit testing on every code push.

### `static/`
- `css/` - contains CSS files for the whole project
- `fonts/` - contains font files
- `images/` - contains images and icons used in the project

### `js/`
- `about.js` - dynamically calculates how many years I've been programming and renders it in "About" page.
- `articleDetail.js` - adds "Copy" button for every code block of an article, and implements the actual copying operation for it; improves the behaviour of "Share" button; implements "Go Up" button functionality that is displayed on overly long pages; improves UX of article's table of contents (smooth scrolling).
- `forms.js` - registers tag filters and updates URL accordingly on the client-side.
- `main.js` - calculates estimated reading time for the current article; handles saving/removing articles to/from the reading list. The IDs of save darticles are being stored in the local storage, and, on request, get passed to the server to retrieve those articles (see `views.py` and `readingList.js`).
- `readingList.js` - fetches saved articles and populates the reading list page with them.
- `sidebar.js` - enables to collapse/expand the sidebar on small screens.
- `subscribeForm.js` - handles submission of email subscription form.

### `templates/`
- `about/index.html` - template for the "About" page.
- `articles/article_detail.html` - template for article page.
- `email/email.html` - template for the email notification the users will receive if they subscribe to the email notifications.
- `reading_list/index.html` - template for the "Reading List" page.
- `unsubscribe/index.html` - template for the page the users will be redirected to when they unsubscribe from the email notifications.
-  `404.html` - template for the requests that return 404 status.
- `base_generic.html` - the main template for all pages of the blog.
- `base_with_sidebar.html` - the base template that adds sidebar (used for home page and article pages).
- `index.html` - home page of the blog.

### `tests/`
- `test_forms.py` - tests for forms.
- `test_models.py` - tests for models.
- `test_views.py` - tests for the views functions and classes.

### `admin.py`
Registers models that the admin sees in the admin page. I changes the default behaviour for saving articles to send email notifications to subscribers.

### `apps.py`
Django file to register applications.

### `context_processors.py`
Provides callables to display additional information in the templates.

### `email.py`
Handles sending email functionality, creates unsubscribe link by encoding an email address into a token.

### `feeds.py`
Handles RSS subscription by configuring how the feed should look like.

### `forms.py`
Creates email subscribtion form.

### `models.py`
Contains all models used in the app.

### `urls.py`
Contains all the available routes for the app and view functions for each of them.

### `views.py`
Handles the logic for all the routes.

### `examples.md`
Contains all the supported CSS necessary for correct conversion of articles' Markdown into HTML. If you want to add your own articles to the blog, use the syntax from this file. 

## How to run
To set up the application, first install Python and pip. After that run:
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
