from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('Artista', __name__, url_prefix="/artistas")

@bp.route('/')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.name AS Nombre, count(al.AlbumId) AS Albums
         FROM artists ar JOIN albums al ON ar.ArtistId = al.ArtistId
		 GROUP BY Nombre
         ORDER BY Nombre ASC"""   
    ).fetchall()

    return render_template('Artista/index.html', artistas=artistas)

@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    artistas = db.execute(
        """SELECT ar.name AS Nombre, title AS Album, sum(milliseconds), g.name AS Genero
         FROM artists ar JOIN albums a ON ar.ArtistId = a.ArtistId
         JOIN tracks t ON t.AlbumId = a.AlbumId
         JOIN genres g ON t.GenreId = g.GenreId
		 WHERE a.ArtistId = ?
         ORDER BY Nombre ASC""",
         (id,)
    ).fetchone()

    artista = db.execute(
        """SELECT a.title AS Album, sum(t.Milliseconds) AS Duración,g.name AS Genero    
        FROM albums a  JOIN tracks t ON t.AlbumId = a.AlbumId
        JOIN genres g ON t.GenreId = g.GenreId

        WHERE ArtistId = ? 
		GROUP BY a.Title
        ORDER BY t.Milliseconds ASC""" ,
        (id,)  
    ).fetchall()


    return render_template('Artista/detalle.html', artistas=artistas, artista=artista)
