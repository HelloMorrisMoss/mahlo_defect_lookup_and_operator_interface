import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_sqlite_uri(db_path_raw):
    """Normalize SQLite URI for both Windows and Linux."""
    # Strip 'sqlite:///' if present to get just the path
    if db_path_raw.startswith('sqlite:///'):
        path_part = db_path_raw[10:]
    else:
        path_part = db_path_raw

    # Extract filename and ensure it's relative to basedir if not absolute
    db_filename = os.path.basename(path_part).replace('"', '')

    # If the original path was absolute, we could keep it, but for this project
    # we generally want it in the basedir or a specific subfolder.
    if 'help_versions.db' in db_path_raw:
        full_path = os.path.join(basedir, 'app', 'help_system', 'help_versions.db')
    else:
        full_path = os.path.join(basedir, db_filename)

    normalized_path = full_path.replace("\\", "/")
    return f"sqlite:///{normalized_path}"


class BaseConfig:
    # Use the filename from DATABASE_URL or default to app.db
    _db_url = os.environ.get('DATABASE_URL', 'app.db')
    SQLALCHEMY_DATABASE_URI = get_sqlite_uri(_db_url)

    SQLALCHEMY_BINDS = {
        'help_system': get_sqlite_uri('help_versions.db')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
