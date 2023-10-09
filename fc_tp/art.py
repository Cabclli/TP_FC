from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from fc_tp.db import get_db

bp = Blueprint('art', __name__, url_prefix="/artistas")    


@bp.route('/')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.name as nombre,count(al.AlbumId) as Albums from artists ar join albums al on ar.ArtistId = al.ArtistId
        group by nombre 
        order by nombre asc
"""
        
    ).fetchall()
    return render_template('Artista/index.html', artistas=artistas)