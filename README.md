# Cinemas Site

The program shows the best movies in the cinemas.
There are films in the [afisha](http://www.afisha.ru/msk/schedule_cinema/), and the [kinopoisk](https://www.kinopoisk.ru/).


# Description of API

API is connected in format- JSON. 
1. There will send 'GET' request to the address /movies
The response description:
movie_title — the movie title;
details.cinemas_count — the cinemas count;
details.movie_url — the description link on the site afisha.ru. 
2. There will send 'GET' request to the address /movie_for giving a film.
```
The request description:
      {
      "movie_url": movie_url,
      }
      
movie_url — a link for the the movie description on the afisha.ru;

The request example:

      {
      "movie_url": "https://www.afisha.ru/movie/229807/",
      }

 The response example:

      {
      "name": "Большой"
      "description": "Амбициозная драма про балет, станки и пуанты",
      "image": "https://s5.afisha. ru/MediaStorage/97/54/731f81fc013443cca7a5ff2a5497.jpg",
      "rating": 7.923
      }

```

# How to use
```
1. virtualenv -p python3 env
2. source env/bin/activate
3. pip install -r requirements.txt

 If your computer shows:
   No module named 'werkzeug' you will do:
pip install Werkzeug
  No module named 'jinja2 you will do:
pip install jinja2
  No module named 'itsdangerous'
pip install itsdangerous
  No module named 'click'
pip install click
  No module named 'flask_caching'
pip install flask_caching
4. python cinemas.py
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
