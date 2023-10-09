from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from fc_tp.db import get_db

bp = Blueprint('alb', __name__, url_prefix="/album")    


@bp.route('/')
def index():
    db = get_db()
    album = db.execute(
        """SELECT al.Title AS Album, COUNT(t.AlbumId) as canciones,t.name as artista
FROM Albums al
JOIN tracks t ON al.AlbumId = t.AlbumId
GROUP BY album;
"""
        
    ).fetchall()
    return render_template('Album/index.html', album=album)