import pytest

from app import create_app
from app.extensions import db
from app.models import User
from config import BaseConfig


class TestConfig(BaseConfig):
    TESTING = True
    LOGIN_DISABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_BINDS = {
        'help_system': 'sqlite:///:memory:'
    }
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    # Use a test config
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        # Create a test user if it doesn't exist
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User(username='testuser')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth_client(client, app):
    """A client with a logged-in user."""
    with client.session_transaction() as sess:
        pass  # Just to initialize

    # We can use a trick to bypass login or actually log in
    # Bypassing login for simplicity in integration tests:
    app.config['LOGIN_DISABLED'] = True
    return client
