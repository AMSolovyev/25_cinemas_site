from bs4 import BeautifulSoup
import requests
import threading


def fetch_afisha_page():
    url = 'https://www.afisha.ru/msk/schedule_cinema/'
    afisha_response = requests.get(url, timeout=30)
    return afisha_response.text


def parse_afisha_list(raw_html):
    list_of_movies = []
    min_number_of_cinemas = 30
    soup = BeautifulSoup(raw_html, 'lxml')
    movie_table_tag = 'object s-votes-hover-area collapsed'
    movie_tag = soup.find_all('div', class_=movie_table_tag)
    for tag in movie_tag:
        number_of_cinemas = len(tag.find_all('tr'))
        if number_of_cinemas > min_number_of_cinemas:
            movie = {}
            movie_title = tag.find('h3', class_='usetags').find('a').get_text()
            afisha_page_tag = tag.find('h3', class_='usetags').find('a')
            movie_description_tag = tag.find('div', class_='m-disp-table')
            movie_description = movie_description_tag.find('p').get_text()
            movie_afisha_page = afisha_page_tag.attrs['href']
            movie['movie_title'] = movie_title
            movie['afisha_page'] = movie_afisha_page
            movie['movie_description'] = movie_description
            list_of_movies.append(movie)
    return list_of_movies


def fetch_movie_info(movie_info):
    movie = Movie.objects.search(movie_info['movie_title'])[0]
    movie_rating = movie.rating or 0.0
    rating_count = movie.votes or 0
    movie_id = movie.id
    poster_url = get_movie_poster(movie_id)
    movie_info.update(dict(zip(['movie_rating', 'rating_count', 'poster_url'],
                               [movie_rating, rating_count, poster_url])))
    return movie_info


def get_movie_poster(movie_id):
    poster_url = 'https://st.kp.yandex.net/images/film_iphone/\
iphone360_{}.jpg'.format(movie_id)
    return poster_url


def sort_movies(movies):
    return sorted(movies, key=lambda key: key['movie_rating'], reverse=True)


def get_first_n_movies(movies, number_of_movies=10):
    output_movies = [movie for movie in movies[:number_of_movies]]
    return output_movies


def get_movies():
    raw_html = fetch_afisha_page()
    movies = parse_afisha_list(raw_html)
    threads = []
    for movie in movies:
        thread = threading.Thread(target=fetch_movie_info, args=(movie, ))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    sorted_movies = sort_movies(movies)
    output_movies = get_first_n_movies(sorted_movies)
    return output_movies