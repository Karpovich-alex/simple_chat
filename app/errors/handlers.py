from flask import render_template, request
from app import db
from app.errors import bp


@bp.app_errorhandler(code=404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(code=500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


