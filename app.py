import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from tiny_url_api import UrlShortenTinyurl

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']
        short_url = UrlShortenTinyurl().shorten(url)

        if not url or short_url == 'Error':
            flash('Please input a valid URL...')
            return redirect(url_for('index'))
        
        conn.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (url, short_url))
        conn.commit()
        conn.close()

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')


@app.route('/table/<id>')
def url_redirect(id):
    conn = get_db_connection()
    if id:
        id = id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks+1, id))

        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

@app.route('/table')
def table():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, short_url, clicks FROM urls'
                           ).fetchall()
    conn.close()

    urls = [dict(url) for url in db_urls]

    return render_template('table.html', urls=urls)