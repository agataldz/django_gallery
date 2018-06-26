# Django Gallery

Simple django photo gallery site with photo-editing possibility by using Python Imaging Library.

## Getting Started

1) Clone the project:
```
git clone https://github.com/agataldz/django_gallery.git
```
2) Create virtual environment:
```
virtualenv gallery_env
```
```
source gallery_env/bin/activate
```
3) Install requirements:
```
pip install -r requirements.txt
```

4) Create a postgres database and add the credentials to settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'user_name',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
5) Run
```
python manage.py migrate
```
and
```
python manage.py runserver
```

## Screenshots

### Main page:

![Alt text](https://raw.githubusercontent.com/agataldz/django_gallery/master/gallery/media/readme/page.png?raw=true "Title")

### Example filter:

![Alt text](https://raw.githubusercontent.com/agataldz/django_gallery/master/gallery/media/readme/img.png?raw=true "Title")

### Example filter and text added:

![Alt text](https://raw.githubusercontent.com/agataldz/django_gallery/master/gallery/media/readme/img2.png?raw=true "Title")
