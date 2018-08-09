from flask import Flask, render_template, jsonify
from flask_caching import Cache
from werkzeug.contrib.cache import FileSystemCache
from cinemas import get_movies



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': 'cache'})
file_system_cache = FileSystemCache('cache')


def get_cached_movies():
    movies = file_system_cache.get('movies')
    if movies is None:
        movies = get_movies()
        file_system_cache.set('movies', movies)
    return movies

@app.route('/')
@cache.cached(timeout=60)
def films_list():
    movies = get_cached_movies()
    return render_template('films_list.html', movies=movies)


@app.route('/api/movie_info.json', methods=['GET'])
def get_movie_info_api():
    movies = get_cached_movies()
    movies_json = jsonify(movies)
    return movies_json


@app.route('/api')
def api_documentation():
    return render_template('api.html')


if __name__ == "__main__":
    app.run()